# usr/bin/env python3
# author: Isabel Meraner
# Project: Red List SwissLichens 2018-2020
# 2019

"""
Automatically collect material needed for field work from multiple folders and start printing dialogue.
"""

import argparse
import requests
import os
import sys
import csv
import re
import googlemaps
from os import listdir
# import win32print
from os.path import isfile, join

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk), end="")

def move_to_dir(PATH, files, outdir):
    for file in files:
        joined_path = os.path.join(PATH, file)
        print(joined_path)
        os.system('copy {} {}'.format(joined_path, outdir))

def main():
    argparser = argparse.ArgumentParser(
        description='Extract x,y coordinates for a-points and convert into lon/lat coordinates')

    argparser.add_argument(
        '-a', '--a_points_file',
        type=str,
        default=r'../a_punkte/A-Aufnahmen_RL2018.csv',
        help='')

    #engadin: 553 376 583 278
    #simmenthal: 296 527 340 257 215 260
    #wallis: 539 542 318 294 520
    #marchairuz: 465 452 466 445 446 487 451
    #jura: 432 443
    #gesa: 138 170 255 262 263 319 321 352 372 381 383 392 395 441 491 504 507 511 512 518 528 544 558 582 585 594 595 597
    #schaffhausen: 459 431 107 118 104 140 146 427
    argparser.add_argument(
        '-n', '--plot_numbers',
        type=str,
        nargs='+',
        default='226',
        help='')

    argparser.add_argument(
        '-o', '--output',
        type=str,
        default='..\\output\\',
        help='')

    argparser.add_argument(
        '-p', '--printing',
        type=bool,
        default=True,
        help='')

    args = argparser.parse_args()
    a_points_file = args.a_points_file
    outdir = args.output
    printing = args.printing

    plot_numbers = args.plot_numbers
    plot_numbers = plot_numbers.split(" ")


    with open(a_points_file, "r", encoding="latin-1") as a_points:
        csvreader = csv.reader(a_points, delimiter=';', quotechar='|')
        for row in csvreader:

            BearbeiterIn, Status, Bemerkung, Plot_ID, X, Y, TEXT, DAUER, STRUKTUR_T, RELIEF_TEX, VEGUEINH_1, SCANS_PLOT, CK_GH_MD, VEG_HOEHEN_STUFE_TXT, WALD_NICHTWALD_TXT, *rest = row
            if Plot_ID in plot_numbers:

                # convert coordinates and retrieve information from A-Plots File
                url = 'http://geodesy.geo.admin.ch/reframe/lv03towgs84?easting={}&northing={}&format=json'.format(X, Y)
                resp = requests.get(url=url)
                data = resp.json()
                reverse_geocode_result = gmaps.reverse_geocode((data["northing"], data["easting"]))
                short_name_loc = reverse_geocode_result[0]["address_components"][1]["short_name"]
                reg_name_loc = reverse_geocode_result[0]["address_components"][3]["long_name"]

                print("\n\nPlot_ID\tGebiet\tOrtschaft\tGrossregion\tX\tY\tlon-lat\tSTRUKTUR_T\tRELIEF_TEX")
                prGreen(Plot_ID)
                print(" ", TEXT, X, Y, data["northing"] + "," + data["easting"], "{}_{}_{}".format(Plot_ID, short_name_loc, reg_name_loc), STRUKTUR_T, VEGUEINH_1, VEG_HOEHEN_STUFE_TXT, RELIEF_TEX, WALD_NICHTWALD_TXT, end="\n\n", sep="\t")

                luftbild = [f for f in listdir(PATH_LUFTBILDER) if f.split("_")[2].rstrip(".pdf") == Plot_ID]
                print("Luftbild: ", luftbild)

                topomap = [f for f in listdir(PATH_TOPOMAPS) if f.split("_")[2].rstrip(".pdf") == Plot_ID]
                print("Topomap: ", topomap)

                lfi_skizzen = [f for f in listdir(PATH_LFI) if (f.split("_")[0] == X and f.split("_")[1] == Y)]
                print("lfi_skizzen: ", lfi_skizzen)

                rl2002_skizzen = [f for f in listdir(PATH_RL2002) if (f.split("_")[0] == X and f.split("_")[1] == Y)]
                print("rl2002_skizzen: ", rl2002_skizzen)

                if not os.path.exists(outdir):
                    os.mkdir(outdir)

                # copy files to output folder
                move_to_dir(PATH_LUFTBILDER, luftbild, outdir)
                move_to_dir(PATH_TOPOMAPS, topomap, outdir)
                move_to_dir(PATH_LFI, lfi_skizzen, outdir)
                move_to_dir(PATH_RL2002, rl2002_skizzen, outdir)


                if printing:
                    print("# Start print of files in directory ´{}´".format(outdir))
                    for file in os.listdir(outdir):
                        if file.endswith(".pdf"):
                            joined_path = os.path.join(outdir, file)
                            os.startfile(joined_path, "print")


if __name__ == '__main__':
    main()
