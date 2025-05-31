#!/usr/bin/env python3

import os
import re
import csv
import unicodedata

# What this script does
#
# Phase 1 - generation of a in-memory set of words
#  - parse csv
#  - filter out words (and not 台羅)
#  - dump all into a set
#
# Phase 2 - parse the cangjie-large file
#  - read cangjie file
#  - chunk out the dictionary part
#  - cherry pick lines that are in the set
#
# Phase 3 - regenerate file
#  - attach this to cangjie3
#  - run uniq on it
#  - TODO:

# Gotchas:
#  - split() is semantically different from split(" "), because the former eats ideographic space

DICTIONARY_PATH = "./ChhoeTaigiDatabase/ChhoeTaigiDatabase"
CANGJIE_LARGE_PATH = "./tables/cangjie-large.txt"
CANGJIE_3_PATH = "./tables/cangjie3.txt"

WORDSET = set()
TABLE_LARGE = set()
TABLE_3 = set()

#
# Phase 1
# 
with open(os.path.join(DICTIONARY_PATH, "ChhoeTaigi_TaihoaSoanntengTuichiautian.csv")) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.__next__()
    header = { v: k for (k, v) in enumerate(header) }
    for row in reader:
        for c in (
            row[header['HanLoTaibunPoj']]
            + row[header['HanLoTaibunKip']]
        ):
            if unicodedata.category(c) == 'Lo':
                WORDSET.add(c)

with open(os.path.join(DICTIONARY_PATH, "ChhoeTaigi_TaijitToaSutian.csv")) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.__next__()
    header = { v: k for (k, v) in enumerate(header) }
    for row in reader:
        for c in (
            row[header['HanLoTaibunPoj']]
            + row[header['KaisoehHanLoPoj']]
            + row[header['LekuHanLoPoj']]
            + row[header['GoanchhehPoochhiongChuliau']]
        ):
            if unicodedata.category(c) == 'Lo':
                WORDSET.add(c)

with open(os.path.join(DICTIONARY_PATH, "ChhoeTaigi_MaryknollTaiengSutian.csv")) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.__next__()
    header = { v: k for (k, v) in enumerate(header) }
    for row in reader:
        for c in (
            row[header['HoaBun']]
        ):
            if unicodedata.category(c) == 'Lo':
                WORDSET.add(c)

with open(os.path.join(DICTIONARY_PATH, "ChhoeTaigi_TaioanPehoeKichhooGiku.csv")) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.__next__()
    header = { v: k for (k, v) in enumerate(header) }
    for row in reader:
        for c in (
            row[header['HoaBun']]
            + row[header['LekuHoabun']]
        ):
            if unicodedata.category(c) == 'Lo':
                WORDSET.add(c)

with open(os.path.join(DICTIONARY_PATH, "ChhoeTaigi_KauiokpooTaigiSutian.csv")) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.__next__()
    header = { v: k for (k, v) in enumerate(header) }
    for row in reader:
        for c in (
            row[header['HanLoTaibunKip']]
            + row[header['HoaBun']]
            + row[header['KaisoehHanLoPoj']]
        ):
            if unicodedata.category(c) == 'Lo':
                WORDSET.add(c)

print(f"INFO: loaded {len(WORDSET)} words")

#
# Phase 2
# 
with open(CANGJIE_LARGE_PATH) as f:
    lines = f.read().splitlines()
    lines = lines[30:] # HACK: drop the header of the table
    counter = 0

    for line in lines:
        (code, word) = line.split(" ")
        if word and word in WORDSET:
            counter += 1
            TABLE_LARGE.add((code, word))

    print(f"INFO: found {counter} words that has a cangjie code")

#
# Phase 3
# 
with open(CANGJIE_3_PATH, mode="r+") as f:
    lines = f.read().splitlines()
    header = lines[:30]
    lines = lines[30:] # HACK: drop the header of the table

    # Get all pairs
    for line in lines:
        (code, word) = line.split(" ")
        TABLE_3.add((code, word))

    # Dedup and get unique new ones
    TABLE_LARGE_DEDUP = {
        (code, word)
        for (code, word) in TABLE_LARGE
        if word not in map(lambda u: u[1], TABLE_3)
    }

    # Regenerate lines
    new_lines = []
    for (code, word) in TABLE_LARGE_DEDUP:
        new_lines.append(f"{code} {word}")
    new_lines.sort()
    print(f"INFO: will add {len(new_lines)} entries")

    output_content = "\n".join(new_lines)
    f.write(output_content)
