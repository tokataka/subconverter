#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import cchardet
import re
import argparse
import os

COLOR = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9EA0',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkgrey': '#A9A9A9',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8F',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkslategrey': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dimgrey': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'grey': '#808080',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred': '#CD5C5C',
    'indigo': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray': '#D3D3D3',
    'lightgreen': '#90EE90',
    'lightgrey': '#D3D3D3',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightslategrey': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#F4A460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'slategrey': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32',
}

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
        matches = re.findall(r'({[^}]*\\c&H([0-9A-Fa-f]+)&[^}]*}([^{}\\]+))', text)
        for match in matches:
            entire, color, block1 = match
            if len(color) < 6:
                color = '0' * (6 - len(color)) + color
            color = f'#{color[4:6]}{color[2:4]}{color[0:2]}'
            text = text.replace(entire, f'<font color={color}>{block1}</font>')
        text = re.sub(r'{[^}]*}', '', text)
        text = text.replace('\\n', '\n').replace('\\N', '\n')

        return text

    @staticmethod
    def to_ass_text(text):
        matches = re.findall(r'(<font [^>]*color=[\"\']?([^\"\'>]+)[\"\']?[^>]*>(.+?)(</[^>]*font>))', text, flags=re.I+re.DOTALL)
        for match in matches:
            entire, color, block1, block2 = match

            if color.startswith('#'):
                color = color.upper()
            elif color.lower() in COLOR:
                color = COLOR[color.lower()]
            elif len(color) == 6 and len([x for x in color.upper() if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']]) == 6:
                color = '#' + color.upper()
            else:
                color = None

            if color:
                bgr = color[5:] + color[3:5] + color[1:3]
                text = text.replace(entire, f'{{\\c&H{bgr}&}}{block1}{{\\r}}')
            else:
                text = text.replace(entire, block1)

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

            text = re.sub(r'<br>', '\n', text, flags=re.I)
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
Style: Default,{self.font_face},{self.font_size},&H00FFFFFF,&HFF00FFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,1,2.7,0,2,0,0,80,1

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
