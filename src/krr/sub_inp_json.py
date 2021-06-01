#!/usr/bin/env python

import json


def read_dat():
    inp = {}
    fp = open('inp.dat', 'r')
    for line in fp:
        if line.strip() != '':
            inp[line.split()[0]] = line.split()[1]
    return inp


def read_dat_with_label(filename):
    inp = {}
    fp = open(filename, 'r')
    for line in fp:
        if line.strip() != '':
            if "!" not in line.strip():
                string_read = line.strip().split('=', 1)
                string_zero = string_read[0].replace(' ', '')
                strong_one = string_read[1].replace(' ', '')
                inp[string_zero] = strong_one
    return inp


def load_json(filename):
    """
    load an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='r')
    obj = json.load(fp)

    return obj


def dump_json(filename, obj):
    """
    dump an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='w')
    my_str = json.dumps(obj, indent=2)
    fp.write(my_str)
    fp.close()

    return
