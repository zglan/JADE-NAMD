
fp = open("elements.dat", "r")
line = fp.readline()
line = fp.readline()
n_line = int(line)
line = fp.readline()

for i in xrange(n_line):
    line = fp.readline()
    rec = line.split()
    atom_name = rec[0]
    atom_mass = rec[4]
    print "'"+atom_name.upper()+"'"+": ", atom_mass, ",",
    if i % 3 == 2:
        print "\n        ",

fp.close()


