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
        self.ariesFile=None
        self.starFile=None
        self.sightingErrors=0
                
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
                return os.path.abspath(self.xmlFileName)
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
        if self.ariesFile is None:
            raise ValueError("Fix.getSightings:  aries file has not been set!")
        if self.starFile is None:
            raise ValueError("Fix.getSightings:  star file has not been set!")
        self.approximateLatitude="0d0.0"
        self.approximateLongitude="0d0.0"   
        tree=self.buildDOM(self.xmlFileName)
        sightingDict=self.extractSighting(tree) 
        sightingDict=self.adjustedAltitude(sightingDict)
        sightingDict=self.calcGeoLatiLongi(sightingDict)
        self.writeToLog(sightingDict) 
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
        i=1                                  # create a sighting dictionary 
        for sighting in sightings:
            errorflag=False
            attributeDict={}
            sightingDict[i]=attributeDict
            body=self.extractElement("body", sighting)
            date=self.extractElement("date", sighting)
            timeStr=self.extractElement("time", sighting)
            observation=self.extractElement("observation", sighting)
            height=self.extractElement("height", sighting)
            temperature=self.extractElement("temperature", sighting)
            pressure=self.extractElement("pressure", sighting)
            horizon=self.extractElement("horizon", sighting)
            if (body is None) or (date is None) or (timeStr is None) or (observation is None):
                errorflag=True
            if not self.isValidDate(date):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid date!")
            if not self.isValidTime(timeStr):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid time!")
            if not self.isValidObservation(observation):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid observation!")
            attributeDict['body']=body
            attributeDict['date']=date
            attributeDict['time']=timeStr
            attributeDict['observation']=observation
            if height is None:
                attributeDict['height']=0
            elif not self.isValidHeight(height):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid height!")
            else:
                attributeDict['height']=float(height)
                
            if temperature is None:
                attributeDict['temperature']=72
            elif not self.isValidTemperature(temperature):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid temperature!")
            else:
                attributeDict['temperature']=float(temperature)
                
            if pressure is None:
                attributeDict['pressure']=1010
            elif not self.isValidPressure(pressure):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid pressure!")
            else:
                attributeDict['pressure']=int(pressure)
                
            if horizon is None:
                attributeDict['horizon']="natural"
            elif not self.isValidHorizon(horizon):
                errorflag=True
#                 raise ValueError("Fix.getSightings: invalid horizon!")
            else:
                attributeDict['horizon']=horizon
                
            attributeDict['errorflag']=errorflag
            if errorflag is True:
                self.sightingErrors=self.sightingErrors+1
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
        
    def isValidHeight(self,height):
        height=str(height)
        strHeight=height.replace(".","0")
        if strHeight.isdigit():
            return True
        else:
            return False
    
    def isValidTemperature(self,temperature):
        temperature=str(temperature)
        temperature=int(temperature)
        if temperature<=120 and temperature>=-20:
            return True
        else:
            return  False
        
    def isValidPressure(self,pressure):
        pressure=str(pressure)
        try:
            pressure=int(pressure)
            if pressure<=1100 and pressure>=100:
                return True
            else:
                return False
        except:
            return False
        
    def isValidHorizon(self,horizon):
        horizon=str(horizon)
        if horizon.lower()=="artificial" or horizon.lower()=="natural":
            return True
        else:
            return False
    
    def adjustedAltitude(self, sightingDict):
        for eachSighting in sightingDict:
            attributeDict=sightingDict.get(eachSighting)
            if attributeDict.get('errorflag') is False: 
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
                print "adjustedAltitude",adjustedAltitudeFormat
        return sightingDict
    
    def calcGeoLatiLongi(self,sightingDict):
        if (self.xmlFileName is None) or (self.ariesFile is None) or (self.starFile is None):
            raise ValueError("Fix.getSightings:  sighting file/aries file/star file, has not been set!")
        for eachSighting in sightingDict:
            attributDict=sightingDict.get(eachSighting)
            if attributDict.get('errorflag') is False:
                # locate star entry
                starEntry=[]
                starEntryList=[]        # starEntryList is a list of lines that has same body
                bodyValue=attributDict.get('body')
                self.starFileObject=open(self.starFile,'r')
                starFileContents=self.starFileObject.readlines()
                self.starFileObject.close()
                for starEntryNumber in range(0,len(starFileContents)):
                    if(starFileContents[starEntryNumber].find(bodyValue) > -1):
                        #store entries in form of a list of tuples
                        contentString=starFileContents[starEntryNumber]
                        starEntryList.append(contentString.split())
                starEntryList=sorted(starEntryList, cmp=lambda x,y: cmp(time.strptime(x[1], "%m/%d/%y"), time.strptime(y[1], "%m/%d/%y")))
                starEntry=starEntryList[0]
                latitude=starEntry[3]       #latitude stores a string, format "wdz.z"
                attributDict['geographic position latitude']=latitude
                print "geographic position latitude=",latitude
                SHAstar=starEntry[2]        #SHAstar-----string
                # calculate GHAaries: need GHAaries1, GHAaries2, s
                self.ariesFileObject=open(self.ariesFile,'r')
                ariesFileContents=self.ariesFileObject.readlines()
                self.ariesFileObject.close()
                dateValue=attributDict.get('date')
                dateTarget=time.strftime("%m/%d/%y", time.strptime(dateValue, "%Y-%m-%d"))
                timeValue=attributDict.get('time')
                hourTarget1=str(time.strptime(timeValue, "%H:%M:%S")[3])
                GHA1entry=None
                for lineNumber in range(0,len(ariesFileContents)):
                    if(ariesFileContents[lineNumber].find(dateTarget)>-1):
                        if(ariesFileContents[lineNumber].split()[1].find(hourTarget1)>-1):
                            print "*****"
                            GHA1entry=ariesFileContents[lineNumber]
                            break
                GHAaries1=GHA1entry.split()[2]          # GHAaries1----string
                hourTarget2=str((time.strptime(timeValue, "%H:%M:%S")[3]+1)%24)
                GHA2entry=None
                for lineNumber in range(0,len(ariesFileContents)):
                    if(ariesFileContents[lineNumber].find(dateTarget)>-1):
                        if(ariesFileContents[lineNumber].split()[1].find(hourTarget2)>-1):
                            GHA2entry=ariesFileContents[lineNumber]
                            break
                GHAaries2=GHA2entry.split()[2]          # GHAaries2----string
                s= time.strptime(timeValue, "%H:%M:%S")[4]*60+ time.strptime(timeValue, "%H:%M:%S")[5]
                # calculate GHAaries: step1, temp=GHAaries2-GHAaries1
                #                     step2, temp=|temp|---get absolute value
                #                     step3, temp=temp*(s/3600)
                #                     step4, temp=temp+GHAaries1
                #                     step5, GHAaries=temp
                GHAaries1Angle=Angle.Angle()
                GHAaries1Angle.setDegreesAndMinutes(GHAaries1)
                GHAaries2Angle=Angle.Angle()
                GHAaries2Angle.setDegreesAndMinutes(GHAaries2)
                temp=GHAaries2Angle.subtract(GHAaries1Angle)
                temp=abs(temp)
                temp=temp*(s/3600.0)                      # temp----float
                tempAngle=Angle.Angle()
                tempAngle.setDegrees(temp)
                temp=GHAaries1Angle.add(tempAngle)        # temp----float
                GHAaries=temp 
                GHAariesAngle=Angle.Angle()
                GHAariesAngle.setDegrees(GHAaries)
                SHAstarAngle=Angle.Angle()
                SHAstarAngle.setDegreesAndMinutes(SHAstar)
                GHAobservation=GHAariesAngle.add(SHAstarAngle)  # result is float
                GHAobservationAngle=Angle.Angle()
                GHAobservationAngle.setDegrees(GHAobservation)
                longitude=GHAobservationAngle.getString()
                attributDict['geographic position longitude']=longitude   
                print "geographic position longitude=",longitude             
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
            if element[1].get('errorflag') is False:
                bodyValue=element[1].get('body')
                dateValue=element[1].get('date')
                timeValue=element[1].get('time')
                adjstAltiValue=element[1].get('adjustedAltitude')
                geoPosiLatiValue=element[1].get('geographic position latitude')
                geoPosiLongiValue=element[1].get('geographic position longitude')
                stringToWrite=bodyValue+"\t"+dateValue+"\t"+timeValue+"\t"+adjstAltiValue+"\t"
                stringToWrite=stringToWrite+geoPosiLatiValue+"\t"+geoPosiLongiValue+"\n"
                self.logFileObject.write(stringToWrite)
                
        stringToWrite="Sighting errors:"+"\t"+str(self.sightingErrors)+"\n"
        self.logFileObject.write(stringToWrite)           
        self.logFileObject.close()
    
    def setAriesFile(self,ariesFile=None): 
        if ariesFile is None:
            raise ValueError("Fix.setAriesFile: missing ariesFile name!") 
        elif(not isinstance(ariesFile, str)):
            raise ValueError("Fix.setAriesFile:  the file name should be a string!")
        elif (not(ariesFile.endswith(".txt"))):
            raise ValueError("Fix.setAriesFile:  the file name should have .txt extension!")
        elif len(ariesFile.split(".")[0])<1:
            raise ValueError("Fix.setAriesFile:  the file name should have length>=1")
        else:
            if not os.path.isfile(ariesFile):
                raise ValueError("Fix.setAriesFile: ariesFile does not exist!")
            try:
                self.ariesFileObject=open(ariesFile,"r")
                self.ariesFileObject.close()
                self.ariesFile=ariesFile
            except ValueError:
                raise ValueError("Fix.setAriesFile: ariesFile cannot be opened!")
            try:
                self.logFileObject=open(self.logFileName,"a")
                self.logFileObject.write("Aries file:"+" "+os.path.abspath(self.ariesFile)+"\n")
                self.logFileObject.close()
            except ValueError:
                raise ValueError("Fix.setAriesFile:  logFile cannot be opened!")
        return os.path.abspath(self.ariesFile)
    
    def setStarFile(self,starFile=None):
        if starFile is None:
            raise ValueError("Fix.setStarFile:    missing starFile name!")
        elif(not isinstance(starFile, str)):
            raise ValueError("Fix.setStarFile:  the file name should be a string!")
        elif not(starFile.endswith(".txt")):
            raise ValueError("Fix.setStarFile:  the file name should have .txt extension!")
        elif len(starFile.split(".")[0])<1:
            raise ValueError("Fix.setStarFile:  the file name should have length>=1")
        else:
            if not os.path.isfile(starFile):
                raise ValueError("Fix.setStarFile:    starFile does not exist!")
            try:
                self.starFileObject=open(starFile,"r")
                self.starFileObject.close()
                self.starFile=starFile
            except ValueError:
                raise ValueError("Fix.setStarFile:    starFile cannot be opened!")
            try:
                self.logFileObject=open(self.logFileName,"a")
                self.logFileObject.write("Star file:"+" "+os.path.abspath(self.starFile)+"\n")
                self.logFileObject.close()
            except ValueError:
                raise ValueError("Fix.setStarFile:  logFile cannot be opened!")
        return os.path.abspath(self.starFile)
        