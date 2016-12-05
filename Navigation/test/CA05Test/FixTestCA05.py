'''
Created on Nov 26, 2016

@author: lzz0019
'''
import unittest
import uuid
import os
import Navigation.prod.Fix as F

class TestFix(unittest.TestCase):

        
#----------          
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    
#==================== Fix.getSightings ===================         
#   300 getSightings  
#        Happy Path
    def test300_010_ShouldDefaultToZeroOnMissingParameter(self):
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        theFix.getSightings()
        expectedResult=("0d0.0","0d0.0")
        result=theFix.getAssumedLatiLogi()
        self.assertTupleEqual(result,expectedResult)
     
    def test300_020_ShouldReturnTupleOfApproximateLocation(self):
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        result=theFix.getSightings("N27d59.5", "85d33.4")
        expectedResult=("N20d15.5","79d19.9")
        self.assertTupleEqual(result, expectedResult)
            
#     def test300_030_ShouldLogOneSighting(self):
#         targetStringList = ["Pollux", "2017-04-14", "23:50:14", "15d01.5", "27d59.1", "84d33.4", "N27d59.5", "85d33.4", "292d44.6", "174"]
#         theFix = F.Fix("shouldLogOneSighting.txt")
#         theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
#         theFix.setAriesFile("CA03_Valid_Aries.txt")   
#         theFix.setStarFile("CA03_Valid_Stars.txt")
#         theFix.getSightings("N27d59.5", "85d33.4")
#              
#         theLogFile = open("shouldLogOneSighting.txt", "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#              
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings " + "houldLogOneSighting.txt")
#         self.assertEquals(1, sightingCount)
#         self.deleteNamedLogFlag = True  
   
#------Sad Path
    def test300_910_ShouldRaiseExceptionOnNoneStringParameter(self):
        expectedDiag ="Fix.getSightings:"
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings(123, 34.5)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_920_ShouldRaiseExceptionOnMissing_d_Parameter(self):
        expectedDiag ="Fix.getSightings:"
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N2759.5", "85d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N27d59.5", "8533.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
            
    def test300_930_ShouldRaiseExceptionOnInvalidAssumedLongitude_XY_OutOfRange(self):
        expectedDiag ="Fix.getSightings:"
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N27d59.5", "720d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N27d59.5", "85d70.5")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
            
    def test_940_ShouldRaiseExceptionOnInvalidAssumedLatitude_XY_OutOfRange(self):
        expectedDiag ="Fix.getSightings:"
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N100d59.5", "85d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N27d60.1", "85d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
             
    def test_950_ShouldRaiseExceptionOnInvalidAssumedLatitude_inconsistentXYHvalue(self):
        expectedDiag ="Fix.getSightings:"
        theFix=F.Fix()
        theFix.setSightingFile("CA05_300_ValidSightingFile.xml")
        theFix.setStarFile("CA03_Valid_Stars.txt")
        theFix.setAriesFile("CA03_Valid_Aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("N0d0.0", "85d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        with self.assertRaises(ValueError) as context:
            theFix.getSightings("27d50.0", "85d33.4")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    
        
        