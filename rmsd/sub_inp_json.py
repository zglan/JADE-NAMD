import json

def read_dat():
    inp = {}
    fp = open('inp.dat','r')
    for line in fp:
        if line.strip() != '':
            inp[line.split()[0]] = line.split()[1]
    return inp

def load_json(filename, encode='utf-8'):
    """
    load an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='r')
    obj = json.load(fp, encoding='utf-8')

    return obj

def dump_json(filename, obj, encode='utf-8'):
    """
    dump an object in json format.
    """
    json.encoder.FLOAT_REPR = lambda f: format("%.18g" % f)
    fp = open(filename, mode='w')
    my_str = json.dumps(obj, encoding=encode, indent=2)
    fp.write(my_str)
    fp.close()

    return

