import argparse
import json
import math

import numpy as np
from matplotlib import pyplot as plt

my_parser = argparse.ArgumentParser(
    description="H plotter - fingerprinting result plotting",
    allow_abbrev=False,
    prog="hfinger",
    formatter_class=argparse.RawTextHelpFormatter,
)

my_group = my_parser.add_mutually_exclusive_group(required=True)
my_group.add_argument(
    "-f", "--file", action="store", type=str, help="Read a single json file"
)

args = my_parser.parse_args()


def x_coord(ac, bc, ab):
    return (math.pow(ac, 2) - math.pow(bc, 2) + math.pow(ab, 2)) / (2 * ab)


def y_coord(ac, c_x):
    tmp = (math.pow(ac, 2) - math.pow(c_x, 2))
    if tmp > 0:
        return math.sqrt(math.pow(ac, 2) - math.pow(c_x, 2))
    if tmp == 0:
        return 0
    else:
        return "Nothing"


def dist(ax, bx, ay, by):
    return math.sqrt(math.pow((bx - ax), 2) + math.pow((by - ay), 2))


def build_coordinates(coord_object):
    # cluster1 {0,0}
    # cluster2 {?,0}
    x_points = [0]
    y_points = [0, 0]

    # init values
    ab = 0
    ac = 0
    bc = 0

    # init base segment
    x_points.append(coord_object["cluster1"].get("cluster2"))

    for name, entry in coord_object.items():
        # take values
        bx = x_points[len(x_points) - 1]
        ax = x_points[len(x_points) - 2]
        by = y_points[len(y_points) - 1]
        ay = y_points[len(y_points) - 2]

        ab = dist(ax, bx, ay, by)

        # start
        if name == "cluster1":
            ac = list(entry.values())[1]

        # ignore first
        if name != "cluster1":
            bc = list(entry.values())[0]
            cx = x_coord(ac, bc, ab)
            cy = y_coord(ac, x_coord(ac, bc, ab))
            ac = list(entry.values())[1]
            x_points.append(cx)
            y_points.append(cy)

            #print("cx: ", cx)
            #print("cy: ", cy)

    return np.fromiter(x_points, dtype=int)  , np.fromiter(y_points, dtype=int)


def coordify(file):
    coords = {}
    radius = {}

    f = open(file)
    data = json.load(f)
    for entry in data['clusters']:
        coords[entry["name"]] = entry["distances"]
        radius[entry["name"]] = entry["distanceRef"]
    f.close()
    return radius, coords


if args.file:
    json_radius, json_coords = coordify(args.file)
    x_points, y_points = build_coordinates(json_coords)
    print("x_points ", x_points)
    print("y_points ", y_points)
    plt.axis([-5, 15, -5, 15])
    plt.plot(x_points, y_points)
    plt.show()
