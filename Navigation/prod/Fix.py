'''
Created on Oct 7, 2016

@author: lzz0019
'''
import math
import xml.dom.minidom
import Navigation.prod.Angle as Angle

from __builtin__ import str

class Fix():
    def __init__(self, logFile=None):
        if logFile is None:
            self.logFileName="log.txt"
        elif self.invalidLogFileName(logFile) is True:
            raise ValueError("Fix.__init__:  violate parameter specification!")
        else:
            self.logFileName=logFile+ ".txt"
       
        try:
            self.logFileObject=open(self.logFileName,"a")
            self.logFileObject.write("Start of log\n")
            self.logFileObject.close()
        except ValueError:
            raise ValueError("Fix.__init__:  logFile cannot be created or appended!")
        
    def invalidLogFileName(self, logFile):
        if isinstance(logFile, str) and len(logFile)>=1:    # a correct parameter should be a string&& string length>=1
            return False                                    # this is a right,correct parameter
        else:
            return True                                     # this is a wrong parameter
        
    def setSightingFile(self,sightingFile):
        if self.invalidXmlFileName(sightingFile) is True:
            raise ValueError("Fix.setSightingFile:  invalid xml file name!")
        else:           
            self.xmlFileName=sightingFile
            self.logFileObject=open(self.logFileName, "a")
            self.logFileObject.write("Start of sighting file "+self.xmlFileName+"\n")
            self.logFileObject.close()
            return self.xmlFileName
        
    def invalidXmlFileName(self, sightingFile):
        if not(sightingFile.endswith(".xml")):              # if not end with .xml => invalid file name
            return True
        elif len(sightingFile)<5:
            return True
        else:
            try:
                self.xmlFileObject=open(sightingFile,"r")
                self.xmlFileObject.close()
            except ValueError:
                raise ValueError("Fix.setSightingFile:  xml file cannot be opened!")
            else:
                return False
    
    def getSightings(self):
        self.approximateLatitude="0d0.0"
        self.approximateLongitude="0d0.0"       
        tree=self.buildDOM(self.xmlFileName)
        
        sightingDict=self.extractSighting(tree)
                 
        updatedDict=self.adjustedAltitude(sightingDict)
        self.writeToLog(updatedDict) 
        self.logFileObject=open(self.logFileName,"a")
        self.logFileObject.write("End of sighting file "+self.xmlFileName+"\n") 
        self.logFileObject.close()
        return (self.approximateLatitude, self.approximateLongitude)        
            
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
            time=self.extractElement("time", sighting)
            observation=self.extractElement("observation", sighting)
            if (body==None) or (date==None) or (time==None) or (observation==None):
                raise ValueError("Fix.getSightings:  mandatory tag is missing!")
            height=self.extractElement("height", sighting)
            temperature=self.extractElement("temperature", sighting)
            pressure=self.extractElement("pressure", sighting)
            horizon=self.extractElement("horizon", sighting)
            attributeDict['body']=body
            attributeDict['date']=date
            attributeDict['time']=time
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
        else:
            value=tagList[0].firstChild.nodeValue
        return value
    
    def adjustedAltitude(self, sightingDict):
        for eachSighting in sightingDict:
            attributeDict=sightingDict.get(eachSighting)
            observation=attributeDict.get('observation')                    #observation value e.g "045d15.2"
            angleInstance=Angle.Angle()
            observedAltitude=angleInstance.setDegreesAndMinutes(observation)
            if observedAltitude<0.1:
                raise ValueError("Fix.getSightings:  observed altitude is LT. 0.1arc-minutes!")         
            height=attributeDict.get('height')
            horizon=attributeDict.get('horizon')      
            dip=self.calcDip(height,horizon)                # 1. calculate dip
            temperature=attributeDict.get('temperature')
            pressure=attributeDict.get('pressure')
            refraction=self.calcRefraction(temperature,pressure,height)      # 2. calculate refraction
            # 3. adjustedAltitude = observedAltitude + dip + refraction
            
            adjustedAltitude=round((observedAltitude+dip+refraction),1)
            angleInstance.setDegrees(adjustedAltitude)
            adjustedAltitudeFormat=angleInstance.getString()
            attributeDict['adjustedAltitude']=adjustedAltitudeFormat
        return sightingDict
        
    def calcDip(self,height,horizon): 
        if horizon=='Natural':
            sqrtValue=math.sqrt(height)
            result=((-0.97)*sqrtValue)/60
        else:
            result=0
        return result
               
    def calcRefraction(self,temperature,pressure,height):
        celsius=(temperature - 32)*5/9
        tangentALtitude=math.atan(height)
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
        self.ariesFile=ariesFile
        pass  
    
    def setStarFile(self,starFile):
        self.starFile=starFile
        pass
        