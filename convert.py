# -*- coding: utf-8 -*-
import sys
import re
import opencc
from pypinyin import lazy_pinyin
from manual_fix import manual_fix

FILE = sys.argv[1]

converter = opencc.OpenCC('t2s.json')
HANZI_RE = re.compile('^[\u4e00-\u9fa5]+$')
count = 0
last_word = None
with open(FILE) as f:
    for line in f:
        line = line.rstrip("\n")
        if not HANZI_RE.match(line):
            continue

        # Skip single character & too long pages
        if not 1 < len(line):
            continue

        # Skip list pages
        if line.endswith(('列表', '对照表')):
            continue

        if last_word and len(last_word) >= 4 and line.startswith(last_word):
            continue

        pinyin = "'".join(lazy_pinyin(line))
        if pinyin == line:
            # print("Failed to convert, ignoring:", pinyin, file=sys.stderr)
            continue

        if manual_fix(line):
            pinyin = manual_fix(line)
            print(f"Fixing {line} to {pinyin}", file=sys.stderr)

        last_word = line

        print("\t".join((converter.convert(line), pinyin, "0")))
        count += 1
        if count % 1000 == 0:
            print(str(count) + " converted", file=sys.stderr)

if count % 1000 != 0:
    print(str(count) + " converted", file=sys.stderr)
