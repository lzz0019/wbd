'''
Created on Oct 7, 2016

@author: lzz0019
'''
import unittest
import Navigation.prod.Fix as Fix
import os

class FixTest(unittest.TestCase):


    def setUp(self):
        self.className = "Fix."

    def tearDown(self):
        pass

#    Acceptance Test: 100
#        Analysis - Contructor
#            inputs
#                name of a file-"logFile"
#            outputs
#                instance of Fix
#            state change
#                Write "Start of log" to the log file
#
#            Happy path
#                nominal case:  Fix()
#            Sad path
#                1. file name violates parameter specification 
#                    1) logFile is not a string
#                    2) logFile is a string, but string length<1
#                2. file cannot be created or appended for whatever reasons.
                
#
#    Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
        # note:   At this point, we don't any way of verifying the value of the Fix.
        #         We'll be able to so when we construct tests for the getters
         
    def test100_020_logFileShouldExistAfterConstructor(self):
        aFix=Fix.Fix()
        logFileName=aFix.logFileName
        filePath="./"+ logFileName
        self.assertEqual(os.path.exists(filePath), True)
          
    def test100_030_ShouldWriteLogEntryToFile(self):
        aFix=Fix.Fix()
        logFileName=aFix.logFileName
        for line in reversed(open(logFileName).readlines()):
            string=line.rstrip()
            break
        expectedString="Log file:"+"\t"+"/"+os.path.abspath(logFileName)
        self.assertEqual(string, expectedString)
                   
#    Sad Path
    def test100_910_ShouldRaiseExceptionOnViolatingParameterSpecification(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix(1)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
          
    def test100_920_ShouldRaiseExceptionOnViolatingParameterSpecification(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
  
#-----------------------------------------------------------------
#    Acceptance Test: 200
#        Analysis - setSightingFile
#            inputs
#                a file name- "sightingFile"
#            outputs
#                a string having the value passed as th "sightingFile"
#            state change
#                write "Start of sighting file f.xml" to the log file 
#                (f.xml is the actual name of the file)
#
#            Happy path
#                return value is correct
#                an entry is written to the end of log file
#            Sad path
#                
#    Happy Path
         
    def test200_020_ShouldWriteEntryToLogFile(self):
        fixInstance=Fix.Fix()
        fixInstance.setSightingFile("2.xml")
        logFileName=fixInstance.logFileName
        for line in reversed(open(logFileName).readlines()):
            string=line.rstrip()
            break
        expectedString="Sighting file:"+"\t"+os.path.abspath(fixInstance.xmlFileName)
        self.assertEqual(string, expectedString)
         
#    sad path
    def test200_910_ShouldRaiseExceptionFileNameViolateParameterSpecification(self):
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setSightingFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setSightingFile("2")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
          
    def test200_920_ShouldRaiseExceptionFileNameViolateParameterSpecification(self):
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setSightingFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setSightingFile(".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
#     
#     def test200_930_ShouldRaiseExceptionFileCannotOpen(self):
#         fixInstance=Fix.Fix()
#         expectedDiag = self.className + "setSightingFile: "
#         with self.assertRaises(ValueError) as context:
#             fixInstance.setSightingFile("3.xml")
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 

      
#-----------------------------------------------------------------
#    Acceptance Test: 300
#        Analysis - getSightings
#            inputs
#                none
#            outputs
#                return (approximateLatitude, approximateLongitude)
#            state change
#                Navigational calculations are written to the log file 
#
#            Happy path
#                return value is correct
#                an entry is written to the end of log file
#            Sad path
#                
#    Happy Path
    def test300_010_ShouldReturnApproximateLocation(self):
        fixInstance=Fix.Fix("test1")
        fixInstance.setSightingFile("test1.xml")
        self.assertEqual(fixInstance.getSightings(),("0d0.0","0d0.0"))
        
#    Sad Path     ?????
#     def test300_910_ShouldRaiseExceptionSightingFileHasNotBeenSet(self):
#         fixInstance=Fix.Fix("test1.1")
#         fixInstance.setAriesFile("aries.txt")
#         fixInstance.setStarFile("stars.txt")
#         expectedDiag = self.className + "getSightings: "
#         with self.assertRaises(ValueError) as context:
#             fixInstance.getSightings()
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
#-----------------------------------------------------------------
#    Acceptance Test: 400
#        Analysis - setAriesFile
#    Happy Path   
    def test400_010_ShouldReturnAbsoluteFilePath(self):
        fixInstance=Fix.Fix("test2")
        result=fixInstance.setAriesFile("aries.txt")
        expectedString=os.path.abspath("aries.txt")
        self.assertEqual(result,expectedString)
    
    def test400_020_ShouldWriteToTheLogFile(self):
        fixInstance=Fix.Fix("test2")
        fixInstance.setAriesFile("aries.txt")
        logFileName=fixInstance.logFileName
        for line in reversed(open(logFileName).readlines()):
            string=line.rstrip()
            break
        expectedString="Aries file:"+"\t"+os.path.abspath("aries.txt")
        self.assertEqual(string, expectedString)
                
#    Sad Path  
    def test400_910_ShouldRaiseExceptionFileNameIsNotAString(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setAriesFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setAriesFile(1)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test400_920_ShouldRaiseExceptionFileNameLessThanOne(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setAriesFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setAriesFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test400_930_ShouldRaiseExceptionFileNameNoExtension(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setAriesFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setAriesFile("ariesFileName")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

#-----------------------------------------------------------------
#    Acceptance Test: 500
#        Analysis - setStarFile
#    Happy Path
    def test500_010_ShouldReturnAbsoluteFilePath(self):
        fixInstance=Fix.Fix("test3")
        result=fixInstance.setStarFile("stars.txt")
        expectedString=os.path.abspath("stars.txt")
        self.assertEqual(result,expectedString)
    
    def test500_020_ShouldWriteToTheLogFile(self):
        fixInstance=Fix.Fix("test3")
        fixInstance.setStarFile("stars.txt")
        logFileName=fixInstance.logFileName
        for line in reversed(open(logFileName).readlines()):
            string=line.rstrip()
            break
        expectedString="Star file:"+"\t"+os.path.abspath("stars.txt")
        self.assertEqual(string, expectedString)
        
#    Sad Path  
    def test500_910_ShouldRaiseExceptionFileNameIsNotAString(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setStarFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setStarFile(1)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
    
    def test500_920_ShouldRaiseExceptionFileNameLessThanOne(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setStarFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setStarFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test500_930_ShouldRaiseExceptionFileNameNoExtension(self):     
        fixInstance=Fix.Fix()
        expectedDiag = self.className + "setStarFile: "
        with self.assertRaises(ValueError) as context:
            fixInstance.setStarFile("starFile")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        