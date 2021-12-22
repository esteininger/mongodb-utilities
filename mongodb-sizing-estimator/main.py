#!/usr/bin/env python3
import os

file_path = 'mongostat.txt'

def build_obj(keys_list, row):
    obj = {}
    for index, key in enumerate(keys_list):
        obj[key] = row[index]

    return obj

def clean_msg(obj, total):
    msg = ''
    for key, val in obj.items():
        st = f'{val/total} {key}s / sec \n'
        msg += st
    return msg

def formulate(lis):
    iops = {
        'insert': 0,
        'query': 0,
        'update': 0,
        'delete': 0,
        'net_in': 0,
        'net_out': 0
    }
    for obj in lis:
        for row_key, row_val in obj.items():
            # loop thru iops dict
            for iop_key, iop_val in iops.items():
                if iop_key == row_key:
                    row_val_int = convert_val_to_ints(row_val)
                    print(type(row_val_int))
                    # iops[iop_key] += row_val_int

    return iops


def convert_val_to_ints(row_val):
    # strip asterik
    if '*' in row_val:
        row_val = int(row_val.replace("*",""))

    # convert mb to k
    if 'm' in row_val:
        row_val = float(row_val.replace("m",""))
        row_val = row_val * 1000

    # strip k letter to float
    if 'k' in row_val:
        print(row_val)
        row_val = float(row_val.replace("k",""))

    return row_val


def build_list_of_objs():
    keys_list = []
    master_arr = []

    with open(file_path) as f:
        lis = [line.split() for line in f]
        for index, row in enumerate(lis):
            if row[0] == 'insert':
                keys_list = row
            else:
                obj = build_obj(keys_list=keys_list, row=row)
                # obj['counter'] = index
                master_arr.append(obj)

    return master_arr

master_stats = build_list_of_objs()
result_set = formulate(master_stats)
total = len(result_set)


msg = clean_msg(obj=result_set, total=total)

print(msg)
