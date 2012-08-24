#!/usr/env python
# -*- coding: utf-8 -*-

# import glob

# filelist = glob.glob('*.dat')
# sources_file = open('sources_list.txt', 'wn')
# for filename in filelist:
#     sources_file.write(filename[0:-13]+'\t'+filename+'\n')
# sources_file.close()
from math import exp
import pdb

sources_file = open('statgood.txt', 'r')
sources_list = sources_file.readlines()
for i in range(len(sources_list)): sources_list[i] = sources_list[i].split()

coord_file = open('table_good.txt', 'r')
coords = coord_file.readlines()
for i in range(len(coords)): coords[i] = coords[i].split()

gnuplot_file = open('good_spectra.plt', 'wn')
gnuplot_file.write('#!/usr/bin/env gnuplot\n# -*- coding: utf-8 -*-\nset term postscript\nunset key\nset xlabel \'Vlsr, km/s\'\nset ylabel \'Ta*, K\'\n')

for source in sources_list:
    data_file = open(source[1], 'r')
    print source[1]
    data = data_file.readlines()
    # for i in range(len(data)): 
    #     #print data[i]
    #     pdb.set_trace()
    #     print i
    #     data[i] = data[i].split()
    #     #print 'OK!'
    # for i in range(len(data)):
    #     for j in range(len(data[i])):
    #         data[i][j] = float(data[i][j])
    approx_filename = source[0]+'_HCN14MHz.aprx'
    approx_file = open(approx_filename, 'wn')
    for i in range(len(data)): data[i] = data[i].split()
    y0 = float(source[3])
    a0 = float(source[9])
    a_left = float(source[11])
    a_right = float(source[13])
    v0 = float(source[5])
    w = float(source[7])
    tmpf = data[0]#.split()
    tmpl = data[-1]#.split()
    x = float(tmpf[0])
    xmax = float(tmpl[0])
    xnum = 250
    dx = (xmax - x)/xnum
    while x <= xmax:
        y = y0+a0*exp(-(x-v0)**2/(2.0*w**2))+a_left*exp(-(x-(v0-6.82))**2/(2.0*w**2))+a_right*exp(-(x-(v0+4.3))**2/(2.0*w**2))
        approx_file.write(str(x)+' '+str(y)+'\n')
        x += dx
    ra = ''
    dec = ''
    date = ''
    for j in coords:
        if j[0] == source[0]:
            ra = j[2]
            dec = j[3]
            date = j[1]
    data_file.close()
    approx_file.close()
    gnuplot_file.write("set out '"+source[0]+".ps'\n")
    gnuplot_file.write("set title '"+source[0]+" - "+date+" - ra:"+ra+", dec:"+dec+"'\n")
    gnuplot_file.write("plot '"+source[1]+"' w histeps lt -1, '"+approx_filename+"' w l lt -1\n\n")
gnuplot_file.close()
