# usr/bin/env python3
# author: Isabel Meraner
# Project: Red List SwissLichens 2018-2020
# 2019

"""
Retrieve x y coordinates from field work and convert them to lon-lat wgs84 for automatic creation of pins in google maps.

"""

import argparse
import requests
import os
import sys
import csv
import re
import googlemaps


def prGreen(skk): print("\033[92m {}\033[00m".format(skk), end="")


def main():
    argparser = argparse.ArgumentParser(
        description='Extract x,y coordinates for a-points and convert into lon/lat coordinates')

    argparser.add_argument(
        '-a', '--a_points_file',
        type=str,
        default=r'..\a_punkte\A-Aufnahmen_RL2018.csv',
        help='')

    # engadin: 553 376 583 278
    # simmenthal: 296 527 340 257 215 260
    # wallis: 539 542 318 294 520
    # marchairuz: 465 452 466 445 446 487 451
    # jura: 432 443
    # gesa: 138 170 255 262 263 319 321 352 372 381 383 392 395 441 491 504 507 511 512 518 528 544 558 582 585 594 595 597
    # schaffhausen: 459 431 107 118 104 140 146 427
    # wallis zusatz:: 244 492
    # bern: 202 211 486 478 187 479 505 502 480 237
    argparser.add_argument(
        '-n', '--plot_numbers',
        type=str,
        nargs='+',
        default='226',
        help='')

    argparser.add_argument(
        '-m', '--create_label_on_maps',
        action='store_true',
        default=False,
        help='')

    args = argparser.parse_args()
    a_points_file = args.a_points_file
    plot_numbers = args.plot_numbers
    plot_numbers = plot_numbers.split(" ")

    with open(r'../secret/secret.txt', 'r') as f:
        key = f.read()

    gmaps = googlemaps.Client(key=key)
    print(plot_numbers, type(plot_numbers))

    with open(a_points_file, "r", encoding="latin-1") as a_points:
        csvreader = csv.reader(a_points, delimiter=';', quotechar='|')
        for row in csvreader:

            BearbeiterIn, Status, Bemerkung, Plot_ID, X, Y, TEXT, DAUER, STRUKTUR_T, RELIEF_TEX, VEGUEINH_1, SCANS_PLOT, CK_GH_MD, VEG_HOEHEN_STUFE_TXT, WALD_NICHTWALD_TXT, *rest = row
            if Plot_ID in plot_numbers:
                # http://geodesy.geo.admin.ch/reframe/lv03towgs84?easting=733000&northing=245000&format=json

                url = 'http://geodesy.geo.admin.ch/reframe/lv03towgs84?easting={}&northing={}&format=json'.format(X, Y)

                resp = requests.get(url=url)
                data = resp.json()
                print("Plot_ID\tGebiet\tOrtschaft\tGrossregion\tX\tY\tlon-lat\tSTRUKTUR_T\tRELIEF_TEX")

                #                Look up an address with reverse geocoding
                reverse_geocode_result = gmaps.reverse_geocode((data["northing"], data["easting"]))
                # print(reverse_geocode_result)
                short_name_loc = reverse_geocode_result[0]["address_components"][1]["short_name"]
                # print(short_name_loc)
                reg_name_loc = reverse_geocode_result[0]["address_components"][3]["long_name"]
                # print(reg_name_loc)

                prGreen(Plot_ID)
                print(" ", TEXT, X, Y, data["northing"] + "," + data["easting"],
                      "{}_{}_{}".format(Plot_ID, short_name_loc, reg_name_loc), STRUKTUR_T, VEGUEINH_1,
                      VEG_HOEHEN_STUFE_TXT, RELIEF_TEX, WALD_NICHTWALD_TXT, end="\n\n", sep="\t")

                # form_name = reverse_geocode_result[0]["address_components"][3]["formatted_address"]
                # print(form_name)

                # print(Plot_ID, TEXT, short_name_loc, reg_name_loc, X, Y, data["northing"] + "," + data["easting"], STRUKTUR_T, RELIEF_TEX, end="\n\n", sep="\t")

                # https://maps.googleapis.com/maps/api/geocode/json?latlng=47.148340004771896,7.056276337888441&key=AIzaSyA2a4iIjLg6_g22-ksaSRLqgFj4XufG-6k&format=json


if __name__ == '__main__':
    main()
