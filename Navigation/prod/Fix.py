'''
Created on Oct 7, 2016

@author: lzz0019
'''
import math
import time
import os.path
import xml.dom.minidom
import Navigation.prod.Angle as Angle

from __builtin__ import str, False
from _ast import Str

class Fix():    
    
    def __init__(self, logFile=None):
        self.logFileName=None
        self.logFileObject=None
        self.approximateLatitude=None
        self.approximateLongitude=None
        self.ariesFile=None
        self.starFile=None
        self.xmlFileName=None
        self.xmlFileObject=None
                
        if logFile is None:
            self.logFileName="log.txt"
        elif self.invalidLogFileName(logFile) is True:
            raise ValueError("Fix.__init__:  violate parameter specification!")
        else:
            self.logFileName=logFile
        try:
            self.logFileObject=open(self.logFileName,"a")
            self.logFileObject.write("Log file:"+" "+os.path.abspath(self.logFileName)+"\n")
            self.logFileObject.close()
        except ValueError:
            raise ValueError("Fix.__init__:  logFile cannot be created or appended!")
        
    def invalidLogFileName(self, logFile):
        if isinstance(logFile, str) and len(logFile)>=1:    # a correct parameter should be a string&& string length>=1
            return False                                    # this is a right,correct parameter
        else:
            return True                                     # this is a wrong parameter
        
    def setSightingFile(self,sightingFile=None):
        if sightingFile is None:
            raise ValueError("Fix.setSightingFile:  missing file name!") 
        elif self.invalidXmlFileName(sightingFile) is True:
            raise ValueError("Fix.setSightingFile:  invalid xml file name!")
        else:           
            self.xmlFileName=sightingFile
            
            try:
                self.logFileObject=open(self.logFileName, "a")
                self.logFileObject.write("Sighting file:"+" " + os.path.abspath(self.xmlFileName)+"\n")
                self.logFileObject.close()
                return self.xmlFileName
            except ValueError:
                raise ValueError("Fix.setSightingFile:  cannot open log file!")
                 
    def invalidXmlFileName(self, sightingFile):
        if (not isinstance(sightingFile, str)):
            return True
        elif not(sightingFile.endswith(".xml")):              # if not end with .xml => invalid file name
            return True
        elif len(sightingFile)<5:
            return True
        elif os.path.isfile(sightingFile) is False:
            return True
        else:    
            try:
                self.xmlFileObject=open(sightingFile,"r")
                self.xmlFileObject.close()
                return False
            except ValueError:
                raise ValueError("Fix.setSightingFile:  xml file cannot be opened!")
    
    def getSightings(self):
        if self.xmlFileName is None:
            raise ValueError("Fix.getSightings:  xml file has not been set!")
        else:
            self.approximateLatitude="0d0.0"
            self.approximateLongitude="0d0.0"   
            tree=self.buildDOM(self.xmlFileName)
            sightingDict=self.extractSighting(tree)  
            updatedDict=self.adjustedAltitude(sightingDict)
            self.writeToLog(updatedDict) 
            self.logFileObject=open(self.logFileName,"a")
            self.logFileObject.write("End of sighting file "+self.xmlFileName+"\n") 
            self.logFileObject.close()
            result=(self.approximateLatitude, self.approximateLongitude) 
            return result       
            
    def buildDOM(self, fileName):
        DOMTree=xml.dom.minidom.parse(fileName)
        return DOMTree
    
    def extractSighting(self, DOMTree):
        collection=DOMTree.documentElement
        sightings=collection.getElementsByTagName("sighting")       # sightings is a list
        sightingDict={}   
        i=1                                     # create a sighting dictionary 
        for sighting in sightings:
            attributeDict={}
            sightingDict[i]=attributeDict
            body=self.extractElement("body", sighting)
            date=self.extractElement("date", sighting)
            if not self.isValidDate(date):
                raise ValueError("Fix.getSightings: invalid date!")
            timeStr=self.extractElement("time", sighting)
            if not self.isValidTime(timeStr):
                raise ValueError("Fix.getSightings: invalid time!")
            observation=self.extractElement("observation", sighting)
            if not self.isValidObservation(observation):
                raise ValueError("Fix.getSightings: invalid observation!")
            if (body==None) or (date==None) or (timeStr==None) or (observation==None):
                raise ValueError("Fix.getSightings:  mandatory tag is missing!")
            height=self.extractElement("height", sighting)
#             if not self.isValidHeight(height):
#                 raise ValueError("Fix.getSightings: invalid height!")
            temperature=self.extractElement("temperature", sighting)
            pressure=self.extractElement("pressure", sighting)
            horizon=self.extractElement("horizon", sighting)
            attributeDict['body']=body
            attributeDict['date']=date
            attributeDict['time']=timeStr
            attributeDict['observation']=observation
            if height is None:
                attributeDict['height']=0
            else:
                attributeDict['height']=float(height)
            if temperature is None:
                attributeDict['temperature']=72
            else:
                attributeDict['temperature']=float(temperature)
            if pressure is None:
                attributeDict['pressure']=1010
            else:
                attributeDict['pressure']=int(pressure)
            if horizon is None:
                attributeDict['horizon']="natural"
            else:
                attributeDict['horizon']=horizon
            i=i+1            
        return sightingDict
    
    def extractElement(self, tag, sighting):
        if(not isinstance(tag, (str, unicode))):
            raise ValueError("Fix.getSightings:  the information associated with a tag is invalid!")
        tagList=sighting.getElementsByTagName(tag)
        if len(tagList)==0:
            value=None
        elif tagList[0].firstChild==None:
            value=None
        else:
            value=tagList[0].firstChild.nodeValue
        return value
    
    def isValidDate(self,date):
        date=str(date)
        try:
            time.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False
    
    def isValidTime(self,timeStr):
        timeStr=str(timeStr)
        try:
            time.strptime(timeStr, "%H:%M:%S")
            return True
        except:
            return False
    
    def isValidObservation(self, observation):
        observation=str(observation)
        separator = "d"
        index = observation.find(separator)
        if index == -1:
            return False
        else:
            return True
        
#     def isValidHeight(self,height):
#         if height.isnumeric():
#             return True
#         else:
#             return False
    
    def adjustedAltitude(self, sightingDict):
        for eachSighting in sightingDict:
            attributeDict=sightingDict.get(eachSighting)
            observation=attributeDict.get('observation')                    #observation value e.g "045d15.2"
            angleInstance=Angle.Angle()
            observationFloat=angleInstance.setDegreesAndMinutes(observation)
            if observationFloat<0.1:
                raise ValueError("Fix.getSightings:  observed altitude is LT. 0.1arc-minutes!")         
            height=attributeDict.get('height')
            horizon=attributeDict.get('horizon')    
            dip=self.calcDip(height,horizon)                # 1. calculate dip
            temperature=attributeDict.get('temperature')
            pressure=attributeDict.get('pressure')
            refraction=self.calcRefraction(temperature,pressure,observationFloat)      # 2. calculate refraction
            # 3. adjustedAltitude = observationFloat + dip + refraction
            adjustedAltitude= observationFloat+dip+refraction
            angleInstance.setDegrees(adjustedAltitude)
            adjustedAltitudeFormat=angleInstance.getString()      
            attributeDict['adjustedAltitude']=adjustedAltitudeFormat
        return sightingDict
        
    def calcDip(self,height,horizon):
        if horizon=='natural':
            sqrtValue=math.sqrt(height)
            result=((-0.97)*sqrtValue)/60
        else:
            result=0
        return result
               
    def calcRefraction(self,temperature,pressure,observationFloat):
        celsius=(temperature - 32)*5.0/9 
        tangentALtitude=math.tan(math.radians(observationFloat))
        refraction=(-0.00452)*pressure/(273+celsius)/tangentALtitude
        return refraction
             
    def writeToLog(self, sightingDict):
        # 1. convert dictionary into list
        # 2. sort the list
        # 3. writeToLog
        sightingList=sightingDict.items()
        orderedList=sorted(sightingList, key=lambda x: (x[1].get('date'),x[1].get('body')))
        self.logFileObject=open(self.logFileName,"a")
        for element in orderedList:
            bodyValue=element[1].get('body')
            dateValue=element[1].get('date')
            tiemValue=element[1].get('time')
            adjstAltiValue=element[1].get('adjustedAltitude')
            stringToWrite=bodyValue+"\t"+dateValue+"\t"+tiemValue+"\t"+adjstAltiValue+"\n"
            self.logFileObject.write(stringToWrite)           
        self.logFileObject.close()
    
    def setAriesFile(self,ariesFile):  
        if(not isinstance(ariesFile, str)):
            raise ValueError("Fix.setAriesFile:  the file name should be a string!")
        elif not(ariesFile.endswith(".txt")):
            raise ValueError("Fix.setAriesFile:  the file name should have .txt extension!")
        elif len(ariesFile.split(".")[0])<1:
            raise ValueError("Fix.setAriesFile:  the file name should have length>=1")
        else:    
            self.ariesFile=ariesFile
            absoluteFilePath=os.path.abspath(self.ariesFile)
            try:
                self.logFileObject=open(self.logFileName,"a")
                self.logFileObject.write("Aries file:"+" "+os.path.abspath(self.ariesFile)+"\n")
                self.logFileObject.close()
            except ValueError:
                raise ValueError("Fix.setAriesFile:  logFile cannot be opened!")
        return absoluteFilePath
    
    def setStarFile(self,starFile):
        if(not isinstance(starFile, str)):
            raise ValueError("Fix.setStarFile:  the file name should be a string!")
        elif not(starFile.endswith(".txt")):
            raise ValueError("Fix.setStarFile:  the file name should have .txt extension!")
        elif len(starFile.split(".")[0])<1:
            raise ValueError("Fix.setStarFile:  the file name should have length>=1")
        else:
            self.starFile=starFile
            absoluteFilePath=os.path.abspath(self.starFile)
            try:
                self.logFileObject=open(self.logFileName,"a")
                self.logFileObject.write("Star file:"+" "+os.path.abspath(self.starFile)+"\n")
                self.logFileObject.close()
            except ValueError:
                raise ValueError("Fix.setStarFile:  logFile cannot be opened!")
        return absoluteFilePath
        