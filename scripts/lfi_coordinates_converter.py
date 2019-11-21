# usr/bin/env python3
# author: Isabel Meraner
# Project:
# 2019

import argparse
import os
import sys


def read_db(db_file):
    db_storage = {}
    counter = 0
    for line in db_file:
        counter += 1
        CLNR, THEO_X, THEO_Y, Z, ZENTRBESTOF_X, ZENTRBESTOF_Y, ZENTRBESTOF_STATUS_TXT = line.rstrip().split(";")
        print(CLNR, THEO_X, THEO_Y, Z, ZENTRBESTOF_X, ZENTRBESTOF_Y, ZENTRBESTOF_STATUS_TXT)
        x_y_theo = "{} {}".format(THEO_X, THEO_Y)
        db_storage[x_y_theo] = (ZENTRBESTOF_X, ZENTRBESTOF_Y, ZENTRBESTOF_STATUS_TXT, CLNR, THEO_X, THEO_Y, Z)
    return db_storage


def main():
    argparser = argparse.ArgumentParser(
        description='.')

    # CLNR;THEO_X;THEO_Y;Z;ZENTRBESTOF_X;ZENTRBESTOF_Y;ZENTRBESTOF_STATUS_TXT
    argparser.add_argument(
        '-d', '--db',
        type=str,
        default='../lfi_coordinates/db_coordinates.csv',
        help='')

    # Plot ID;X;Y;Z;GEMEINDE;TEXT
    argparser.add_argument(
        '-p', '--plots',
        type=str,
        default='../lfi_coordinates/plot_id.csv',
        help='')

    args = argparser.parse_args()
    db = args.db
    plots = args.plots

    count_newcoordinates = 0
    count_oldcoordinates = 0
    with open(db, "r", encoding="utf-8") as db_file, open(plots, "r", encoding="utf-8") as plots_file:
        db_storage = read_db(db_file)
        for line in plots_file:
            Plot_ID, X, Y, Z, GEMEINDE, TEXT = line.rstrip().split(";")
            xy_project = "{} {}".format(X, Y)
            if db_storage.get(xy_project):
                count_newcoordinates += 1
                print("{};{};{};{};{};{}".format(Plot_ID, db_storage[xy_project][0], db_storage[xy_project][1], Z,
                                                 GEMEINDE, TEXT))
            else:
                count_oldcoordinates += 1
                #print(">>> not found")
                print("{};{};{};{};{};{}".format(Plot_ID, X, Y, Z,
                                                 GEMEINDE, TEXT))

        print("new: {}  ---  old: {}".format(count_newcoordinates, count_oldcoordinates))
        sum_counts = count_oldcoordinates + count_newcoordinates
        print(sum_counts)


if __name__ == '__main__':
    main()
