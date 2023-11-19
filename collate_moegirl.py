#!/usr/bin/env python
# This collation file is for moegirl.org.
# It MIGHT NOT be fit for other wikis.
import re
import sys

AFTER_SLASH = re.compile(r'\/.*')
MIDDLE_DOT = re.compile(r'·')


def dont_have(string: str, array: [str]):
    for i in array:
        if string.find(i) != -1:
            return False
    return True


def split_and_merge_single(group: [str], spliter: str):
    ret = []
    for i in group:
        for j in i.split(spliter):
            ret.append(j)
    return ret


def split_and_merge(group: [str], spliters: [str]):
    ret = group
    for i in spliters:
        tmp = []
        for j in split_and_merge_single(ret, i):
            tmp.append(j)
        ret = tmp
    return ret


def dedup(arr: [str]):
    ret = []
    for i in arr:
        if i not in ret:
            ret.append(i)
    return ret


def process_title(str):
    ret = [str]
    ret = list(filter(lambda x: dont_have(x, ["○", "〇"]), ret))
    ret = split_and_merge(ret, [
        ":",
        "/",
        "(",
        ")",
        "（",
        "）",
        "【",
        "】",
        "『",
        "』",
        "／"
    ])
    ret = list(map(lambda x: AFTER_SLASH.sub("", x), ret))
    ret = list(map(lambda x: MIDDLE_DOT.sub("", x), ret))
    ret = list(map(lambda x: x.strip(), ret))
    ret = list(filter(lambda x: len(x) > 1, ret))
    return ret


def main():
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    with open(filename) as file:
        lines = file.read().split("\n")
        print(f"Read {len(lines)} titles.")
        ret = []
        for i in lines:
            for j in process_title(i):
                ret.append(j)
        print(f"Got {len(ret)} words with duplicate. Deduplicating.")
        results = dedup(ret)
        print(f"Got {len(ret)} valid words.")
        with open(output_filename, "w") as ofile:
            ofile.write("\n".join(results))


if __name__ == "__main__":
    main()
