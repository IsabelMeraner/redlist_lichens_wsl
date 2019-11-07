# usr/bin/env python3
# author: Isabel Meraner
# Project: Red List SwissLichens 2018-2020
# 2019

"""
Reformat dataset to horizontal format for the creation of a dynamic dropdown list.
"""

import argparse
import os
import sys
import csv
from collections import defaultdict, OrderedDict
import pandas as pd
from collections import OrderedDict, Callable


def main():
    argparser = argparse.ArgumentParser(
        description='.')

    argparser.add_argument(
        '-l', '--lfi',
        type=str,
        default=r'../lfi/lfi_horizontal.csv',
        help='')

    args = argparser.parse_args()
    lfi = args.lfi

    with open(lfi, "r", encoding="latin-1") as a_plots:
        csvreader = csv.reader(a_plots, delimiter=';', quotechar='"')
        dict_clnr = OrderedDict()

        for row in csvreader:
            if row[0].startswith("CLNR"):
                continue
            else:
                # print(row)
                clnr, txt, banr, spec, bhd, bhd_class, dist, azi = row[0], row[1], row[2], row[3], row[4], row[5], row[
                    6], row[7]
                # print(clnr, txt, banr, spec, bhd, bhd_class, dist, azi)
                clnr = "C_" + str(clnr)
                print(clnr)
                if clnr in dict_clnr:
                    print("appending")
                    dict_clnr[clnr].append(txt)
                else:
                    dict_clnr[clnr] = []
                    dict_clnr[clnr].append(txt)

    dict_keys = list(dict_clnr)
    dict_keys = dict_keys.insert(0, "")
    column_headers = dict_keys
    print(column_headers)

    vals = dict_clnr.values()
    print(vals)

    print("lenght dict: ", len(dict_clnr))
    print("length values max: ", len(sorted(dict_clnr.values(), key=len)[-1]))

    for k, v in dict_clnr.items():
        if len(v) < 51:

            to_insert = 51 - len(v)
            for i in range(to_insert):
                dict_clnr[k].append("")

    for k, v in dict_clnr.items():
        print(k, "---->", v)
        if len(v) != 50:
            print(">> error")

    dict_clnr_sorted = dict()
    for k, v in sorted(dict_clnr.items()):
        print(k, "---->", v)
        dict_clnr_sorted[k] = v

    print("lenght dict old: ", len(dict_clnr))
    print("lenght dict new: ", len(dict_clnr_sorted))

    print("length values max old: ", len(sorted(dict_clnr.values(), key=len)[-1]))
    print("length values max new: ", len(sorted(dict_clnr_sorted.values(), key=len)[-1]))

    df = pd.DataFrame(dict_clnr_sorted)

    print(df)
    df.to_csv(r'..\lfi\lfi_vertical_sorted.csv')


if __name__ == '__main__':
    main()
