import argparse
import json
import math
import random

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
        return math.sqrt(tmp)
    if tmp == 0:
        return 0
    else:
        tmp = -1*tmp
        return math.sqrt(tmp)*-1


def dist(ax, bx, ay, by):
    return math.sqrt(math.pow((bx - ax), 2) + math.pow((by - ay), 2))


def build_coordinates(coord_object, names):
    # cluster1 {0,0}
    # cluster2 {?,0}
    x_points = [0]
    y_points = [0, 0]

    # init values
    ab = 0
    ac = 0
    bc = 0

    # init base segment
    x_points.append(float(coord_object[list(coord_object.keys())[0]].get("B"))*10)

    # take values
    bx = x_points[len(x_points) - 1]
    ax = x_points[len(x_points) - 2]
    by = y_points[len(y_points) - 1]
    ay = y_points[len(y_points) - 2]
    ab = dist(ax, bx, ay, by)

    ignore_first = False
    ignore_second = False
    for entry in coord_object.values():
        # ignore first
        if ignore_first and ignore_second:
            ac = entry.get("A") * 10
            bc = entry.get("B") * 10
            cx = x_coord(ac, bc, ab)
            cy = y_coord(ac, x_coord(ac, bc, ab))
            x_points.append(cx)
            y_points.append(cy)

            # print("cx: ", cx)
            # print("cy: ", cy)
        else:
            if ignore_first:
                ignore_second = True
            ignore_first = True

    return np.fromiter(x_points, dtype=int), np.fromiter(y_points, dtype=int)


def coordify(file):
    coords = {}
    radius = {}
    name = {}

    f = open(file)
    data = json.load(f)
    for entry in data['clusters']:
        coords[entry["idFingerprintRef"]] = entry["distances"]
        radius[entry["idFingerprintRef"]] = entry["distanceRef"]
        name[entry["idFingerprintRef"]] = entry["name"]
    f.close()
    return radius, coords, name


if args.file:
    json_radius, json_coords, json_name = coordify(args.file)
    x_points, y_points = build_coordinates(json_coords, json_name)
    print("x_points ", x_points)
    print("y_points ", y_points)
    plt.axis([-5, 15, -5, 15])
    plt.axis("equal")

    count = 0
    previous_name = None
    color = None
    for circle, name in zip(json_radius.values(), json_name.values()):
        if name != previous_name:
            color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
            previous_name = name
        c = plt.Circle((x_points[count], y_points[count]), radius=0.1, color=color, alpha=0.8, label=name)
        plt.gca().add_artist(c)
        #plt.text(x_points[count], y_points[count], name, horizontalalignment='center', verticalalignment='center')
        plt.legend()
        count += 1
    #plt.plot(x_points, y_points)
    plt.show()
