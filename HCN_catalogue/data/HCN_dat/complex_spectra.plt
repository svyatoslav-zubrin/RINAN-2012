#!/usr/bin/env gnuplot
# -*- coding: utf-8 -*-

set term postscript
unset key
set xlabel 'Vlsr, km/s'
set ylabel 'Ta*, K'

# already plotted
set out '109.92+1.98.ps'
set title '109.92+1.98 - 22.10.2010 - HCN(1-0)'
plot '109.92+1.98-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '111.24-0.76.ps'
set title '111.24-0.76 - 24.10/04.11.2010 - HCN(1-0)'
plot '111.24-0.76-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '173.71+2.35.ps'
set title '173.71+2.35 - 22.10.2010 - HCN(1-0)'
plot '173.71+2.35-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '202.92+1.47.ps'
set title '202.92+1.47 - 24.10.2010 - HCN(1-0)'
plot '202.92+1.47-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '36.10+0.56.ps'
set title '36.10+0.56 - 22.10.2010 - HCN(1-0)'
plot '36.10+0.56-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '79.75+0.99.ps'
set title '79.75+0.99 - 27.10.2010 - HCN(1-0)'
plot '79.75+0.99-HCN14MHz.dat' w histeps lt -1

# already plotted
set out '90.90+1.15.ps'
set title '90.90+1.15 - 22.10.2010 - HCN(1-0)'
plot '90.90+1.15-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '.ps'
# set title ' - 31.10.2010 - HCN(1-0)'
# plot '-HCN14MHz.dat' w histeps lt -1

# already plotted
# set out '208.816-19.239.ps'
# set title '208.816-19.239 - 03.11.2010 - HCN(1-0)'
# plot '208.816-19.239-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '205.539-14.602.ps'
# set title '205.539-14.602 - 01.11.2010 - HCN(1-0)'
# plot '205.539-14.602-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '170.657-0.269.ps'
# set title '170.657-0.269 - 31.10.2010 - HCN(1-0)'
# plot '170.657-0.269-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '158.395-20.575.ps'
# set title '158.395-20.575 - 24.10.2010 - HCN(1-0)'
# plot '158.395-20.575-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '122.015-7.072.ps'
# set title '122.015-7.072 - 31.10.2010 - HCN(1-0)'
# plot '122.015-7.072-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '105.469+9.828.ps'
# set title '105.469+9.828 - 24.10.2010 - HCN(1-0)'
# plot '105.469+9.828-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '102.641+15.784.ps'
# set title '102.641+15.784 - 27.10.2010 - HCN(1-0)'
# plot '102.641+15.784-HCN14MHz.dat' w histeps lt -1

# # already plotted
# set out '49.49-0.387.ps'
# set title '49.49-0.387 - 27.10.2010 - HCN(1-0)'
# plot '49.49-0.387-HCN14MHz.dat' u ($1):($2)-1 w histeps lt -1

# set out '106.797+5.312.ps'
# set title '106.797+5.312 - Date - HCN(1-0)'
# plot '106.797+5.312-HCN14MHz.dat' w histeps lt -1

# set out '108.18+5.51.ps'
# set title '108.18+5.51-HCN14MHz - Date - HCN(1-0)'
# plot '108.18+5.51-HCN14MHz.dat' w histeps lt -1


# set out '108.596+0.493.ps'
# set title '108.596+0.493-HCN14MHz - 31.20.2010 - HCN(1-0)'
# plot '108.596+0.493-HCN14MHz.dat' w histeps lt -1


# set out '108.75-0.96.ps'
# set title '108.75-0.96-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '108.75-0.96-HCN14MHz.dat' w histeps lt -1


# set out '109.86+2.10-HCN14MHz.ps'
# set title '109.86+2.10-HCN14MHz - Date - HCN(1-0)'
# plot '109.86+2.10-HCN14MHz.dat' w histeps lt -1


# set out '110.093-0.065-HCN14MHz.ps'
# set title '110.093-0.065-HCN14MHz - Date - HCN(1-0)'
# plot '110.093-0.065-HCN14MHz.dat' w histeps lt -1


# set out '111.236-1.238.ps'
# set title '111.236-1.238-HCN14MHz - 31.20.2010 - HCN(1-0)'
# plot '111.236-1.238-HCN14MHz.dat' w histeps lt -1


# set out '111.542+0.777.ps'
# set title '111.542+0.777-HCN14MHz - Date - HCN(1-0)'
# plot '111.542+0.777-HCN14MHz.dat' w histeps lt -1


# set out '114.513-0.535.ps'
# set title '114.513-0.535-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '114.513-0.535-HCN14MHz.dat' w histeps lt -1


# set out '121.28+0.65.ps'
# set title '121.28+0.65-HCN14MHz - 22/24/30.10.2010 - HCN(1-0)'
# plot '121.28+0.65-HCN14MHz.dat' w histeps lt -1


# set out '123.05-6.31.ps'
# set title '123.05-6.31-HCN14MHz - Date - HCN(1-0)'
# plot '123.05-6.31-HCN14MHz.dat' w histeps lt -1


# set out '133.749+1.198.ps'
# set title '133.749+1.198-HCN14MHz - Date - HCN(1-0)'
# plot '133.749+1.198-HCN14MHz.dat' w histeps lt -1


# set out '133.94+1.04.ps'
# set title '133.94+1.04-HCN14MHz - Date - HCN(1-0)'
# plot '133.94+1.04-HCN14MHz.dat' w histeps lt -1


# set out '136.84+1.12.ps'
# set title '136.84+1.12-HCN14MHz - 22.10.2010 - HCN(1-0)'
# plot '136.84+1.12-HCN14MHz.dat' w histeps lt -1


# set out '173.481+2.446.ps'
# set title '173.481+2.446-HCN14MHz - Date - HCN(1-0)'
# plot '173.481+2.446-HCN14MHz.dat' w histeps lt -1


# set out '173.49+2.42.ps'
# set title '173.49+2.42-HCN14MHz - Date - HCN(1-0)'
# plot '173.49+2.42-HCN14MHz.dat' w histeps lt -1


# set out '173.69+2.87.ps'
# set title '173.69+2.87-HCN14MHz - Date - HCN(1-0)'
# plot '173.69+2.87-HCN14MHz.dat' w histeps lt -1


# set out '174.19-0.09.ps'
# set title '174.19-0.09-HCN14MHz - Date - HCN(1-0)'
# plot '174.19-0.09-HCN14MHz.dat' w histeps lt -1


# set out '183.34+0.59.ps'
# set title '183.34+0.59-HCN14MHz - Date - HCN(1-0)'
# plot '183.34+0.59-HCN14MHz.dat' w histeps lt -1


# set out '188.79+1.02.ps'
# set title '188.79+1.02-HCN14MHz - Date - HCN(1-0)'
# plot '188.79+1.02-HCN14MHz.dat' w histeps lt -1


# set out '188.95+0.89.ps'
# set title '188.95+0.89-HCN14MHz - Date - HCN(1-0)'
# plot '188.95+0.89-HCN14MHz.dat' w histeps lt -1


# set out '189.032+0.785.ps'
# set title '189.032+0.785-HCN14MHz - Date - HCN(1-0)'
# plot '189.032+0.785-HCN14MHz.dat' w histeps lt -1


# set out '189.78+0.34.ps'
# set title '189.78+0.34-HCN14MHz - Date - HCN(1-0)'
# plot '189.78+0.34-HCN14MHz.dat' w histeps lt -1


# set out '192.597-0.035.ps'
# set title '192.597-0.035-HCN14MHz - Date - HCN(1-0)'
# plot '192.597-0.035-HCN14MHz.dat' w histeps lt -1


# set out '192.60-0.05.ps'
# set title '192.60-0.05-HCN14MHz - Date - HCN(1-0)'
# plot '192.60-0.05-HCN14MHz.dat' w histeps lt -1


# set out '194.934-1.227.ps'
# set title '194.934-1.227-HCN14MHz - Date - HCN(1-0)'
# plot '194.934-1.227-HCN14MHz.dat' w histeps lt -1

# set out '196.45-1.68.ps'
# set title '196.45-1.68-HCN14MHz - Date - HCN(1-0)'
# plot '196.45-1.68-HCN14MHz.dat' w histeps lt -1

# set out '203.316+2.055.ps'
# set title '203.316+2.055-HCN14MHz - Date - HCN(1-0)'
# plot '203.316+2.055-HCN14MHz.dat' w histeps lt -1

# set out '205.109-14.111.ps'
# set title '205.109-14.111-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '205.109-14.111-HCN14MHz.dat' w histeps lt -1

# set out '206.538-16.358.ps'
# set title '206.538-16.358-HCN14MHz - Date - HCN(1-0)'
# plot '206.538-16.358-HCN14MHz.dat' w histeps lt -1

# set out '34.3+0.2.ps'
# set title '34.3+0.2-HCN14MHz - 27.10.2010 - HCN(1-0)'
# plot '34.3+0.2-HCN14MHz.dat' w histeps lt -1

# set out '34.403+0.233.ps'
# set title '34.403+0.233-HCN14MHz - 02.11.2010 - HCN(1-0)'
# plot '34.403+0.233-HCN14MHz.dat' w histeps lt -1

# set out '34.82+0.352.ps'
# set title '34.82+0.352-HCN14MHz - 27.10.2010 - HCN(1-0)'
# plot '34.82+0.352-HCN14MHz.dat' w histeps lt -1

# set out '37.427+1.518.ps'
# set title '37.427+1.518-HCN14MHz - 02.11.2010 - HCN(1-0)'
# plot '37.427+1.518-HCN14MHz.dat' w histeps lt -1

# set out '45.07+0.13.ps'
# set title '45.07+0.13-HCN14MHz - 02.11.2010 - HCN(1-0)'
# plot '45.07+0.13-HCN14MHz.dat' w histeps lt -1

# set out '45.44+0.07.ps'
# set title '45.44+0.07-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '45.44+0.07-HCN14MHz.dat' w histeps lt -1

# set out '45.47+0.07.ps'
# set title '45.47+0.07-HCN14MHz - 27.10.2011 - HCN(1-0)'
# plot '45.47+0.07-HCN14MHz.dat' w histeps lt -1

# set out '49.267-0.337.ps'
# set title '49.267-0.337-HCN14MHz - 31.10.2010 - HCN(1-0)'
# plot '49.267-0.337-HCN14MHz.dat' w histeps lt -1

# set out '49.485-0.359.ps'
# set title '49.485-0.359-HCN14MHz - 27.10.2010 - HCN(1-0)'
# plot '49.485-0.359-HCN14MHz.dat' w histeps lt -1

# set out '50.00+0.59.ps'
# set title '50.00+0.59-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '50.00+0.59-HCN14MHz.dat' w histeps lt -1

# set out '53.032+0.117.ps'
# set title '53.032+0.117-HCN14MHz - 31.10.2010 - HCN(1-0)'
# plot '53.032+0.117-HCN14MHz.dat' w histeps lt -1

# set out '59.78+0.06.ps'
# set title '59.78+0.06-HCN14MHz - Date - HCN(1-0)'
# plot '59.78+0.06-HCN14MHz.dat' w histeps lt -1

# set out '59.832+0.671.ps'
# set title '59.832+0.671-HCN14MHz - 02.11.2010 - HCN(1-0)'
# plot '59.832+0.671-HCN14MHz.dat' w histeps lt -1

# set out '60.56-0.17.ps'
# set title '60.56-0.17-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '60.56-0.17-HCN14MHz.dat' w histeps lt -1

# set out '69.541-0.975.ps'
# set title '69.541-0.975-HCN14MHz - 24/29.10.2010 - HCN(1-0)'
# plot '69.541-0.975-HCN14MHz.dat' w histeps lt -1

# set out '73.062+1.797.ps'
# set title '73.062+1.797-HCN14MHz - 31.10.2010 - HCN(1-0)'
# plot '73.062+1.797-HCN14MHz.dat' w histeps lt -1

# set out '75.76+0.34.ps'
# set title '75.76+0.34-HCN14MHz - 22.10.2010 - HCN(1-0)'
# plot '75.76+0.34-HCN14MHz.dat' w histeps lt -1

# set out '75.772+0.343.ps'
# set title '75.772+0.343-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '75.772+0.343-HCN14MHz.dat' w histeps lt -1

# set out '78.10+3.64.ps'
# set title '78.10+3.64-HCN14MHz - Date - HCN(1-0)'
# plot '78.10+3.64-HCN14MHz.dat' w histeps lt -1

# set out '78.122+3.636.ps'
# set title '78.122+3.636-HCN14MHz - Date - HCN(1-0)'
# plot '78.122+3.636-HCN14MHz.dat' w histeps lt -1

# set out '81.76+0.59.ps'
# set title '81.76+0.59-HCN14MHz - Date - HCN(1-0)'
# plot '81.76+0.59-HCN14MHz.dat' w histeps lt -1

# set out '81.87+0.78.ps'
# set title '81.87+0.78-HCN14MHz - 15.10.2010 - HCN(1-0)'
# plot '81.87+0.78-HCN14MHz.dat' w histeps lt -1

# set out '81.877+0.784.ps'
# set title '81.877+0.784-HCN14MHz - Date - HCN(1-0)'
# plot '81.877+0.784-HCN14MHz.dat' w histeps lt -1

# set out '85.40-0.00.ps'
# set title '85.40-0.00-HCN14MHz - Date - HCN(1-0)'
# plot '85.40-0.00-HCN14MHz.dat' w histeps lt -1

# set out '94.259-0.411.ps'
# set title '94.259-0.411-HCN14MHz - Date - HCN(1-0)'
# plot '94.259-0.411-HCN14MHz.dat' w histeps lt -1

# set out '99.982+4.17.ps'
# set title '99.982+4.17-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot '99.982+4.17-HCN14MHz.dat' w histeps lt -1

# set out 'DR21(OH).ps'
# set title 'DR21(OH)-HCN14MHz - 24.10.2010 - HCN(1-0)'
# plot 'DR21(OH)-HCN14MHz.dat' w histeps lt -1

# set out 'DR21-West.ps'
# set title 'DR21-West-HCN14MHz - 15.10.2010 - HCN(1-0)'
# plot 'DR21-West-HCN14MHz.dat' w histeps lt -1

# set out 'H05480+2545.ps'
# set title 'H05480+2545-HCN14MHz - Date - HCN(1-0)'
# plot 'H05480+2545-HCN14MHz.dat' w histeps lt -1

# set out 'IRAS05373+2349.ps'
# set title 'IRAS05373+2349-HCN14MHz - Date - HCN(1-0)'
# plot 'IRAS05373+2349-HCN14MHz.dat' w histeps lt -1

# set out 'S235-HCN14MHz.ps'
# set title 'S235-HCN14MHz - Date - HCN(1-0)'
# plot 'S235-HCN14MHz.dat' w histeps lt -1
