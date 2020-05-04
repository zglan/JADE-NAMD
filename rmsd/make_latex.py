#! /usr/bin/env python
import os

tex_filename = 'latex.tex'
if os.path.exists(tex_filename):
    os.remove(tex_filename)
fp = open(tex_filename,"w")
print >>fp,  "\documentclass{article}"
print >> fp, "\usepackage{graphicx}"
print >> fp, "\\begin{document}"
print >> fp, ""



for i in range(10):
    for j in range(10):
        filename_old = "group_plot_" + str(i+1) +"_" +str(j+1) + ".bmp"
        filename_new = "group_plot_" + str(i+1) +"_" +str(j+1) + ".jpg"
        if os.path.exists(filename_old):
            command0 = "convert " + filename_old + " " + filename_new
            os.system(command0)

            pl_label = str(i+1) +"---" +str(j+1)
            print >> fp,  "\\begin{figure}[ht!]"
            print >> fp,  "    \\resizebox{120mm}{!}{\includegraphics{%s}}" % filename_new
            print >> fp,  "    \caption{ {\Large %s} }" % pl_label
            print >> fp,  "    \label{%s}" % pl_label
            print >> fp,  "\end{figure}"
            print >> fp,  "\\newpage"
            print >> fp, ""




print >> fp,  "\end{document}"
fp.close
