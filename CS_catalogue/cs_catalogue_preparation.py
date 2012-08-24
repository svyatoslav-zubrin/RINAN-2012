#!/usr/bin/env python

import ephem
from math import sqrt

#-----------------------------------------------------------------------------
ERROR_VALUE = -9999

SPATIAL_RESOLUTION_DEFAUL = 10 #arcsec

RT22_NONDETECTED = -1
RT22_UNKNOWN     =  0
RT22_DETECTED    =  1

OTHER_NONDETECTED = -1
OTHER_UNKNOWN     =  0
OTHER_DETECTED    =  1

#-----------------------------------------------------------------------------
# Base classes
#-----------------------------------------------------------------------------
class Coordinates(object):
    """Coordinates of the astronomical source"""
    def __init__(self, coordinates_source, source_type="fft_string"):
        if (source_type != "list_galactic"):
            if (source_type == "list_equat"):
                # coordinates
                ra_h = coordinates_source[0]
                ra_m = coordinates_source[1]
                ra_s = coordinates_source[2]
                dec_d = coordinates_source[3]
                dec_m = coordinates_source[4]
                dec_s = coordinates_source[5]
                epoch = coordinates_source[6]
                # popravki
                dra = 0
                dde = 0
            if (source_type == "fft_string"):
                # coordinates
                coordinates_source = coordinates_source.split()
                ra_h = float(coordinates_source[1])
                ra_m = float(coordinates_source[2])
                ra_s = float(coordinates_source[3])
                dec_d = float(coordinates_source[5])
                dec_m = float(coordinates_source[6])
                dec_s = float(coordinates_source[7])
                epoch = coordinates_source[12]
                # popravki
                dra = float(coordinates_source[9])
                dde = float(coordinates_source[11])
            # convert to ephem style coordinates 
            ra_string  = str(ra_h)+":"+str(ra_m)+":"+str(ra_s)
            dec_string = str(dec_d)+":"+str(dec_m)+":"+str(dec_s)
            if epoch == "1950":
                self.coord1950 = ephem.Equatorial(ra_string, dec_string, epoch=ephem.B1950)
                self.coord2000 = ephem.Equatorial(self.coord1950, epoch=ephem.J2000)
            else:
                self.coord2000 = ephem.Equatorial(ra_string, dec_string, epoch=ephem.J2000)
                self.coord1950 = ephem.Equatorial(self.coord2000, epoch=ephem.B1950)
        else:
            # coordinates
            self.gal_lon = coordinates_source[0]
            self.gal_lat = coordinates_source[1]

            # popravki
            self.dra = 0
            self.dde = 0
            coord_gal = ephem.Galactic(str(self.gal_lon), str(self.gal_lat))
            self.coord1950 = ephem.Equatorial(coord_gal, epoch=ephem.B1950)
            self.coord2000 = ephem.Equatorial(coord_gal, epoch=ephem.J2000)

    def description(self):
        ra_list  = str(self.coord2000.ra).split(":")
        dec_list = str(self.coord2000.dec).split(":")
        # desc_string = str(self.coord2000.ra)+' '+str(self.coord2000.dec)
        # desc_string = "%2.0f %2.0f %5.2f    %2.0f %2.0f %5.2f    %s" % (ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch)
        desc_string = "%2.0f %2.0f %5.2f    %+2.0f %2.0f %5.2f    %s" % (float(ra_list[0]), float(ra_list[1]), float(ra_list[2]), \
                                                                        float(dec_list[0]), float(dec_list[1]), float(dec_list[2]), "2000")
        return desc_string

    def isIdenticalWithCoordinates(self, coordinates, accuracy_arcmin=3):
        ra1  = float(self.coord2000.ra)*180.0/ephem.pi
        dec1 = float(self.coord2000.dec)*180.0/ephem.pi
        ra2  = float(coordinates.coord2000.ra)*180.0/ephem.pi
        dec2 = float(coordinates.coord2000.dec)*180.0/ephem.pi
        dist_deg = sqrt((ra1-ra2)*(ra1-ra2) + (dec1-dec2)*(dec1-dec2))
        accuracy_deg = accuracy_arcmin/60.0
        if (dist_deg <= accuracy_deg):
            return True
        else:
            return False


#-----------------------------------------------------------------------------
class Source(object):
    """Base class for all types of astronomical sources"""
    def __init__(self, name, coordinates, author):  
        super(Source, self).__init__()
        self.name = name
        self.coordinates = coordinates
        self.author_name = author

    def isNameIdeticalWithSource(self, source):
        if (self.name == source.name):
            return True
        else:
            return False


#-----------------------------------------------------------------------------
# Maser operations
#-----------------------------------------------------------------------------
class MMResult(object):
    """ Results of methanol spectrul line approximation """
    def __init__(self, vlsr, flux, linewidth=ERROR_VALUE):
        """
        """
        self.vlsr = vlsr
        self.flux = flux
        self.linewidth = linewidth


class MMaser(Source):
    """Methanol maser information"""
    def __init__(self, name, coordinates, flux, mclass, velocity, irasname, author):
        super(MMaser, self).__init__(name, coordinates, author)
        self.flux = flux
        self.mclass = mclass
        self.velocity = velocity
        self.irasname = irasname
        # maser spectral lines parameters (can be more than one line for a maser)
        self.multiple_sectral_lines = False
        self.spectral_lines = []
        # if maser has spatially unresolved maser sources of other type
        self.has_unresolved_sources = False
        self.unresolved_sources = []
        # if maser was observed in CS with third-party telescope
        self.other_cs_results = []
        self.otherDetectionMark = OTHER_UNKNOWN;
        # if maser was observed in CS(2-1) on the RT22 telescope
        self.our_cs_results = []
        self.rt22DetectionMark = RT22_UNKNOWN;

    def addMMResult(self, result):
        """
        """
        self.spectral_lines.append(result)
        self.multiple_sectral_lines = True

    def addOurCS(self, our_cs_result):
        self.our_cs_results.append(our_cs_result)

    def addThirdpartyCS(self, cs_results):
        self.other_cs_results.append(cs_results)

    def addSpatiallyUnresolvedSource(self, source):
        self.unresolved_sources.append(source)
        self.has_unresolved_sources = True
        
    def description(self):
        desc_string = self.name + "\t" + \
            self.coordinates.description() + "\t"
        if (self.multiple_sectral_lines == False):
            desc_string += \
            str(self.velocity) + "\t" + \
            self.author_name + "\t" + \
            str(self.flux) + "\t" + \
            self.mclass + "\t" + \
            self.irasname + "\t"
        else:
            for line in self.spectral_lines:
                desc_string += "%6.2f %6.2f %5.2f " % (line.vlsr, line.flux, line.linewidth)
        if (len(self.unresolved_sources) > 0):
            for source in self.unresolved_sources:
                desc_string += source.name + "\t"
        if (len(self.cs_results) > 0):
            for source in self.cs_results:
                desc_string += source.description() + "\t"
        if (len(self.our_cs_results) > 0):
            for result in self.our_cs_results:
                desc_string += source.description() + "\t"
        return desc_string
    
    def observationalCatalogueItem(self):
        if (self.multiple_sectral_lines == False):
            # name and parameters of maser
            if self.velocity == ERROR_VALUE:
                return ""
            desc_string = "%15.15s    %s   " % (self.name, self.coordinates.description())
            desc_string += "%8.2f  %8.2f          |%s|  " % (self.velocity, self.flux, self.author_name)
            # rt22 observations mark
            #if ((self.our_cs_observed == True) & (self.our_cs_detected == False)):
            #    desc_string += "n   |  "
            #elif ((self.our_cs_observed == True) & (self.our_cs_detected == True)):
            #    desc_string += "y   |  "
            #else:
            #    desc_string += "-   |  "
            if (self.rt22DetectionMark == RT22_NONDETECTED):
                desc_string += "n  |  "
            elif (self.rt22DetectionMark == RT22_DETECTED):
                desc_string += "y  |  "
            else:
                desc_string += "-  |  "
            # third-party observations mark 
            if (len(self.other_cs_results) > 0): #TODO: not working
                desc_string += "y  |  "
            else:
                desc_string += "n  |  "
            # unresolved maser sources from other catalogues
            if (self.has_unresolved_sources == True):
                for unres_source in self.unresolved_sources:
                    desc_string += "%s  " % (unres_source.name)
        else:
            # name and parameters of maser
            desc_string = "multi:\n"
            for line in self.spectral_lines:
                desc_string += "%15.15s    %s   " % (self.name, self.coordinates.description())
                desc_string += "%8.2f  %8.2f  %5.2f   |%s|  " % (line.vlsr, line.flux, line.linewidth, self.author_name)
                # rt22 observations mark
                if (self.rt22DetectionMark == RT22_NONDETECTED):
                    desc_string += "n  |  "
                elif (self.rt22DetectionMark == RT22_DETECTED):
                    desc_string += "y  |  "
                else:
                    desc_string += "-  |  "
                # third-party observations mark
                if (len(self.other_cs_results) > 0): # TODO: not working
                    desc_string += "y  |  "
                else:
                    desc_string += "n  |  "
                # unresolved maser sources from other catalogues
                if (self.has_unresolved_sources == True):
                    for unres_source in self.unresolved_sources:
                        desc_string += "%s  " % (unres_source.name)
                desc_string += "\n"
        return desc_string
    
    def markAsRT22Detected(self):
        self.rt22DetectionMark = RT22_DETECTED;
        
    def markAsRT22Nondetected(self):
        self.rt22DetectionMark = RT22_NONDETECTED;
        
    def markAsOtherDetected(self):
        self.otherDetectionMark = OTHER_DETECTED;
        
    def markAsOtherNondetected(self):
        self.otherDetectionMark = OTHER_NONDETECTED;
        
    def selectAppropriateCSObservations(self, cs_catalogues):
        for catalogue in cs_catalogues:
            for source in catalogue:
                if (source.coordinates.isIdenticalWithCoordinates(self.coordinates)):
                    self.addThirdpartyCS(source)
        return

def preparePestalozzi():
    filename = "./catalogues/pestalozzi.catalogue"
    sourcesInitStringNumber = 106
    sourcesFinlStringNumber = 624

    masersFile = open(filename, 'r')
    masersList = masersFile.readlines()
    pestalozziMasers = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        sourcename = masersList[i][31:43]
        ra_h = float(masersList[i][44:46])
        ra_m = float(masersList[i][47:49])
        ra_s = float(masersList[i][50:56])
        dec_d = float(masersList[i][57:60])
        dec_m = float(masersList[i][61:63])
        dec_s = float(masersList[i][64:69])
        epoch = "2000"
        flux = float(masersList[i][107:114])
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        vlsr = float(masersList[i][86:92])
        irasname = masersList[i][132:142]
        maserSource = MMaser(sourcename, coordinates, flux, "IIclass", vlsr, irasname, "pest")
        pestalozziMasers.append(maserSource)
        # print maserSource.description()
    return pestalozziMasers


def prepareValttz():
    filename = "./catalogues/valtts.catalogue"
    sourcesInitStringNumber = 98
    sourcesFinlStringNumber = 257

    masersFile = open(filename, 'r')
    masersList = masersFile.readlines()
    valttzMasers = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # names
        sourcename = "VALTTZ_" + str(i)
        irasname = masersList[i][120:131]
        # coordinates
        ra_h = float(masersList[i][0:2])
        ra_m = float(masersList[i][3:5])
        ra_s = float(masersList[i][6:11])
        dec_d = float(masersList[i][12:15])
        dec_m = float(masersList[i][16:18])
        dec_s = float(masersList[i][19:23])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        # flux
        flux_string = masersList[i][99:105] 
        if flux_string != "      ":
            flux = float(flux_string)
        else:
            flux = ERROR_VALUE
        # vlsr
        vlsr_string = masersList[i][108:114]
        # print "\"" + vlsr_string + "\"" 
        if vlsr_string != "      ":
            vlsr = float(vlsr_string)
        else:
            vlsr = ERROR_VALUE
        maserSource = MMaser(sourcename, \
            coordinates, \
            flux, " Iclass", \
            vlsr, \
            irasname, "valt")
        valttzMasers.append(maserSource)
        # print maserSource.description()
    return valttzMasers


def prepareChen():
    filename = "./catalogues/chen.catalogue"
    sourcesInitStringNumber = 90
    sourcesFinlStringNumber = 282
    resultsInitStringNumber = 305
    resultsFinlStringNumber = 641

    masersFile = open(filename, 'r')
    masersList = masersFile.readlines()
    for i in range(len(masersList)):
        masersList[i] = masersList[i].split()
    chenMasers = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # names
        sourcename = masersList[i][6]
        # coordinates
        ra_h = float(masersList[i][0])
        ra_m = float(masersList[i][1])
        ra_s = float(masersList[i][2])
        dec_d = float(masersList[i][3])
        dec_m = float(masersList[i][4])
        dec_s = float(masersList[i][5])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        # temporary values
        irasname = "NO_IRAS"
        flux = ERROR_VALUE
        vlsr = ERROR_VALUE
        
        maserSource = MMaser(sourcename, \
            coordinates, \
            flux, " Iclass", \
            vlsr, \
            irasname, "chen")
        chenMasers.append(maserSource)

    # results (can be more than one result for single source)   
    for i in range(resultsInitStringNumber, resultsFinlStringNumber):
        sourcename = masersList[i][0]
        source = [source for source in chenMasers if source.name == sourcename]
        flux = float(masersList[i][1])
        vlsr = float(masersList[i][3])
        linewidth = float(masersList[i][5])
        chenResult = MMResult(vlsr, flux, linewidth)
        source[0].addMMResult(chenResult)
        
    # printing for test
    # for maser in chenMasers:
    #     print maser.description()

    return chenMasers


def findCataloguesIntersection(sourcesList1, sourcesList2, spatial_resolution_arcsec=SPATIAL_RESOLUTION_DEFAUL):
    for source1 in sourcesList1:
        for source2 in sourcesList2:
            if (source1.coordinates.isIdenticalWithCoordinates(source2.coordinates, spatial_resolution_arcsec/60.0)):
                source1.addSpatiallyUnresolvedSource(source2)
                source2.addSpatiallyUnresolvedSource(source1)
                # print source1.description()


#-----------------------------------------------------------------------------
# Third-party CS observations operations
#-----------------------------------------------------------------------------

class CSResult(object):
    """Unique result of CS observations (spectrl parameters of the line)"""
    def __init__(self, velocity, linewidth, temperature):
        super(CSResult, self).__init__()
        self.velocity = velocity
        self.linewidth = linewidth
        self.temperature = temperature


class CSSource(Source):
    """Base class for all third-party observations"""
    def __init__(self, name, coordinates, author, irasname = ""):
        super(CSSource, self).__init__()
        self.irasname = irasname
        self.cs_results = []
        
    def addCSResult(self, result):
        self.cs_results.append(result)
        return

    def description(self):
        desc_string = "%+6.1f %4.1f %4.1f" % (self.velocity, self.temperature, self.linewidth)
        return desc_string + "   "

#-----------------------------------------------------------------------------

class BronfmanSource(CSSource):
    """docstring for BronfmanSource"""
    def __init__(self, name, coordinates, author, irasname = ""):
        super(BronfmanSource, self).__init__(name, coordinates, author, irasname)
        
    def description(self):
        desc_string = self.author_name + "__" + self.name + " " + str(self.temperature) + " " + self.irasname
        return desc_string


def prepareBronfman():
    filename = "bronfman.catalogue"
    sourcesInitStringNumber = 55
    sourcesFinlStringNumber = 1504

    csFile = open(filename, 'r')
    csList = csFile.readlines()
    bronfmanSources = []
    j = 1 # numeration in Brinfman catalogue starts from 1
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # Names
        sourcename = "BRONFMAN_" + str(j)
        irasname = csList[i][42:53]
        # Coordinates
        gal_lon = float(csList[i][9:16])
        gal_lat = float(csList[i][17:23])
        coordinates = Coordinates([gal_lon, gal_lat], "list_galactic")
        # Brightness temperature
        temperature_string = csList[i][31:36] 
        if temperature_string != "     ":
            temperature = float(temperature_string)
        else:
            temperature = ERROR_VALUE
        # Velocity
        velocity_string = csList[i][32:37] 
        if velocity_string != "     ":
            velocity = float(velocity_string)
        else:
            velocity = ERROR_VALUE
        # Linewidth
        linewidth_string = csList[i][37:41] 
        if linewidth_string != "    ":
            linewidth = float(linewidth_string)
        else:
            linewidth = ERROR_VALUE
        bronfmanSource = BronfmanSource(sourcename, coordinates, "bron", irasname)
        cs_result = CSResult(velocity, linewidth, temperature)
        bronfmanSource.addCSResult(cs_result)
        bronfmanSources.append(bronfmanSource)
        j += 1
        # print bronfmanSource.description()
    return bronfmanSources


#-----------------------------------------------------------------------------
# class BeutherCSResult(object):
#     """docstring for beutherCSResult"""
#     def __init__(self, velocity, temperature, linewidth):
#         super(BeutherCSResult, self).__init__()
#         self.velocity = velocity
#         self.temperature = temperature
#         self.linewidth = linewidth

#     def description(self):
#         desc_string = "%+6.1f %4.1f %4.1f" % (self.velocity, self.temperature, self.linewidth)
#         return desc_string + "   "
        
class BeutherSource(CSSource):
    """Beuther CS observations result (stored in beuther.catalogue)"""
    def __init__(self, name, coordinates, author, irasname):
        super(BeutherSource, self).__init__(name, coordinates, author, irasname)

    def description(self):
        desc_string = self.name + "\t" + self.coordinates.description() + "\t" + self.irasname + "\t"
        cs_results_sorted = sorted(self.cs_results, key=lambda result: result.velocity)
        for result in cs_results_sorted:
            desc_string += result.description()
        return desc_string


def prepareBeuther():
    filename = "beuther.catalogue"
    sourcesInitStringNumber = 99
    sourcesFinlStringNumber = 168
    resultsInitStringNumber = 376
    resultsFinlStringNumber = 469

    # sources
    csFile = open(filename, 'r')
    csList = csFile.readlines()
    beutherSources = []
    j = 0 # there is no numeration in Beuther catalogue. Starts from 0
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # Names
        sourcename = "BEUTHER_" + str(j)
        irasname = csList[i][0:10]
        # Coordinates
        ra_h = float(csList[i][11:13])
        ra_m = float(csList[i][14:16])
        ra_s = float(csList[i][16:21])
        dec_d = float(csList[i][22:25])
        dec_m = float(csList[i][26:28])
        dec_s = float(csList[i][29:31])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        # Velocity
        velocity_string = csList[i][32:37] 
        # print "\""+ velocity_string + "\""
        if velocity_string != "      ":
            velocity = float(velocity_string)
        else:
            velocity = ERROR_VALUE
        beutherSource = BeutherSource(sourcename, coordinates, "beut", irasname)
        beutherSources.append(beutherSource)
        j += 1
        
    # results (can be more than one result for single source)   
    for i in range(resultsInitStringNumber, resultsFinlStringNumber):
        irasname = csList[i][0:10]
        source = [source for source in beutherSources if source.irasname == irasname]
        velocity = float(csList[i][13:18])
        temperature = float(csList[i][19:23])
        linewidth = float(csList[i][24:28])
        cs_result = CSResult(velocity, linewidth, temperature)
        source[0].addCSResult(cs_result)

    # # printing for test
    # for source in beutherSources:
    #     print source.description()

    csFile.close()
    return beutherSources


#-----------------------------------------------------------------------------
class LarionovSource(CSSource):
    """docstring for LarionovSource"""
    def __init__(self, name, coordinates, author, irasname=""):
        super(LarionovSource, self).__init__(name, coordinates, author, irasname)
        # self.cs_detected = False
        # self.temperature = temperature
        # self.temperatureIntegrated = temperatureIntegrated
        # self.velocity    = velocity
        # self.linewidth   = linewidth
        # if self.temperature != ERROR_VALUE:
        #     self.cs_detected = True;
        
    def description(self):
        desc_string = self.author_name + "__" + self.name + " " + str(self.temperatureIntegrated)
        return desc_string


def prepareLarionov():
    filename = "larionov_data_new.txt"
    sourcesInitStringNumber = 3
    sourcesFinlStringNumber = 154

    csFile = open(filename, 'r')
    csList = csFile.readlines()
    larionovSources = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        csList[i] = csList[i].split()
        # Names
        sourcename = csList[i][0]
        # Coordinates
        ra_h = float(csList[i][1])
        ra_m = float(csList[i][2])
        ra_s = float(csList[i][3])
        dec_d = float(csList[i][4])
        dec_m = float(csList[i][5])
        dec_s = float(csList[i][6])
        epoch = "1950"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        # Antenna temperature
        temperature_string = csList[i][14] 
        temperature = float(temperature_string)
        # Integrated temperature
        integrated_temperature_string = csList[i][14] 
        integrated_temperature = float(integrated_temperature_string)
        # Velocity
        velocity_string = csList[i][10] 
        velocity = float(velocity_string)
        # Linewidth
        linewidth_string = csList[i][12] 
        linewidth = float(linewidth_string)
        # source treatment
        larionovSource = LarionovSource(sourcename, coordinates, "lari")
        cs_result = CSResult(velocity, linewidth, temperature)
        larionovSource.addCSResult(cs_result)
        larionovSources.append(larionovSource)
        # print larionovSource.description()

    csFile.close()
    return larionovSources

#-----------------------------------------------------------------------------
# Our CS observations operations
#-----------------------------------------------------------------------------
class OurCSSource(Source):
    """Class contains data of our observations of methanol masers in CS(2-1)"""
    def __init__(self, name, coordinates, temperature, observational_date, observational_time):
        super(OurCSSource, self).__init__(name, coordinates)
        self.temperature = temperature
        self.observational_date = observational_date
        self.observational_time = observational_time

    def description(self):
        desc_string = self.author_name + "__" + self.name + " " + self.temperature
        return desc_string



class OurDetection(Source):
    """docstring for OurDetection"""
    def __init__(self, name, recno, year, coordinates, author, elev, antena_temperature, velocity, linewidth, rms):
        super(OurDetection, self).__init__(name, coordinates, author)
        self.recno = recno
        self.year = year
        self.elevation = elev
        self.antena_temperature = antena_temperature
        self.velocity = velocity
        self.linewidth = linewidth
        self.rms = rms
        
    def description(self):
        return self.name + "\t" + str(self.antena_temperature) + "\t" + str(self.rms)



class OurNondetection(Source):
    """docstring for OurNondetection"""
    def __init__(self, name, recno, coordinates, author, rms):
        super(OurNondetection, self).__init__(name, coordinates, author)
        self.recno = recno
        self.rms = rms
        
    def description(self):
        return self.name + "\t" + str(self.rms)



class R22(object):
    """docstring for R22"""
    def __init__(self, filename):
        super(R22, self).__init__()
        self.filename = filename
        r22_file = open(self.filename, 'r')
        r22_content = r22_file.readlines()
        self.sourcename = (r22_content[1].split())[0]
        self.coordinates = Coordinates(r22_content[3])
        self.source_ID = self.sourcename + "_" + self.coordinates.description()


#-----------------------------------------------------------------------------
def prepareCSObservations():
    filename = "search.txt"
    fileWithList = open(filename, 'r')
    filelist = fileWithList.readlines()
    all_cs_data = []
    for observational_filename in filelist:
        observ_result = open(observational_filename[0:-2], 'r')
        observ_result_data = observ_result.readlines()
        # FIXME: right file type detection
        if (observational_filename[-3] == "2"): # r22-file 
            r22_cs_data = R22(observational_filename[0:-2])
            all_cs_data.append(r22_cs_data)
        else:
            print "ERROR: Wrong file type (not R22 file)!"

def prepareCSObservationsResults(): 
    pass

def prepareOurDetections():
    filename = "./rt22/our_detections.txt"
    f = open(filename, 'r')
    detectionsList = f.readlines()
    ourDetections = []
    for i in range(len(detectionsList)):
        detectionsList[i] = detectionsList[i].split()
        name = detectionsList[i][2]
        irasname = detectionsList[i][0]
        ra_h = float(detectionsList[i][5])
        ra_m = float(detectionsList[i][6])
        ra_s = float(detectionsList[i][7])
        dec_d = float(detectionsList[i][8])
        dec_m = float(detectionsList[i][9])
        dec_s = float(detectionsList[i][10])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        elevation = detectionsList[i][11]
        year  = int(detectionsList[i][4])
        recno = int(detectionsList[i][3]) # recno from pestalozzi catalogue
        tempr = float(detectionsList[i][16])
        vlsr  = float(detectionsList[i][17])
        linewidth = float(detectionsList[i][18])
        rms = float(detectionsList[i][19])
        our_detection = OurDetection(name, recno, year, coordinates, "shulga", elevation, tempr, vlsr, linewidth, rms)
        ourDetections.append(our_detection)
        # print our_detection.description()
    return ourDetections

def prepareOurNondetections():
    filename = "./rt22/our_nondetections.txt"
    f = open(filename, 'r')
    nondetectionsList = f.readlines()
    ourNondetections = []
    for i in range(len(nondetectionsList)):
        nondetectionsList[i] = nondetectionsList[i].split()
        name  = nondetectionsList[i][2]
        ra_h  = float(nondetectionsList[i][4])
        ra_m  = float(nondetectionsList[i][5])
        ra_s  = float(nondetectionsList[i][6])
        dec_d = float(nondetectionsList[i][7])
        dec_m = float(nondetectionsList[i][8])
        dec_s = float(nondetectionsList[i][9])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_d, dec_m, dec_s, epoch], "list_equat")
        recno = int(nondetectionsList[i][3]) # recno from pestalozzi catalogue
        rms = float(nondetectionsList[i][14])
        our_nondetection = OurNondetection(name, recno, coordinates, "shulga", rms)
        ourNondetections.append(our_nondetection)
        # print our_nondetection.description()
    return ourNondetections

#-----------------------------------------------------------------------------

def setMarkForR22Observations(masers, detections, nondetections, spatial_resolution_arcsec=10):
    for maser in masers:
        for detection in detections:
            if (maser.coordinates.isIdenticalWithCoordinates(detection.coordinates, spatial_resolution_arcsec/60.0)):
                maser.markAsRT22Detected()
    for maser in masers:
        for nondetection in nondetections:
            if (maser.coordinates.isIdenticalWithCoordinates(nondetection.coordinates, spatial_resolution_arcsec/60.0)):
                maser.markAsRT22Nondetected()
    return

def setMarkForOtherObservations(masers, other_cs_catalogues, spatial_resolution_arcsec=10):
    for cs_catalogue in other_cs_catalogues:
        for detection in cs_catalogue:
            for maser in masers:
                if (maser.coordinates.isIdenticalWithCoordinates(detection.coordinates, spatial_resolution_arcsec/60.0)):
                    maser.markAsOtherDetected()
    return

#-----------------------------------------------------------------------------

def selectCSResultsForMasers(cs_results_list, masers_list):
    for masers in masers_list:
        for maser in masers:
            maser.selectAppropriateCSObservations(cs_results_list)
    return

#-----------------------------------------------------------------------------
# Main programm logic
#-----------------------------------------------------------------------------
def prepareMaserCatalogsForObservations2012():
    # prepare lists of masers
    pestalozziList = preparePestalozzi()
    valttsList     = prepareValttz()
    chenList       = prepareChen()
    findCataloguesIntersection(pestalozziList, valttsList)
    findCataloguesIntersection(pestalozziList, chenList)
    findCataloguesIntersection(valttsList, chenList)

    # # prepare third-party CS observations lists
    # bronfmanList   = prepareBronfman()
    # beutherList    = prepareBeuther()
    # larionovList   = prepareLarionov()

    # prepare our CS observations lists
    # ourObservationsList = prepareCSObservations()
    ourDetectionsList   = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()

    # step-by-step comparison of obtained lists
    
    # create catalogues for observations in 2012:
    #   - compare every of maser catalogues with our-detection
    
    #   - compare every of maser catalogues with our-nondetections
    #   - select maser sources within nothern hemisphere
    #   - print every maser catalogue with info about our CS results and other MM (names)

    
    # create catalogue for 2012 observational session
    # --- mark rt22 CS observations
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(valttsList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(chenList, ourDetectionsList, ourNondetectionList)
    # --- mark third-party CS observations
    # setMarkForOtherObservations()
    # --- pestalozzi catalogue
    for maser in pestalozziList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
    # --- valtts catalogue
    for maser in valttsList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
    # --- chen catalogue
    for maser in chenList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
        

def prepareMaserTableForObservations2012():
    # prepare lists of masers
    pestalozziList = preparePestalozzi()
    valttsList     = prepareValttz()
    chenList       = prepareChen()
    findCataloguesIntersection(pestalozziList, valttsList)
    findCataloguesIntersection(pestalozziList, chenList)
    findCataloguesIntersection(valttsList, chenList)

    # # prepare third-party CS observations lists
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()

    # prepare our CS observations lists
    # ourObservationsList = prepareCSObservations()
    ourDetectionsList   = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()

    # step-by-step comparison of obtained lists
    
    # create catalogues for observations in 2012:
    #   - compare every of maser catalogues with our-detection
    
    #   - compare every of maser catalogues with our-nondetections
    #   - select maser sources within nothern hemisphere
    #   - print every maser catalogue with info about our CS results and other MM (names)

    # create catalogue for 2012 observational session

    # --- select third-party CS observations
    masers_list = [pestalozziList, valttsList, chenList]
    cs_results_list = [bronfmanList, beutherList, larionovList]
    selectCSResultsForMasers(cs_results_list, masers_list)
    # --- mark r22 CS observations
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(valttsList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(chenList, ourDetectionsList, ourNondetectionList)
    # --- pestalozzi catalogue
    for maser in pestalozziList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
    # --- valtts catalogue
    for maser in valttsList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
    # --- chen catalogue
    for maser in chenList:
        item = maser.observationalCatalogueItem()
        if item != "": 
            print item
        
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    prepareMaserCatalogsForObservations2012()
