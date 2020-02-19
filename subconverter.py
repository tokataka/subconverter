#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from colour import Color
import cchardet
import re
import argparse
import os


class Dialogue:
    _start = 0
    _end = 0
    _text = ''

    def __init__(self, ext, start, end, text):
        if ext == 'smi':
            self._start = start
            self._end = end
            self._text = text
        elif ext == 'srt':
            self._start = self.from_srt_time(start)
            self._end = self.from_srt_time(end)
            self._text = text
        elif ext == 'ass':
            self._start = self.from_ass_time(start)
            self._end = self.from_ass_time(end)
            self._text = self.from_ass_text(text)

    def start(self, ext):
        if ext == 'smi':
            return self._start
        elif ext == 'srt':
            return self.to_srt_time(self._start)
        elif ext == 'ass':
            return self.to_ass_time(self._start)

    def end(self, ext):
        if ext == 'smi':
            return self._end
        elif ext == 'srt':
            return self.to_srt_time(self._end)
        elif ext == 'ass':
            return self.to_ass_time(self._end)

    def text(self, ext):
        if ext == 'smi':
            return self._text
        if ext == 'srt':
            return self._text
        elif ext == 'ass':
            return self.to_ass_text(self._text)

    @staticmethod
    def from_srt_time(hms):
        h, m, s, ms = re.findall('(\d+):(\d+):(\d+),(\d+)', hms)[0]
        return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)

    @staticmethod
    def to_srt_time(ms):
        hours = ms // 3600000
        ms -= hours * 3600000
        minutes = ms // 60000
        ms -= minutes * 60000
        seconds = ms // 1000
        ms -= seconds * 1000
        return '%02d:%02d:%02d,%03d' % (hours, minutes, seconds, ms)

    @staticmethod
    def from_ass_time(hms):
        h, m, s, ms10 = re.findall('(\d+):(\d+):(\d+).(\d+)', hms)[0]
        return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms10) * 10

    @staticmethod
    def to_ass_time(ms):
        hours = ms // 3600000
        ms -= hours * 3600000
        minutes = ms // 60000
        ms -= minutes * 60000
        seconds = ms // 1000
        ms -= seconds * 1000
        ms //= 10
        return '%01d:%02d:%02d.%02d' % (hours, minutes, seconds, ms)

    @staticmethod
    def from_ass_text(text):
        matches = re.findall(r'({[^}]*\\c&H([^}]+)&[^}]*}([^{}\\]+))', text)
        for match in matches:
            block, color, block2 = match
            if len(color) < 6:
                color = '0' * (6 - len(color)) + color
            color = f'#{color[4:6]}{color[2:4]}{color[0:2]}'
            text = text.replace(block, f'<font color={color}>{block2}</font>')
        text = text.replace('\\n', '\n').replace('\\N', '\n')

        return text

    @staticmethod
    def to_ass_text(text):
        matches = re.findall('(<font.*color=[\"\'](.+)[\"\'].*>).+</[^>]*font>', text, flags=re.I)
        for match in matches:
            block1, color= match
            color = Color(color)
            color_hex = color.get_hex_l().upper()
            bgr = color_hex[5:] + color_hex[3:5] + color_hex[1:3]
            text = text.replace(block1, '{\c&H' + bgr + '&}')

        text = re.sub(r'<[^>]*>', '', text)
        text = text.replace('\n', '\\N')
        return text


class SubConverter:
    title = ''
    ext = ''
    dialogues = []
    font_face = '맑은 고딕'
    font_size = 70
    width = 1920
    height = 1080

    def __init__(self, args=None):
        if args:
            self.font_face = args.font_face
            self.font_size = args.font_size
            self.width = args.width
            self.height = args.height

    def load_file(self, file):
        self.ext = file.split('.')[-1]
        self.ext = 'ass' if self.ext == 'ssa' else self.ext
        self.title = file[:-(len(self.ext) + 1)]
        self.dialogues = []

        with open(file, 'rb') as fp:
            content = fp.read()
            chdt = cchardet.detect(content)
            content = content.decode(chdt['encoding'])
            content = content.strip()

        content = content.replace('\r\n', '\n')

        if self.ext == 'smi':
            self.from_smi(content)
        elif self.ext == 'srt':
            self.from_srt(content)
        elif self.ext == 'ass':
            self.from_ass(content)

    def load_string(self, ext, content):
        self.ext = 'ass' if ext == 'ssa' else ext
        self.title = ''
        self.dialogues = []

        content = content.replace('\r\n', '\n')

        if self.ext == 'smi':
            self.from_smi(content)
        elif self.ext == 'srt':
            self.from_srt(content)
        elif self.ext == 'ass':
            self.from_ass(content)

    def convert(self, ext):
        if ext == 'smi':
            return self.to_smi()
        elif ext == 'srt':
            return self.to_srt()
        elif ext == 'ass':
            return self.to_ass()

    def from_smi(self, content):
        title = re.search(r'<title>(.+)</title>', content, flags=re.I)[1]
        self.title = title if title else self.title
        content = re.split(r'<body>', content, flags=re.I)[1]
        content = re.split(r'</body>', content, flags=re.I)[0]
        texts = re.split(r'<sync\s+start=', content, flags=re.I)[1:]

        for cur, next_ in zip(texts, (texts + [None])[1:]):
            start = int(re.match(r'\d+', cur)[0])
            end = int(re.match(r'\d+', next_)[0] if next_ else start)

            cur = cur.replace('\n', '')

            text = re.search(r'.+<p class=\w+[^>]*>(.+)$', cur, flags=re.I)[1]

            text = text.replace('<BR>', '\n')
            text = re.sub(r'&nbsp;', '', text, flags=re.I)
            text = text.strip()

            if not text:
                continue

            self.dialogues.append(Dialogue('smi', start, end, text))

    def from_srt(self, content):
        content = re.sub(r'\n{3,}', '\n\n', content)
        for block in content.split('\n\n'):
            lines = block.split('\n')
            if len(lines) < 3:
                continue
            start, end = re.findall(r'(.+) --> (.+).*', lines[1])[0]
            self.dialogues.append(Dialogue('srt', start, end, '\n'.join(lines[2:])))

    def from_ass(self, content):
        for line in content.split('\n'):
            if line.lower().startswith('dialogue:'):
                start, end, text = re.findall(r'[^,]*,([^,]+),([^,]+),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)$', line)[0]
                if not text:
                    continue
                self.dialogues.append(Dialogue('ass', start, end, text))

            elif line.lower().startswith('title:'):
                self.title = line[6:].strip()

    def to_smi(self):
        header = f'''<SAMI>
<HEAD>
<TITLE>{self.title}</TITLE>
<STYLE TYPE="text/css">
<!--
P [ text-align:center; font-family:{self.font_face}, Arial; color:white;
    background-color:black; ]
.KRCC [ Name:ko; lang:ko-KR; SAMIType:CC; ]
-->
</STYLE>
</HEAD>
<BODY>
'''
        # {, } are not allowed in formatted string..
        header = header.replace('[', '{').replace(']', '}')

        lines = []
        last_end = 0

        for dialogue in self.dialogues:
            if last_end and last_end != dialogue.start('smi'):
                lines.append(f'<SYNC Start={last_end}><P Class=KRCC>&nbsp;')
            lines.append(f'<SYNC Start={dialogue.start("smi")}><P Class=KRCC>')
            lines.append(dialogue.text('smi').replace('\n', '<BR>\n'))
            last_end = dialogue.end('smi')

        lines.append(f'<SYNC Start={last_end}><P Class=KRCC>&nbsp;')
        lines.append('</BODY>\n</SAMI>')
        return header + '\n'.join(lines)

    def to_srt(self):
        lines = []
        index = 1

        for dialogue in self.dialogues:
            lines.append(f'{index}')
            lines.append(f'{dialogue.start("srt")} --> {dialogue.end("srt")}')
            lines.append(dialogue.text('srt'))
            lines.append('')
            index += 1

        return '\n'.join(lines)

    def to_ass(self):
        header = f'''[Script Info]
Title: {self.title}
ScriptType: v4.00+
PlayDepth: 0
PlayResX: {self.width}
PlayResY: {self.height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{self.font_size},{self.font_size},&H00FFFFFF,&HFF00FFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,1,2.7,0,2,0,0,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
        lines = []

        for dialogue in self.dialogues:
            text = dialogue.text('ass')
            lines.append(f'Dialogue: 0, {dialogue.start("ass")},{dialogue.end("ass")},Default,,0,0,0,,{text}')

        return header + '\n'.join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='file', nargs='*', help='Input subtitle file(s) [.smi | .srt | .ass], leave blank to all files in current folder')
    parser.add_argument('-f', '--format', metavar='format', help='Target format [smi | srt | ass] (Default: ass)', default='ass')
    parser.add_argument('-d', '--delete', action="store_true", help='Enable to delete original files')
    parser.add_argument('-ff', '--font-face', metavar='font_face', help='Font face for .smi, .ass (Default: 맑은 고딕)', default="맑은 고딕")
    parser.add_argument('-fs', '--font-size', metavar='font_size', type=int, help='Font size for .ass (Default: 70)', default=70)
    parser.add_argument('-W', '--width', metavar='width', type=int, help='Resolution width for .ass (Default: 1920)', default=1920)
    parser.add_argument('-H', '--height', metavar='height', type=int, help='Resolution height for .ass (Default: 1080)', default=1080)
    args = parser.parse_args()

    files = args.file
    if not files:
        files = [x for x in os.listdir('.') if x.endswith('smi') or x.endswith('srt') or x.endswith('ass') or x.endswith('ssa')]

    if args.format == 'ssa':
        args.format = 'ass'

    if args.format not in ['smi', 'srt', 'ass']:
        print(f'Unsupported subtitle format: {args.format}\n')
        exit(1)

    sc = SubConverter(args)

    for file in files:
        ext = file.split('.')[-1]
        if ext == args.format:
            continue
        sc.load_file(file)
        converted = sc.convert(args.format)
        new_file = f'{file[:-(len(ext) + 1)]}.{args.format}'
        with open(new_file, 'w', encoding='utf-8') as fp:
            fp.write(converted)
        if args.delete:
            os.remove(file)

        print(f'Convert {file} -> {new_file} finished')

    print('Convert finished')
