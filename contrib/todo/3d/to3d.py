#! /usr/bin/env python


def to3d(x_bins, y_bins, min_show=3, filename="cross.dat"):
    vx = []
    vy = []
    fp = open(filename, "r")
    while True:
        line = fp.readline()
        if line.strip() == "":
            break
        rec = line.split()
        vx.append(float(rec[0]))
        vy.append(float(rec[1]))
    
    x_max = max(vx)
    x_min = min(vx)
    y_max = max(vy)
    y_min = min(vy)
    x_delta = (x_max-x_min)/x_bins
    y_delta = (y_max-y_min)/y_bins

    my3d = [[0 for i in xrange(y_bins+1)] for j in xrange(x_bins+1)]

    for ix in xrange(x_bins+1):
        for iy in xrange(y_bins+1):
            x_value = x_min + ix * x_delta
            y_value = y_min + iy * y_delta
            for x, y in zip(vx,vy):
                if abs(x_value-x) < x_delta and abs(y_value-y) < y_delta:
                    my3d[ix][iy] += 1

    tmp3d = []
    for ix in xrange(x_bins+1):
        tmp3d.extend(my3d[ix])
    max_val = max(tmp3d)

    fp = open("my3d.dat", "w")
    for ix in xrange(x_bins+1):
        for iy in xrange(y_bins+1):
            x_value = x_min + ix * x_delta
            y_value = y_min + iy * y_delta
            imy3d = my3d[ix][iy]
            print >>fp, "%12.6f%12.6f%12.6f" % (x_value, y_value, my3d[ix][iy]/float(max_val))
        print >>fp, ""
    fp.close()

    return



if __name__ == "__main__":
    line = raw_input("number of bins: \n> ")
    nbins = int(line)
    line = raw_input("filename: \n> ")
    fname = line.strip()
    to3d(nbins,nbins,3,filename=fname)
    



