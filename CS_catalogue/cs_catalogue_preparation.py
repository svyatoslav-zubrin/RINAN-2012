#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ephem
# import pdb

#-----------------------------------------------------------------------------
ERROR_VALUE = -9999

SPATIAL_RESOLUTION_MASER_TO_MASER = 10  # arcsec
SPATIAL_RESOLUTION_CS_TO_MASER = 60  # arcsec


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
                dec_sign = coordinates_source[3]
                dec_d = coordinates_source[4]
                dec_m = coordinates_source[5]
                dec_s = coordinates_source[6]
                epoch = coordinates_source[7]
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
                # dra = float(coordinates_source[9])
                # dde = float(coordinates_source[11])
            # convert to ephem style coordinates
            ra_string = str(ra_h)+":"+str(ra_m)+":"+str(ra_s)
            dec_string = dec_sign + str(dec_d)+":"+str(dec_m)+":"+str(dec_s)
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
        ra_list = str(self.coord2000.ra).split(":")
        dec_list = str(self.coord2000.dec).split(":")
        desc_string = "%2.0f %2.0f %5.2f    %+3.0f %2.0f %5.2f    %s" % (float(ra_list[0]), float(ra_list[1]), float(ra_list[2]), \
                                                                        float(dec_list[0]), float(dec_list[1]), float(dec_list[2]), "2000")
        return desc_string

    def isIdenticalWithCoordinates(self, coordinates, accuracy_arcmin):
        angular_separation_rad = ephem.separation([coordinates.coord2000.ra, coordinates.coord2000.dec], [self.coord2000.ra, self.coord2000.dec])
        accuracy_rad = 2.0 * ephem.pi * accuracy_arcmin / (360.0 * 60.0)
        # print "separation: %f radian" % (accuracy_rad)
        if (angular_separation_rad > accuracy_rad):
            return False
        else:
            return True


#-----------------------------------------------------------------------------
# Base class
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


#-------------------------------------------------------------`----------------
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
        self.other_cs_sources = []
        self.otherDetectionMark = OTHER_UNKNOWN
        self.isOtherResultPositive = False
        # if maser was observed in CS(2-1) on the RT22 telescope
        self.our_cs_results = []
        self.rt22DetectionMark = RT22_UNKNOWN

    def addMMResult(self, result):
        """
        """
        self.spectral_lines.append(result)
        self.multiple_sectral_lines = True

    def addOurCS(self, our_cs_result):
        self.our_cs_results.append(our_cs_result)

    def addThirdpartyCS(self, cs_source):
        print "add 3party"
        self.other_cs_sources.append(cs_source)
        if cs_source.isCSDetectionPositive is True:
            self.isOtherResultPositive = True

    def addSpatiallyUnresolvedSource(self, source):
        self.unresolved_sources.append(source)
        self.has_unresolved_sources = True

    def description(self):
        desc_string = self.name + "\t" + \
            self.coordinates.description() + "\t"
        if self.multiple_sectral_lines is False:
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
        # if (len(self.cs_results) > 0):
        #     for source in self.cs_results:
        #         desc_string += source.description() + "\t"
        if (len(self.our_cs_results) > 0):
            for result in self.our_cs_results:
                desc_string += source.description() + "\t"
        return desc_string

    def observationalCatalogueItem(self):
        if self.multiple_sectral_lines is False:
            # name and parameters of maser
            if self.velocity == ERROR_VALUE:
                return ""
            desc_string = "%15.15s    %s   " % (self.name, self.coordinates.description())
            desc_string += "%8.2f  %8.2f          |%s|  " % (self.velocity, self.flux, self.author_name)
            # rt22 observations mark
            if (self.rt22DetectionMark == RT22_NONDETECTED):
                desc_string += "n  |  "
            elif (self.rt22DetectionMark == RT22_DETECTED):
                desc_string += "y  |  "
            else:
                desc_string += "-  |  "
            # third-party observations mark
            if ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is True)):
                desc_string += "y  |  "
            elif ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is False)):
                desc_string += "n  |  "
            else:
                desc_string += "-  |  "
            # need further observations
            # maser need further observations if:
            # - there is no previous CS observations
            # - there is no CS observations of the other authors
            # - maser line placed apart from the CS spectral line (for other authors' observations)
            hasR22CSObservations = (self.rt22DetectionMark != RT22_UNKNOWN)
            hasCrossedLines = False
            for source in self.other_cs_sources:
                if (not(self.isSourceNeedFurtherObservations(source))):
                    hasCrossedLines = True
            if (hasCrossedLines | hasR22CSObservations):
                desc_string += "n  |  "
            else:
                desc_string += "y  |  "
            # unresolved maser sources from other catalogues
            if self.has_unresolved_sources is True:
                for unres_source in self.unresolved_sources:
                    desc_string += "%s  " % (unres_source.name)
            # end string
            desc_string += '\n'
        else:
            # name and parameters of maser
            desc_string = "source:\n"
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
                if ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is True)):
                    desc_string += "y  |  "
                elif ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is False)):
                    desc_string += "n  |  "
                else:
                    desc_string += "-  |  "
                # need further observations mark
                # maser need further observations if:
                # - there is no previous CS observations
                # - there is no CS observations of the other authors
                # - maser line placed apart from the CS spectral line (for other authors' observations)
                hasR22CSObservations = (self.rt22DetectionMark != RT22_UNKNOWN)
                hasCrossedLines = False
                for source in self.other_cs_sources:
                    if (not(self.isSourceNeedFurtherObservations(source))):
                        hasCrossedLines = True
                if (hasCrossedLines | hasR22CSObservations):
                    desc_string += "n  |  "
                else:
                    desc_string += "y  |  "
                # unresolved maser sources from other catalogues
                if self.has_unresolved_sources is True:
                    for unres_source in self.unresolved_sources:
                        desc_string += "%s  " % (unres_source.name)

                desc_string += "\n"
        return desc_string

    def observationalTableItem(self):
        if self.multiple_sectral_lines is False:
            # name and parameters of maser
            if self.velocity == ERROR_VALUE:
                return ""
            desc_string = "maser %24s    %s   " % (self.name, self.coordinates.description())
            desc_string += "F(%8.2f)  Vlsr(%+8.2f)              |%s|  " % (self.flux, self.velocity, self.author_name)
            # rt22 observations mark
            if (self.rt22DetectionMark == RT22_NONDETECTED):
                desc_string += "n  |  "
            elif (self.rt22DetectionMark == RT22_DETECTED):
                desc_string += "y  |  "
            else:
                desc_string += "-  |  "
            # third-party observations mark
            if ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is True)):
                desc_string += "y  |  "
            elif ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is False)):
                desc_string += "n  |  "
            else:
                desc_string += "-  |  "
            # need further observations mark
            # maser need further observations if:
            # - there is no previous CS observations
            # - there is no CS observations of the other authors
            # - maser line placed apart from the CS spectral line (for other authors' observations)
            hasR22CSObservations = (self.rt22DetectionMark != RT22_UNKNOWN)
            hasCrossedLines = False
            for source in self.other_cs_sources:
                if (not(self.isSourceNeedFurtherObservations(source))):
                    hasCrossedLines = True
            if (hasCrossedLines | hasR22CSObservations):
                desc_string += "n  |  "
            else:
                desc_string += "y  |  "
            # unresolved maser sources from other catalogues
            if (self.has_unresolved_sources is True):
                for unres_source in self.unresolved_sources:
                    desc_string += "%s  " % (unres_source.name)
            desc_string += '\n'
            # CS results list
            # rt22 results
            # if (self.rt22DetectionMark != RT22_UNKNOWN):
            if (len(self.our_cs_results) > 0):
                for result in self.our_cs_results:
                    desc_string += '' + result.description() + '\n'
            # third-party results
            if (len(self.other_cs_sources) > 0):
                for cs_source in self.other_cs_sources:
                    desc_string += '' + cs_source.description() + '\n'
        else:
            # name and parameters of maser
            desc_string = "new source:\n"
            for line in self.spectral_lines:
                desc_string += "maser %24s    %s   " % (self.name, self.coordinates.description())
                desc_string += "F(%8.2f)  Vlsr(%+8.2f)  dV(%5.2f)   |%s|  " % (line.flux, line.vlsr, line.linewidth, self.author_name)
                # rt22 observations mark
                if (self.rt22DetectionMark == RT22_NONDETECTED):
                    desc_string += "n  |  "
                elif (self.rt22DetectionMark == RT22_DETECTED):
                    desc_string += "y  |  "
                else:
                    desc_string += "-  |  "
                # third-party observations mark
                if ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is True)):
                    desc_string += "y  |  "
                elif ((len(self.other_cs_sources) > 0) & (self.isOtherResultPositive is False)):
                    desc_string += "n  |  "
                else:
                    desc_string += "-  |  "
                # need further observations mark
                # maser need further observations if:
                # - there is no previous CS observations
                # - there is no CS observations of the other authors
                # - maser line placed apart from the CS spectral line (for other authors' observations)
                hasR22CSObservations = (self.rt22DetectionMark != RT22_UNKNOWN)
                hasCrossedLines = False
                for source in self.other_cs_sources:
                    if (not(self.isSourceNeedFurtherObservations(source))):
                        hasCrossedLines = True
                if (hasCrossedLines | hasR22CSObservations):
                    desc_string += "n  |  "
                else:
                    desc_string += "y  |  "
                # unresolved maser sources from other catalogues
                if (self.has_unresolved_sources is True):
                    for unres_source in self.unresolved_sources:
                        desc_string += "%s  " % (unres_source.name)
                desc_string += "\n"
            # CS results list (after all of the lines)
            # rt22 results
            if (len(self.our_cs_results) > 0):
                for result in self.our_cs_results:
                    desc_string += '' + result.description() + '\n'
            # third-party results
            if (len(self.other_cs_sources) > 0):
                for cs_source in self.other_cs_sources:
                    desc_string += '' + cs_source.description() + '\n'
        desc_string += "\n"
        return desc_string

    def markAsRT22Detected(self):
        self.rt22DetectionMark = RT22_DETECTED

    def markAsRT22Nondetected(self):
        self.rt22DetectionMark = RT22_NONDETECTED

    def markAsOtherDetected(self):
        self.otherDetectionMark = OTHER_DETECTED

    def markAsOtherNondetected(self):
        self.otherDetectionMark = OTHER_NONDETECTED

    def selectAppropriateCSObservations(self, cs_catalogues):
        for catalogue in cs_catalogues:
            for source in catalogue:
                if (source.coordinates.isIdenticalWithCoordinates(self.coordinates, SPATIAL_RESOLUTION_CS_TO_MASER / 60.0)):
                    self.addThirdpartyCS(source)
        return

    def isSourceNeedFurtherObservations(self, cs_source):
        isSpatiallyIdentical = cs_source.coordinates.isIdenticalWithCoordinates(self.coordinates, SPATIAL_RESOLUTION_CS_TO_MASER / 60.0)
        isVelocitiesCovered = False
        for result in cs_source.cs_results:
            if ((self.velocity >= (result.velocity - result.linewidth)) & (self.velocity <= (result.velocity + result.linewidth))):
                isVelocitiesCovered = True
        return not(isVelocitiesCovered & isSpatiallyIdentical)

    def isNothernSource(self):
        if (float(self.coordinates.coord2000.dec) > 0):
            return True
        else:
            return False


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
        dec_sign = masersList[i][57:58]
        dec_d = float(masersList[i][58:60])
        dec_m = float(masersList[i][61:63])
        dec_s = float(masersList[i][64:69])
        epoch = "2000"
        flux = float(masersList[i][107:114])
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        vlsr = float(masersList[i][86:92])
        irasname = masersList[i][132:142]
        maserSource = MMaser(sourcename, coordinates, flux, "IIclass", vlsr, irasname, "M.Pestalozzi(J/A+A/432/737)")
        pestalozziMasers.append(maserSource)
        # print maserSource.description()
    return pestalozziMasers

def prepareValttz():
    filename = "./catalogues/valtts.catalogue"
    sourcesInitStringNumber = 97
    sourcesFinlStringNumber = 257

    masersFile = open(filename, 'r')
    masersList = masersFile.readlines()
    valttzMasers = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # names
        source_id = int(masersList[i][25:32])
        sourcename = "VALTTZ_" + str(source_id)
        irasname = masersList[i][120:131]
        # coordinates
        ra_h = float(masersList[i][0:2])
        ra_m = float(masersList[i][3:5])
        ra_s = float(masersList[i][6:11])
        dec_sign = masersList[i][12:13]
        dec_d = float(masersList[i][13:15])
        dec_m = float(masersList[i][16:18])
        dec_s = float(masersList[i][19:23])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
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
        maserSource = MMaser(sourcename,
            coordinates,
            flux, " Iclass",
            vlsr,
            irasname, "Val'tts(J/AZh/84/579)")
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
        dec_sign = '+'  # there is no sources in catalogue with dec_d = "-00"
        dec_d = float(masersList[i][3])
        dec_m = float(masersList[i][4])
        dec_s = float(masersList[i][5])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        # temporary values
        irasname = "NO_IRAS"
        flux = ERROR_VALUE
        vlsr = ERROR_VALUE

        maserSource = MMaser(sourcename,
            coordinates,
            flux, " Iclass",
            vlsr,
            irasname, "Chen(J/ApJS/196/9)")
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


def findCataloguesIntersection(sourcesList1, sourcesList2, spatial_resolution_arcsec=SPATIAL_RESOLUTION_MASER_TO_MASER):
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
    """Unique result of CS observations (spectral parameters of the line)"""
    def __init__(self, velocity, linewidth, temperature):
        super(CSResult, self).__init__()
        self.velocity = velocity
        self.linewidth = linewidth
        self.temperature = temperature
        self.positiveDetection = False
        if (self.temperature != ERROR_VALUE):
            self.positiveDetection = True

    def description(self):
        desc_string = "T(%8.2f)  Vlsr(%+8.2f)  dV(%4.1f)" % (self.temperature, self.velocity, self.linewidth)
        return desc_string + "   "

    def description_bronfman(self):
        desc_string = "Tmb(%6.2f)  Vlsr(%+8.2f)  dV(%4.1f)" % (self.temperature, self.velocity, self.linewidth)
        return desc_string + "   "

    def description_larionov(self):
        desc_string = "Ta*(%6.2f)  Vlsr(%+8.2f)  dV(%4.1f)" % (self.temperature, self.velocity, self.linewidth)
        return desc_string + "   "


class CSSource(Source):
    """Base class for all third-party observations"""
    def __init__(self, name, coordinates, author, irasname=""):
        super(CSSource, self).__init__(name, coordinates, author)
        self.irasname = irasname
        self.cs_results = []
        self.isCSDetectionPositive = False

    def addCSResult(self, result):
        self.cs_results.append(result)
        if (result.positiveDetection is True):
            self.isCSDetectionPositive = True
        return

    def description(self):
        desc_string = ""
        for item in self.cs_results:
            desc_string += "T(%8.2f)  Vlsr(%+8.2f)  dV(%4.1f)" % (item.temperature, item.velocity, item.linewidth)
        return desc_string + "\n"


#-----------------------------------------------------------------------------
class BronfmanSource(CSSource):
    """docstring for BronfmanSource"""
    def __init__(self, name, coordinates, author, irasname=""):
        super(BronfmanSource, self).__init__(name, coordinates, author, irasname)

    def description(self):
        desc_string = "%30s    %s   " % (self.name, self.coordinates.description())
        cs_results_sorted = sorted(self.cs_results, key=lambda result: result.velocity)
        for result in cs_results_sorted:
            desc_string += result.description_bronfman()
        return desc_string


def prepareBronfman():
    filename = "./catalogues/bronfman.catalogue"
    sourcesInitStringNumber = 55
    sourcesFinlStringNumber = 1504

    csFile = open(filename, 'r')
    csList = csFile.readlines()
    bronfmanSources = []
    j = 1  # numeration in Brinfman catalogue starts from 1
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # Names
        sourcename = "BRONFMAN:" + str(j)
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
        bronfmanSource = BronfmanSource(sourcename, coordinates, "Bronfman(J/A+AS/115/81)", irasname)
        cs_result = CSResult(velocity, linewidth, temperature)
        bronfmanSource.addCSResult(cs_result)
        bronfmanSources.append(bronfmanSource)
        j += 1
        # print bronfmanSource.description()
    return bronfmanSources


#-----------------------------------------------------------------------------
class BeutherSource(CSSource):
    """Beuther CS observations result (stored in beuther.catalogue)"""
    def __init__(self, name, coordinates, author, irasname):
        super(BeutherSource, self).__init__(name, coordinates, author, irasname)

    def description(self):
        desc_string = "%30s    %s   " % (self.name+':'+self.irasname, self.coordinates.description())
        cs_results_sorted = sorted(self.cs_results, key=lambda result: result.velocity)
        first_result = True
        for result in cs_results_sorted:
            if (first_result):
                desc_string += result.description()
                first_result = False
            else:
                desc_string += "\n"
                desc_string += "%30s    %s   %s" % (self.name+':'+self.irasname, self.coordinates.description(), result.description())
        return desc_string


def prepareBeuther():
    filename = "./catalogues/beuther.catalogue"
    sourcesInitStringNumber = 99
    sourcesFinlStringNumber = 168
    resultsInitStringNumber = 376
    resultsFinlStringNumber = 469

    # sources
    csFile = open(filename, 'r')
    csList = csFile.readlines()
    beutherSources = []
    j = 0  # there is no numeration in Beuther catalogue. Starts from 0
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        # Names
        sourcename = "BEUTHER:" + str(j)
        irasname = csList[i][0:10]
        # Coordinates
        ra_h = float(csList[i][11:13])
        ra_m = float(csList[i][14:16])
        ra_s = float(csList[i][16:21])
        dec_sign = csList[i][22:23]
        dec_d = float(csList[i][23:25])
        dec_m = float(csList[i][26:28])
        dec_s = float(csList[i][29:31])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        # Velocity
        velocity_string = csList[i][32:37]
        # print "\""+ velocity_string + "\""
        if velocity_string != "      ":
            velocity = float(velocity_string)
        else:
            velocity = ERROR_VALUE
        beutherSource = BeutherSource(sourcename, coordinates, "Beuther(J/ApJ/566/945)", irasname)
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

    csFile.close()
    return beutherSources


#-----------------------------------------------------------------------------
class LarionovSource(CSSource):
    """docstring for LarionovSource"""
    def __init__(self, name, coordinates, author, irasname=""):
        super(LarionovSource, self).__init__(name, coordinates, author, irasname)

    def description(self):
        desc_string = "%30s    %s   " % (self.name, self.coordinates.description())
        cs_results_sorted = sorted(self.cs_results, key=lambda result: result.velocity)
        for result in cs_results_sorted:
            desc_string += result.description_larionov()
        return desc_string


def prepareLarionov():
    filename = "./catalogues/larionov_data_new.txt"
    sourcesInitStringNumber = 3
    sourcesFinlStringNumber = 154

    csFile = open(filename, 'r')
    csList = csFile.readlines()
    larionovSources = []
    for i in range(sourcesInitStringNumber, sourcesFinlStringNumber):
        csList[i] = csList[i].split()
        # Names
        sourcename = "LARIONOV:" + csList[i][0]
        # Coordinates
        ra_h = float(csList[i][1])
        ra_m = float(csList[i][2])
        ra_s = float(csList[i][3])
        _dec = csList[i][4]
        dec_sign = _dec[0]
        dec_d = abs(float(_dec))
        # dec_d = float(csList[i][4])
        dec_m = float(csList[i][5])
        dec_s = float(csList[i][6])
        epoch = "1950"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        # Antenna temperature
        temperature_string = csList[i][14]
        temperature = float(temperature_string)
        # Integrated temperature
        # integrated_temperature_string = csList[i][14]
        # integrated_temperature = float(integrated_temperature_string)
        # Velocity
        velocity_string = csList[i][10]
        velocity = float(velocity_string)
        # Linewidth
        linewidth_string = csList[i][12]
        linewidth = float(linewidth_string)
        # source treatment
        larionovSource = LarionovSource(sourcename, coordinates, "Larionov(J/A&AS/139/257)")
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
    # def description(self):
    #     desc_string = "%0.15s  " % ("RT22:" + self.name)
    #     desc_string += self.coordinates.description() + "  "
    #     cs_results_sorted = sorted(self.cs_results, key=lambda result: result.velocity)
    #     for result in cs_results_sorted:
    #         desc_string += result.description()
    #     return desc_string


#-----------------------------------------------------------------------------
class OurDetection(CSSource):
    """ """
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
        desc_string = "%30s    %s   " % ("RT22:" + self.name, self.coordinates.description())
        desc_string += "Ta*(%6.2f)  Vlsr(%+8.2f)  dV(%4.2f)  rms(%6.3f)  year(%4i)" % (self.antena_temperature, self.velocity, self.linewidth, self.rms, self.year)
        return desc_string

    def description(self):
        desc_string = "%20.20s   " % ("RT22:" + self.name)
        desc_string += self.coordinates.description() + "  "
        desc_string += "Ta(%5.2f)  Vlsr(%5.2f)  dV(%4.2f)  rms(%6.3f)" % (self.antena_temperature, self.velocity, self.linewidth, self.rms)
        return desc_string


#-----------------------------------------------------------------------------
class OurNondetection(Source):
    """docstring for OurNondetection"""
    def __init__(self, name, recno, coordinates, author, rms):
        super(OurNondetection, self).__init__(name, coordinates, author)
        self.recno = recno
        self.rms = rms

    def description(self):
        desc_string = "%30s    %s   " % ("RT22:" + self.name, self.coordinates.description())
        desc_string += "rms(%6.3f) year(----)" % (self.rms)
        return desc_string


#-----------------------------------------------------------------------------
# class R22(object):
#     """docstring for R22"""
#     def __init__(self, filename):
#         super(R22, self).__init__()
#         self.filename = filename
#         r22_file = open(self.filename, 'r')
#         r22_content = r22_file.readlines()
#         self.sourcename = (r22_content[1].split())[0]
#         self.coordinates = Coordinates(r22_content[3])
#         self.source_ID = self.sourcename + "_" + self.coordinates.description()


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
    filename = "./rt22/our_detections_v3.txt"
    f = open(filename, 'r')
    detectionsList = f.readlines()
    ourDetections = []
    for i in range(len(detectionsList)):
        detectionsList[i] = detectionsList[i].split()
        name = detectionsList[i][2]
        irasname = detectionsList[i][1]
        ra_h = float(detectionsList[i][5])
        ra_m = float(detectionsList[i][6])
        ra_s = float(detectionsList[i][7])
        dec_sign = detectionsList[i][8]
        dec_d = float(detectionsList[i][9])
        dec_m = float(detectionsList[i][10])
        dec_s = float(detectionsList[i][11])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        elevation = detectionsList[i][12]
        year  = int(detectionsList[i][4])
        recno = int(detectionsList[i][3]) # recno from pestalozzi catalogue
        tempr = float(detectionsList[i][17])
        vlsr  = float(detectionsList[i][18])
        linewidth = float(detectionsList[i][19])
        rms = float(detectionsList[i][21])
        our_detection = OurDetection(name, recno, year, coordinates, "shulga", elevation, tempr, vlsr, linewidth, rms)
        ourDetections.append(our_detection)
        # print our_detection.description()
    print 'Our detections number: ' + str(len(ourDetections))
    return ourDetections


def prepareOurNondetections():
    filename = "./rt22/our_nondetections_v3.txt"
    f = open(filename, 'r')
    nondetectionsList = f.readlines()
    ourNondetections = []
    for i in range(len(nondetectionsList)):
        nondetectionsList[i] = nondetectionsList[i].split()
        name = nondetectionsList[i][2]
        ra_h = float(nondetectionsList[i][4])
        ra_m = float(nondetectionsList[i][5])
        ra_s = float(nondetectionsList[i][6])
        _dec = nondetectionsList[i][7]
        dec_sign = _dec[0]
        if (dec_sign != "-"):
            dec_sign = "+"
        dec_d = abs(float(_dec))
        # dec_d = float(nondetectionsList[i][7])
        dec_m = float(nondetectionsList[i][8])
        dec_s = float(nondetectionsList[i][9])
        epoch = "2000"
        coordinates = Coordinates([ra_h, ra_m, ra_s, dec_sign, dec_d, dec_m, dec_s, epoch], "list_equat")
        recno = int(nondetectionsList[i][3])  # recno from pestalozzi catalogue
        rms = float(nondetectionsList[i][14])
        our_nondetection = OurNondetection(name, recno, coordinates, "shulga", rms)
        ourNondetections.append(our_nondetection)
        # print our_nondetection.description()
    print 'Out nondetections number: '+str(len(ourNondetections))
    return ourNondetections


#-----------------------------------------------------------------------------
def setMarkForR22Observations(masers, detections, nondetections, spatial_resolution_arcsec=10):
    for maser in masers:
        for detection in detections:
            if (maser.coordinates.isIdenticalWithCoordinates(detection.coordinates, spatial_resolution_arcsec/60.0)):
                maser.markAsRT22Detected()
                maser.addOurCS(detection)
    for maser in masers:
        for nondetection in nondetections:
            if (maser.coordinates.isIdenticalWithCoordinates(nondetection.coordinates, spatial_resolution_arcsec/60.0)):
                maser.markAsRT22Nondetected()
                maser.addOurCS(nondetection)
    return


def setMarkForOtherObservations(masers, other_cs_catalogues, spatial_resolution_arcsec=10):
    for cs_catalogue in other_cs_catalogues:
        for detection in cs_catalogue:
            for maser in masers:
                if (maser.coordinates.isIdenticalWithCoordinates(detection.coordinates, spatial_resolution_arcsec/60.0)):
                    maser.markAsOtherDetected()
                    maser.addThirdpartyCS(detection)
    return


#-----------------------------------------------------------------------------
def selectCSResultsForMasersTable(cs_results_list, masers_list):
    for masers in masers_list:
        for maser in masers:
            maser.selectAppropriateCSObservations(cs_results_list)
    return


#-----------------------------------------------------------------------------
# Main program logic
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
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()

    # prepare our CS observations lists
    # ourObservationsList = prepareCSObservations()
    ourDetectionsList   = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()

    # create catalogue for 2012 observational session
    catalogue_file = open('cs_catalogue_2013.cat', 'w')
    # --- select third-party CS observations
    masers_list = [pestalozziList, valttsList, chenList]
    cs_results_list = [bronfmanList, beutherList, larionovList]
    selectCSResultsForMasersTable(cs_results_list, masers_list)
    # --- mark r22 CS observations
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(valttsList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(chenList, ourDetectionsList, ourNondetectionList)
    # --- pestalozzi catalogue
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Pestalozzi catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in pestalozziList:
        if maser.isNothernSource():
            item = maser.observationalCatalogueItem()
            if item != "":
                #print item
                catalogue_file.write(item)
    # --- valtts catalogue
    catalogue_file.write("\n\n\n// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Valtts catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in valttsList:
        if maser.isNothernSource():
            item = maser.observationalCatalogueItem()
            if item != "":
                #print item
                catalogue_file.write(item)
    # --- chen catalogue
    catalogue_file.write("\n\n\n// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Chen catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in chenList:
        if maser.isNothernSource():
            item = maser.observationalCatalogueItem()
            if item != "":
                #print item
                catalogue_file.write(item)
    # --- description of the catalogue ---
    catalogue_file.write("\n\n\n// ----------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//    Description of the table\n")
    catalogue_file.write("// ----------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("  Only sources for Northern hemisphere are placed in this catalogue (declination > 0).\n")
    catalogue_file.write("  Col.1   - Maser source name (from the maser catalogue). If there is no name - number used.\n")
    catalogue_file.write("  Col.2   - Coordinates of the maser source from the catalogue.\n")
    catalogue_file.write("  Col.3   - Vlsr value from maser catalogue.\n")
    catalogue_file.write("  Col.4   - Maser flux or flux dencity (depends on the maser catalogue).\n")
    catalogue_file.write("  Col.5   - Maser catalogue identifier.\n")
    catalogue_file.write("  Col.6   - Mark of the RT22 CS observations towards this maser source:\n")
    catalogue_file.write("        \"-\" - there were no observations;\n")
    catalogue_file.write("        \"n\" - negative observation (CS line was not detected);\n")
    catalogue_file.write("        \"y\" - positive observation (CS line was detected);\n")
    catalogue_file.write("  Col.7   - Mark of CS observations towards this maser source from other authors:\n")
    catalogue_file.write("        \"-\" - there were no observations;\n")
    catalogue_file.write("        \"n\" - negative observation (CS line was not detected);\n")
    catalogue_file.write("        \"y\" - positive observation (CS line was detected);\n")
    catalogue_file.write("  Col.8   - deniote if maser needs additional observations. Maser is marked as \"y\" if:\n")
    catalogue_file.write("                * there is no CS observations of that source on the RT22;\n")
    catalogue_file.write("                * the maser spectral line does not fit into any of the observed CS lines (Vcs - dVcs <= Vmaser <= Vcs + dVcs );\n")
    catalogue_file.write("        \"y\" - marked for observations in 2012;\n");
    catalogue_file.write("        \"n\" - no need for further obsevations;\n")
    catalogue_file.write("// ----------------------------------------------------------------------------------------------------\n")
    
    catalogue_file.close()
    return


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

    # create catalogue for 2012 observational session
    catalogue_file = open('cs_table_2013.cat', 'w')
    # --- select third-party CS observations
    masers_list = [pestalozziList, valttsList, chenList]
    cs_results_list = [bronfmanList, beutherList, larionovList]
    selectCSResultsForMasersTable(cs_results_list, masers_list)
    # --- mark r22 CS observations
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(valttsList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(chenList, ourDetectionsList, ourNondetectionList)
    # --- pestalozzi catalogue
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Pestalozzi catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in pestalozziList:
        item = maser.observationalTableItem()
        if item != "":
            # print item
            catalogue_file.write(item)
    # --- valtts catalogue
    catalogue_file.write("\n\n\n// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Valtts catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in valttsList:
        # if (maser.name == "VALTTZ_133"):
        #     pdb.set_trace()
        item = maser.observationalTableItem()
        if item != "":
            # print item
            catalogue_file.write(item)
    # --- chen catalogue
    catalogue_file.write("\n\n\n// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//     Chen catalogue \n")
    catalogue_file.write("// --------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("// ---------- 1 ------------------/------------------ 2 ---------------/---- 3 -----/------- 4 -----/--5---------/-----------6---------------/--7--/--8--/--9--/\n")
    for maser in chenList:
        item = maser.observationalTableItem()
        if item != "":
            #print item
            catalogue_file.write(item)
    # --- description of the catalogue ---
    catalogue_file.write("\n\n\n// ----------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("//    Description of the table\n")
    catalogue_file.write("// ----------------------------------------------------------------------------------------------------\n")
    catalogue_file.write("  Col.1   - Maser source name (from the maser catalogue). If there is no name - number used.\n")
    catalogue_file.write("  Col.2   - Coordinates of the maser source from the catalogue.\n")
    catalogue_file.write("  Col.3   - Vlsr value from maser catalogue.\n")
    catalogue_file.write("  Col.4   - Maser flux or flux dencity (depends on the maser catalogue).\n")
    catalogue_file.write("  Col.5   - Maser catalogue identifier.\n")
    catalogue_file.write("  Col.6   - Mark of the RT22 CS observations towards this maser source:\n")
    catalogue_file.write("        \"-\" - there were no observations;\n")
    catalogue_file.write("        \"n\" - negative observation (CS line was not detected);\n")
    catalogue_file.write("        \"y\" - positive observation (CS line was detected);\n")
    catalogue_file.write("  Col.7   - Mark of CS observations towards this maser source from other authors:\n")
    catalogue_file.write("        \"-\" - there were no observations;\n")
    catalogue_file.write("        \"n\" - negative observation (CS line was not detected);\n")
    catalogue_file.write("        \"y\" - positive observation (CS line was detected);\n")
    catalogue_file.write("  Col.8   - deniote if maser needs additional observations. Maser is marked as \"y\" if:\n")
    catalogue_file.write("                * there is no CS observations of that source on the RT22;\n")
    catalogue_file.write("                * the maser spectral line does not fit into any of the observed CS lines (Vcs - dVcs <= Vmaser <= Vcs + dVcs );\n")
    catalogue_file.write("        \"y\" - marked for observations in 2012;\n");
    catalogue_file.write("        \"n\" - no need for further obsevations;\n")
    catalogue_file.write("\
       CS line parameters presented in the next line for all positive detections of CS.\n \
      Every line begins with the arrow, catalog ID and source name or number.\n \
      Then coordinates and spectral line parameters come.\n \
      RMS for RT22 observations means 3*sigma level (is taken from observational programm)\n");  
    catalogue_file.write("// ----------------------------------------------------------------------------------------------------\n")

    catalogue_file.close()
    return


##########################################################################################
# Staistics part
##########################################################################################

def prepareIClassForStatistics():
    return


def prepareIIClassForStatistics():
    return


def prepareOurIClassForStatistics():
    pestalozziList = preparePestalozzi()
    ourDetectionsList = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in pestalozziList:
        if maser.rt22DetectionMark == RT22_DETECTED:
            for item in maser.our_cs_results:
                print "%s %s %f %f %f %f %f" % (maser.name, maser.coordinates.description(), maser.velocity, maser.flux, item.velocity, item.linewidth, item.antena_temperature)
    return


def prepareOurIIClassForStatistics():
    valttzList = prepareValttz()
    ourDetectionsList = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()
    setMarkForR22Observations(valttzList, ourDetectionsList, ourNondetectionList)
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in valttzList:
        if maser.rt22DetectionMark == RT22_DETECTED:
            for item in maser.our_cs_results:
                print "%s %s %f %f %f %f %f" % (maser.name, maser.coordinates.description(), maser.velocity, maser.flux, item.velocity, item.linewidth, item.antena_temperature)
    return


def prepareOurChenMasersForStatistics():
    masersList = prepareChen()
    ourDetectionsList = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()
    setMarkForR22Observations(masersList, ourDetectionsList, ourNondetectionList)
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in masersList:
        if maser.rt22DetectionMark == RT22_DETECTED:
            for maser_line in maser.spectral_lines:
                for item in maser.our_cs_results:
                    print "%s %s %f %f %f %f %f %f" % (maser.name, maser.coordinates.description(), maser_line.vlsr, maser_line.flux, maser_line.linewidth, item.velocity, item.linewidth, item.antena_temperature)
    return


def prepareOtherChenMasersForStatistics():
    masersList     = prepareChen()
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()
    setMarkForOtherObservations(masersList, [bronfmanList, beutherList, larionovList])
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in masersList:
        if maser.otherDetectionMark == OTHER_DETECTED:
            for maser_line in maser.spectral_lines:
                for item in maser.other_cs_sources:
                    print "%s %s %f %f %f %s" % (maser.name, maser.coordinates.description(), maser_line.vlsr, maser_line.flux, maser_line.linewidth, item.description())
    return


def prepareOtherIClassForStatistics():
    masersList     = prepareChen()
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()
    setMarkForOtherObservations(masersList, [bronfmanList, beutherList, larionovList])
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in masersList:
        if maser.otherDetectionMark == OTHER_DETECTED:
            for item in maser.other_cs_sources:
                print "%s %s %f %f %s" % (maser.name, maser.coordinates.description(), maser.velocity, maser.flux, item.description())
    return


def prepareOtherIIClassForStatistics():
    valttzList = prepareValttz()
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()
    setMarkForOtherObservations(valttzList, [bronfmanList, beutherList, larionovList])
    # prepare table
    # stat_file = open('our_Iclass_stat.dat')
    for maser in valttzList:
        if maser.otherDetectionMark == OTHER_DETECTED:
            for item in maser.other_cs_sources:
                print "%s %s %f %f %s" % (maser.name, maser.coordinates.description(), maser.velocity, maser.flux, item.description())
    return


def prepareForStatistics():
    # prepare lists of masers
    pestalozziList = preparePestalozzi()
    valttsList     = prepareValttz()
    chenList       = prepareChen()
    findCataloguesIntersection(pestalozziList, valttsList)
    findCataloguesIntersection(pestalozziList, chenList)
    findCataloguesIntersection(valttsList, chenList)

    # prepare third-party CS observations lists
    bronfmanList   = prepareBronfman()
    beutherList    = prepareBeuther()
    larionovList   = prepareLarionov()

    # prepare our CS observations lists
    # ourObservationsList = prepareCSObservations()
    ourDetectionsList   = prepareOurDetections()
    ourNondetectionList = prepareOurNondetections()

    # create catalogue for 2012 observational session
    catalogue_file = open('cs_table_2013.cat', 'w')
    # --- select third-party CS observations
    masers_list = [pestalozziList, valttsList, chenList]
    cs_results_list = [bronfmanList, beutherList, larionovList]
    
    # --- mark r22 CS observations
    setMarkForR22Observations(pestalozziList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(valttsList, ourDetectionsList, ourNondetectionList)
    setMarkForR22Observations(chenList, ourDetectionsList, ourNondetectionList)
    # TODO:
    # - make list of observations for statistics
    # - which python module should be used to make statistics
    # - split sources into some groups for separate statistics:
    #   1. Iclass 
    #   2. IIclass
    #   3. BothClasses
    #   4. OurResultsOnly
    #   5. OtherResultsOnly
    #   6. AllResults
    # - graphics for obtained statistics (gnuplot)
    # - overall table for comparison
    
    # output for statistic should contain next columns:
    # - source name
    # - other possible source ids
    # - Vlsr
    # - dV
    # - Ta
    # - Vlsr meth
    # - dV meth / Vmin & Vmax
    # - S/Sint meth
    # - 
    return


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    # prepareMaserCatalogsForObservations2012()
    # prepareMaserTableForObservations2012()

    # prepareOurIClassForStatistics()
    # prepareOurIIClassForStatistics()
    # prepareOtherIClassForStatistics()
    # prepareOtherIIClassForStatistics()

    # prepareOurChenMasersForStatistics()
    prepareOtherChenMasersForStatistics()

    print "Finished OK!"
