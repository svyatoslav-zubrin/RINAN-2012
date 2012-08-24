import pyfits
import numpy
import glob
import pdb
import ephem

def get_R22fit(fitname):
    """ Returns a spectrum from fit-file that was created by FFT.exe (not for GILDAS: popravki - unchecked)

    @param PARAM: fitname - name of the fits-file with data
    @return RETURN: spectr - numpy 2d array [Vlsr, Ta]
    """
    try:
        fhdu = pyfits.open(fitname)       #open a fits file
    except IOError:
        print 'Error: incorrect FITS file name...'
        return 1
    fheader = fhdu[0].header
    fdata = fhdu[0].data
    xrange = fdata.shape[2]
    dv = float(fheader['DELTAV'])*1.0e-3 # [km/s]
    center_vlsr = float(fheader['VLSR'])*1.0e-3 # [km/s]
    center_channel = float(fheader['CRPIX1'])

    spectr = numpy.zeros((xrange,2),'d')
    for i in range(xrange):
        spectr[i,1] = fdata[0,0,i]
        spectr[i,0] = -(center_channel-i)*dv+center_vlsr

    info = (fheader['OBJECT'],
            fheader['LINE'],
            fheader['DATE_OBS'],
            fheader['UTC'],
            fheader['TELESCOP'],
            fheader['ORIGIN'],
            fheader['CRVAL2'],
            fheader['CRVAL3'],
            fheader['EPOCH'])

    print 'get_RT22fit: OK!'
    return spectr, info

# def main():
#     files = glob.glob('*.FIT')
#     for i in files:
#         spectr, info = get_R22fit(i)
#         name = info[0]+'-'+info[1]+'.dat'
#         out = open(name, 'w')
#         for j in spectr:
#             out.write(str(j[0])+' '+str(j[1])+'\n')
#         out.close()
#     # spectr, info = get_R22fit(files[0])
#     # print spectr[0,1]
#     return 0


# def stat(infile, outfile):
#     # data reading
#     input = open(infile, 'r')
#     text = input.readlines()
#     for i in range(len(text)):
#         text[i] = text[i].split()
#     source_number = len(text)/13
#     result = []
#     tmp = []
#     for i in range(source_number):
#         print i
#         tmp.append(text[i*13][1]) # source name
#         tmp.append(text[i*13+6][1]) # y0
#         tmp.append(text[i*13+6][2]) # y0_error
#         tmp.append(text[i*13+7][1]) # V0
#         tmp.append(text[i*13+7][2]) # V0_error
#         tmp.append(text[i*13+8][1]) # w
#         tmp.append(text[i*13+8][2]) # w_error
#         tmp.append(text[i*13+9][1]) # a0
#         tmp.append(text[i*13+9][2]) # a0_error
#         tmp.append(text[i*13+10][1]) # a_left
#         tmp.append(text[i*13+10][2]) # a_left_error
#         tmp.append(text[i*13+11][1]) # a_right
#         tmp.append(text[i*13+11][2]) # a_right_error
#         result.append(tmp)
#         tmp = []
#     # output in file
#     output = open(outfile, 'wn')
#     for i in result:
#         strng = ''
#         for j in range(13):
#             strng = strng + i[j] + ' '
#         output.write(strng+'\n')
#     output.close()
#     return result

    
# def main():
#     infile = 'stat_good.txt'
#     outfile = 'stat_good.dat'
#     stat(infile, outfile)
#     return 0


def main():

    # Read all the *.FIT files in current directory ,
    # get from them some data and put it into file. 
    # Every string i file formatted like this one:
    #     source_name epoch_of_observtions ra dec

    files = glob.glob('*.FIT')
    out = open('table_good.txt', 'wn')
    for i in files:
        spectr, info = get_R22fit(i)
        if info[8] != '2000':
            equat_init = ephem.Equatorial(str(ephem.hours(info[6]*ephem.pi/180.0)), str(ephem.degrees(info[7]*ephem.pi/180.0)), epoch=str(info[8]))
            equat_fin = ephem.Equatorial(equat_init, epoch=ephem.J2000)
        out.write(info[0]+' '+info[2]+' '+str(equat_fin.ra)+' '+str(equat_fin.dec)+'\n')
    out.close()
    return 0

    
main()
