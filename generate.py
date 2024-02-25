import os
import subprocess
from pathlib import Path

training_text_file = 'Ofl.txt'

lines = []

with open(training_text_file, 'r') as input_file:
    for line in input_file.readlines():
        if (line.strip() != ""):
            lines.append(line.strip())

output_directory = 'out/'
fonts = [
    'Noto Sans',
    'Noto Sans Italic',
    'Noto Sans Bold',
    'Nimbus Sans',
    'Nimbus Sans Italic',
    'Nimbus Sans Bold',
    'Noto Serif',
    'Noto Serif Italic',
    'Noto Serif Bold',
    'C059',
    'C059 Italic',
    'C059 Bold',
    'P052',
    'P052 Italic',
    'P052 Bold',
    'Cantarell',
    'Cantarell Bold',
    'Liberation Mono',
    'Liberation Mono Italic',
    'Liberation Mono Bold',
    'Liberation Sans',
    'Liberation Sans Italic',
    'Liberation Sans Bold',
    'Nimbus Roman',
    'Nimbus Roman, Italic',
    'Nimbus Roman, Bold',

]

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def filename_base(idx, font):
    font = font.replace(' ', '_')
    font = font.lower()
    return f'lat_{idx}_{font}'

def fnames(idx, font):
    fname = filename_base(idx, font)
    box_fpath = os.path.join(output_directory, f'{fname}.box')
    txt_fpath = os.path.join(output_directory, f'{fname}.gt.txt')
    skip_fpath = os.path.join(output_directory, f'{fname}.skip')
    return box_fpath, txt_fpath, skip_fpath

for idx, line in enumerate(lines):
    for font in fonts:
        box_fpath, txt_fpath, skip_fpath = fnames(idx, font)

        if os.path.exists(box_fpath):
            continue
        if os.path.exists(skip_fpath):
            continue
        with open(txt_fpath, 'w') as output_file:
            output_file.writelines([line])
        outputbase = os.path.join(output_directory, filename_base(idx, font))
        subprocess.Popen([
            'text2image',
            f'--font={font}',
            f'--text={txt_fpath}',
            f'--outputbase={outputbase}',
            '--xsize=2000',
            '--ysize=500',
        ])

# remove .gt.txt files for which no .box file was created
for idx, line in enumerate(lines):
    for font in fonts:
        box_fpath, txt_fpath, skip_fpath = fnames(idx, font)
        
        if os.path.exists(box_fpath) and os.stat(box_fpath).st_size > 0:
            continue
        
        print(f'No box file for {txt_fpath}! Skipping...')
        Path(skip_fpath).touch()

        if os.path.exists(txt_fpath):
            os.remove(txt_fpath)
        if os.path.exists(box_fpath):
            os.remove(box_fpath)
        
