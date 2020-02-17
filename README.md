# subconverter
Subtitle Converter (smi <-> srt <-> ass)

Currently only maintains color informations

## Requirements

- python3
- colour
- cchardet


## Usage examples

Commandline:
```sh
python3 subconverter.py -d  # converts all subtitles in current directory to .ass and delete originals

python3 subconverter.py -f srt foo.smi bar.ass  # converts foo.smi, bar.ass to foo.srt, bar.srt
```

Python code:
```python
from subconverter import SubConverter

sc = SubConverter()
sc.load_file('./foo.srt')
converted = sc.convert('ass')
```


## Optional arguments list
| Parameter       | Default   | Description
|-----------------|-----------|-------------
| -f --format     | 'ass'     | Target format ['smi' \| 'srt' \| 'ass']
| -d --delete     |           | Enable to delete original files
| -ff --font-face | '맑은 고딕' | Font face for .smi and .ass
| -fs --font-size | 70        | Font size for .ass
| -W --width      | 1920      | Video width for .ass
| -H --height     | 1080      | Video height for .ass
