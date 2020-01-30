#!/usr/bin/python3
from collections import Counter
import sys

def extract_file_name(line):
    slice = line[line.index("(") + 1: line.index(":")]
    return slice

file_name = sys.argv[1]
rw = sys.argv[2]

with open(file_name, 'r') as reader:
    logdict = {}
    key = ""
    start_index = 0
    end_index = 0

    lines = reader.readlines()
    for (no,line) in enumerate(lines):
        if line.startswith("start: ") and rw in line:
            start_index = no
            # get the key to the dict
            if "java" in line:
                key = "java"
            if "ibis" in line:
                key = "ibis"
            if "kryo" in line:
                key = "kryo"
        if line.startswith("end: "):
            end_index = no
            slice = lines[(start_index+1):end_index]
            logdict.update({key:logdict.get(key, []) + [slice]})

    refined = {}
    for ls in logdict["java"]:
        if len(ls) == 0:
            print("warning: an open section without end")
            continue
        refined.update(java=refined.get("java", []) + [ls[4]])
    for ls in logdict["ibis"]:
        if len(ls) == 0:
            print("warning: an open section without end")
            continue
        refined.update(ibis=refined.get("ibis", []) + [ls[4]])

    temp_result = dict({k: list((extract_file_name(x)) for x in v) for k,v in refined.items()})

    final_result = dict({k:dict(Counter(v)) for k,v in temp_result.items()})

    print(final_result)



