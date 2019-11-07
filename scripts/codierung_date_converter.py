# usr/bin/env python3
# author: Isabel Meraner
# Project:
# 2019

"""
Convert unsystematic dates from historical, digitized herbarium of lichens to systematic format
in order to prepare the dataset for the DB import.
"""
import argparse


def main():
    argparser = argparse.ArgumentParser(
        description='.')

    argparser.add_argument(
        '-f', '--file',
        type=str,
        default=r'../codierung_herbar/det_datum.txt',
        help='')

    args = argparser.parse_args()
    date_file = args.file

    with open(date_file, "r") as date_file:
        for line in date_file:
            line = line.rstrip("\n")
            if line == "-":
                print("-")

            elif "." in line:
                date_items = line.split(".")
                if len(date_items) == 2:
                    if len(date_items[0]) == 1:
                        date_items[0] = "0{}".format(date_items[0])
                    new_date = "01.{}.{}".format(date_items[0], date_items[1])
                    print(new_date)
                elif len(date_items) == 3:
                    if len(date_items[0]) == 1:
                        date_items[0] = "0{}".format(date_items[0])
                    elif len(date_items[1]) == 1:
                        date_items[1] = "0{}".format(date_items[1])
                    new_date = "{}.{}.{}".format(date_items[0], date_items[1], date_items[2])
                    print(new_date)
                else:
                    print(">>>>>>>>>>error")
            else:
                new_date = "01.01.{}".format(line)
                print(new_date)


if __name__ == '__main__':
    main()
