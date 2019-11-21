# usr/bin/env python3
# author: Isabel Meraner
# Project: Rote Liste Gefährdete Flechten (2018-2022)
# 2019

"""
For a list of names that might contain synonymous / outdated or non-standardized names, run a lookup query in
the currently accepted checklist of lichens.

Resources used:
- Nimis et al. (2018)
- CJB: Conservatoire et jardin botaniquess ville de Geneve.
- Levenshtein package (python3)

Please note:
The input .csv-files contain the name variant (accepted name | synonym | homonym) (1st column)
and the associated db code (lichen.liart) (2nd column) [e.g. FILE_REDLIST_NOMENCLATURE or FILE_LIART|DB_EXPORT]
The input file [e.g. FILE_INPUT] should contain 1 name per line, which will be checked against the entries in the
database and normalized using the associated DB code that is also valid for synonyms.

# How to run:
python3 name_getter.py --rl FILE_REDLIST_NOMENCLATURE --liart FILE_LIART_EXPORT --db FILE_DB_EXPORT --input FILE_INPUT

"""

import argparse
import os
import sys
from collections import defaultdict
from fuzzywuzzy import fuzz


def prGreen(skk): print("\033[92m {}\033[00m".format(skk), end="")


def build_json(input_file: str, name_storage: dict) -> dict:
    """
    Clean input names from white spaces and store them in a dict-structure.
    :param input_file: file-like obj
    :param name_storage: dict to store names with db-codes
    :return name_store: dict
    """

    with open(input_file, "r") as input_file_handler:
        for line in input_file_handler:
            # print(line)
            name, db_code = line.rstrip("\n").split(";")
            name, db_code = name.rstrip(), db_code.rstrip()
            # print(name, db_code)
            name_storage[name] = db_code

    prGreen("\nItems in name_storage for file '{}' :\n ".format(input_file))
    print(len(name_storage))
    print(list(name_storage.items())[:11])
    return name_storage


def process_synonyms(input_file: str, syn_storage: dict, out=sys.stdout):
    """
    Check synonym lists for the names in the input file and print associated db-codes to stdout.
    :param out: sys.stdout
    :param input_file: file-like obj
    :return:
    """

    count_matches = 0
    count_failures = 0

    with open(input_file, "r", encoding="utf-8") as input_file_handler:
        for line in input_file_handler:
            name = line.rstrip().lstrip()
            # print(name)
            if syn_storage.get(name):
                # print("retrieved db code : {}".format(syn_storage[name]))
                print("{};{};{}".format(name, name, syn_storage[name]))
                count_matches += 1
            else:

                try:
                    species, epithet = name.split(" ")[0], name.split(" ")[1]
                    # see also: https://towardsdatascience.com/natural-language-processing-for-fuzzy-string-matching-with-python-6632b7824c49
                    max_levenshtein = 0
                    db_code = ""
                    alt_name = ""
                    for k, v in syn_storage.items():
                        # result = fuzz.partial_ratio(name, k) # @TODO: try fuzz.ratio()
                        result = fuzz.ratio(name, k)
                        if result >= max_levenshtein:
                            #print("result > max_levenshtein: score = {} name in input = {} similar name in db = {}".format(result, name, k))
                            max_levenshtein = result
                            db_code = syn_storage[k]
                            alt_name = k

                    if db_code:
                        count_matches += 1
                        print("{};{};{}xxx".format(name, alt_name, db_code))
                    else:
                        print("{};{};xxx".format(name, alt_name))
                        count_failures += 1

                except IndexError:

                    print("{};{};xxx".format(name, name))
                    count_failures += 1

    prGreen("\nmatches: {}  ---  vs. --- failures: {}\n".format(count_matches, count_failures))


def main():
    argparser = argparse.ArgumentParser(
        description='.')

    argparser.add_argument(
        '-r', '--rl',
        type=str,
        default=r'../nomenclat/rl_accepted_names.csv',
        help='')

    argparser.add_argument(
        '-l', '--liart',
        type=str,
        default=r'../nomenclat/db_synonym_list_liart.csv',
        help='')

    argparser.add_argument(
        '-d', '--db',
        type=str,
        default=r'../nomenclat/db_synonym_list_alltaxa.csv',
        help='')

    argparser.add_argument(
        '-i', '--input',
        type=str,
        default=r'../nomenclat/input_groner.txt',
        help='')

    args = argparser.parse_args()
    rl = args.rl
    liart = args.liart
    db = args.db
    input_file = args.input

    json_rl = defaultdict(int)
    json_rl_dict = build_json(rl, json_rl)

    json_liart = defaultdict(int)
    json_liart_dict = build_json(liart, json_liart)

    json_db = defaultdict(int)
    json_db_dict = build_json(db, json_db)

    syn_storage = {**json_liart_dict, **json_db_dict, **json_rl_dict}
    prGreen("\nItems in syn_storage [expected: {}]\n".format(
        (len(json_rl_dict) + len(json_liart_dict) + len(json_db_dict))))
    print(len(syn_storage))

    process_synonyms(input_file, syn_storage)

    # TODO: use GBIF API to retrieve synonyms:
    # http://api.gbif.org/v1/species/3467182/synonyms
    # http://api.gbif.org/v1/species?name=Lepra%20amara&limit=500


if __name__ == '__main__':
    main()
