#!/usr/bin/env gnuplot
# -*- coding: utf-8 -*-
set term postscript
unset key
set xlabel 'Vlsr, km/s'
set ylabel 'Ta*, K'
set out '106.797+5.312.ps'
set title '106.797+5.312 - 27/10/2010 - ra:22:19:18.27, dec:63:18:48.6'
plot '106.797+5.312-HCN14MHz.dat' w histeps lt -1, '106.797+5.312_HCN14MHz.aprx' w l lt -1

set out '108.18+5.51.ps'
set title '108.18+5.51 - 22/10/2010 - ra:22:28:52.00, dec:64:13:22.0'
plot '108.18+5.51-HCN14MHz.dat' w histeps lt -1, '108.18+5.51_HCN14MHz.aprx' w l lt -1

set out '109.86+2.10.ps'
set title '109.86+2.10 - 15/10/2010 - ra:22:56:18.10, dec:62:01:49.0'
plot '109.86+2.10-HCN14MHz.dat' w histeps lt -1, '109.86+2.10_HCN14MHz.aprx' w l lt -1

set out '110.093-0.065.ps'
set title '110.093-0.065 - 03/11/2010 - ra:23:05:25.71, dec:60:08:07.9'
plot '110.093-0.065-HCN14MHz.dat' w histeps lt -1, '110.093-0.065_HCN14MHz.aprx' w l lt -1

set out '111.542+0.777.ps'
set title '111.542+0.777 - 03/11/2010 - ra:23:13:45.37, dec:61:28:10.0'
plot '111.542+0.777-HCN14MHz.dat' w histeps lt -1, '111.542+0.777_HCN14MHz.aprx' w l lt -1

set out '123.05-6.31.ps'
set title '123.05-6.31 - 23/10/2010 - ra:0:52:19.90, dec:56:33:17.0'
plot '123.05-6.31-HCN14MHz.dat' w histeps lt -1, '123.05-6.31_HCN14MHz.aprx' w l lt -1

set out '133.749+1.198.ps'
set title '133.749+1.198 - 25/10/2010 - ra:2:25:53.55, dec:62:04:10.9'
plot '133.749+1.198-HCN14MHz.dat' w histeps lt -1, '133.749+1.198_HCN14MHz.aprx' w l lt -1

set out '133.94+1.04.ps'
set title '133.94+1.04 - 20/10/2010 - ra:2:27:03.80, dec:61:52:25.0'
plot '133.94+1.04-HCN14MHz.dat' w histeps lt -1, '133.94+1.04_HCN14MHz.aprx' w l lt -1

set out '173.481+2.446.ps'
set title '173.481+2.446 - 25/10/2010 - ra:5:39:12.90, dec:35:45:54.1'
plot '173.481+2.446-HCN14MHz.dat' w histeps lt -1, '173.481+2.446_HCN14MHz.aprx' w l lt -1

set out '173.49+2.42.ps'
set title '173.49+2.42 - 16/10/2010 - ra:5:39:13.10, dec:35:45:51.0'
plot '173.49+2.42-HCN14MHz.dat' w histeps lt -1, '173.49+2.42_HCN14MHz.aprx' w l lt -1

set out '173.69+2.87.ps'
set title '173.69+2.87 - 23/10/2010 - ra:5:41:33.80, dec:35:48:27.0'
plot '173.69+2.87-HCN14MHz.dat' w histeps lt -1, '173.69+2.87_HCN14MHz.aprx' w l lt -1

set out '174.19-0.09.ps'
set title '174.19-0.09 - 25/10/2010 - ra:5:30:42.00, dec:33:47:14.0'
plot '174.19-0.09-HCN14MHz.dat' w histeps lt -1, '174.19-0.09_HCN14MHz.aprx' w l lt -1

set out '183.34+0.59.ps'
set title '183.34+0.59 - 21/10/2010 - ra:5:51:06.00, dec:25:45:45.0'
plot '183.34+0.59-HCN14MHz.dat' w histeps lt -1, '183.34+0.59_HCN14MHz.aprx' w l lt -1

set out '188.79+1.02.ps'
set title '188.79+1.02 - 25/10/2010 - ra:6:09:06.50, dec:21:50:26.0'
plot '188.79+1.02-HCN14MHz.dat' w histeps lt -1, '188.79+1.02_HCN14MHz.aprx' w l lt -1

set out '188.95+0.89.ps'
set title '188.95+0.89 - 25/10/2010 - ra:6:08:53.40, dec:21:38:29.0'
plot '188.95+0.89-HCN14MHz.dat' w histeps lt -1, '188.95+0.89_HCN14MHz.aprx' w l lt -1

set out '189.032+0.785.ps'
set title '189.032+0.785 - 01/11/2010 - ra:6:08:41.16, dec:21:31:03.6'
plot '189.032+0.785-HCN14MHz.dat' w histeps lt -1, '189.032+0.785_HCN14MHz.aprx' w l lt -1

set out '189.78+0.34.ps'
set title '189.78+0.34 - 25/10/2010 - ra:6:08:34.50, dec:20:38:50.0'
plot '189.78+0.34-HCN14MHz.dat' w histeps lt -1, '189.78+0.34_HCN14MHz.aprx' w l lt -1

set out '192.597-0.035.ps'
set title '192.597-0.035 - 25/10/2010 - ra:6:12:56.41, dec:17:59:53.8'
plot '192.597-0.035-HCN14MHz.dat' w histeps lt -1, '192.597-0.035_HCN14MHz.aprx' w l lt -1

set out '192.60-0.05.ps'
set title '192.60-0.05 - 21/10/2010 - ra:6:12:54.00, dec:17:59:23.0'
plot '192.60-0.05-HCN14MHz.dat' w histeps lt -1, '192.60-0.05_HCN14MHz.aprx' w l lt -1

set out '194.934-1.227.ps'
set title '194.934-1.227 - 01/11/2010 - ra:6:13:15.18, dec:15:22:36.3'
plot '194.934-1.227-HCN14MHz.dat' w histeps lt -1, '194.934-1.227_HCN14MHz.aprx' w l lt -1

set out '196.45-1.68.ps'
set title '196.45-1.68 - 21/10/2010 - ra:6:14:37.10, dec:13:49:37.0'
plot '196.45-1.68-HCN14MHz.dat' w histeps lt -1, '196.45-1.68_HCN14MHz.aprx' w l lt -1

set out '203.316+2.055.ps'
set title '203.316+2.055 - 25/10/2010 - ra:6:41:09.66, dec:9:29:34.9'
plot '203.316+2.055-HCN14MHz.dat' w histeps lt -1, '203.316+2.055_HCN14MHz.aprx' w l lt -1

set out '206.538-16.358.ps'
set title '206.538-16.358 - 03/11/2010 - ra:5:41:42.89, dec:-1:54:33.6'
plot '206.538-16.358-HCN14MHz.dat' w histeps lt -1, '206.538-16.358_HCN14MHz.aprx' w l lt -1

set out '37.427+1.518.ps'
set title '37.427+1.518 - 02/11/2010 - ra:18:54:13.82, dec:4:41:31.7'
plot '37.427+1.518-HCN14MHz.dat' w histeps lt -1, '37.427+1.518_HCN14MHz.aprx' w l lt -1

set out '59.78+0.06.ps'
set title '59.78+0.06 - 22/10/2010 - ra:19:43:11.20, dec:23:44:03.0'
plot '59.78+0.06-HCN14MHz.dat' w histeps lt -1, '59.78+0.06_HCN14MHz.aprx' w l lt -1

set out '69.541-0.975.ps'
set title '69.541-0.975 - 24/10/2010 - ra:20:10:09.08, dec:31:31:37.4'
plot '69.541-0.975-HCN14MHz.dat' w histeps lt -1, '69.541-0.975_HCN14MHz.aprx' w l lt -1

set out '78.10+3.64.ps'
set title '78.10+3.64 - 22/10/2010 - ra:20:14:26.00, dec:41:13:33.0'
plot '78.10+3.64-HCN14MHz.dat' w histeps lt -1, '78.10+3.64_HCN14MHz.aprx' w l lt -1

set out '78.122+3.636.ps'
set title '78.122+3.636 - 24/10/2010 - ra:20:14:25.17, dec:41:13:35.5'
plot '78.122+3.636-HCN14MHz.dat' w histeps lt -1, '78.122+3.636_HCN14MHz.aprx' w l lt -1

set out '81.76+0.59.ps'
set title '81.76+0.59 - 22/10/2010 - ra:20:39:03.50, dec:42:25:53.0'
plot '81.76+0.59-HCN14MHz.dat' w histeps lt -1, '81.76+0.59_HCN14MHz.aprx' w l lt -1

set out '81.877+0.784.ps'
set title '81.877+0.784 - 24/10/2010 - ra:20:38:36.76, dec:42:37:59.6'
plot '81.877+0.784-HCN14MHz.dat' w histeps lt -1, '81.877+0.784_HCN14MHz.aprx' w l lt -1

set out '85.40-0.00.ps'
set title '85.40-0.00 - 22/10/2010 - ra:20:54:13.70, dec:44:54:08.0'
plot '85.40-0.00-HCN14MHz.dat' w histeps lt -1, '85.40-0.00_HCN14MHz.aprx' w l lt -1

set out '94.259-0.411.ps'
set title '94.259-0.411 - 24/10/2010 - ra:21:32:30.80, dec:51:02:15.5'
plot '94.259-0.411-HCN14MHz.dat' w histeps lt -1, '94.259-0.411_HCN14MHz.aprx' w l lt -1

set out 'H05480+2545.ps'
set title 'H05480+2545 - 30/10/2010 - ra:5:51:10.60, dec:25:46:14.0'
plot 'H05480+2545-HCN14MHz.dat' w histeps lt -1, 'H05480+2545_HCN14MHz.aprx' w l lt -1

set out 'IRAS05373+2349.ps'
set title 'IRAS05373+2349 - 01/11/2010 - ra:5:40:24.40, dec:23:50:54.0'
plot 'IRAS05373+2349-HCN14MHz.dat' w histeps lt -1, 'IRAS05373+2349_HCN14MHz.aprx' w l lt -1

set out 'S235.ps'
set title 'S235 - 23/10/2010 - ra:5:40:53.31, dec:35:41:48.8'
plot 'S235-HCN14MHz.dat' w histeps lt -1, 'S235_HCN14MHz.aprx' w l lt -1

