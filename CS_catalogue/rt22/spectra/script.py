sources_file = open('sources_list.txt', 'r')
sources_list = sources_file.readlines()

gnuplot_file = open('good_spectra.plt', 'wn')
gnuplot_file.write('#!/usr/bin/env gnuplot\n# -*- coding: utf-8 -*-\nset term jpeg\nunset key\nset xlabel \'Vlsr, km/s\'\nset ylabel \'Ta*, K\'\n')

for source in sources_list:
    datafile_name = "../data/" + source[0:-2]
    aprxfile_name = "../aprx/" + source[0:-2] + ".aprx"
    gnuplot_file.write("set out '" + source[0:-2] + ".jpg'\n")
    gnuplot_file.write("set title '" + source[0:-2] + "'\n")
    gnuplot_file.write("plot '" + datafile_name + "' w histeps lt -1, '" + aprxfile_name + "' w histeps lt 1\n\n")
gnuplot_file.close()