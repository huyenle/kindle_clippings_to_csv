import collections
import json
import os
import re
import pandas as pd

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"output"
INPUT_DIR = u"/media/huyen/Kindle/documents"


def get_sections(filename):
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
        f.close()
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return
    position = match.group(1)

    clip['position'] = int(position)
    clip['content'] = lines[2]

    return clip


def export_csv(clips):
    for book in clips.items():
        df = pd.DataFrame.from_dict(book[1].items())
        file_name = re.sub('[^a-zA-Z0-9 \n\.]', '_', book[0])
        df.to_csv( OUTPUT_DIR + u"/%s.csv" % file_name)
    return None


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def save_clips(clips):
    """
    Save new clips to DATA_FILE
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(clips, f)


def main():
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    # extract clips
    sections = get_sections(INPUT_DIR + u'/My Clippings.txt')
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][str(clip['position'])] = clip['content']

    # remove key with empty value
    clips = {k: v for k, v in clips.items() if v}

    # save/export clips
    save_clips(clips)
    export_csv(clips)


if __name__ == '__main__':
    main()

