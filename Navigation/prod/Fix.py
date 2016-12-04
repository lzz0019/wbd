'''
Created on Oct 7, 2016

@author: lzz0019
'''
import math
import time
import os.path
import xml.dom.minidom
import Navigation.prod.Angle as Angle


class Fix():    
    
    def __init__(self, logFile=None):
        self.logFileName=None
        self.logFileObject=None
        self.ariesFile=None
        self.starFile=None
        self.xmlFileName=None
        self.xmlFileObject=None
        self.ariesFile=None
        self.starFile=None
        self.sightingErrors=0
        self.assumedLatitude=None
        self.assumedLongitude=None
        self.approximateLatitude=None
        self.approximateLongitude=None
                
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
    
    def getSightings(self, assumedLatitude=None, assumedLongitude=None):
        if self.xmlFileName is None:
            raise ValueError("Fix.getSightings:  xml file has not been set!")
        if self.ariesFile is None:
            raise ValueError("Fix.getSightings:  aries file has not been set!")
        if self.starFile is None:
            raise ValueError("Fix.getSightings:  star file has not been set!") 
        # Defaults to "0d0.0" for missing parameter:
        if assumedLatitude is None:
            self.assumedLatitude="0d0.0"           
        if assumedLongitude is None:
            self.assumedLongitude="0d0.0"
        # Raise Error on invalid parameter:
        if (assumedLatitude is not None) and (not isinstance(assumedLatitude, str)):
            raise ValueError("Fix.getSightings:    assumedLatitude should be a string!")
        if (assumedLongitude is not None) and (not isinstance(assumedLongitude, str)):
            raise ValueError("Fix.getSightings:    assumedLongitude should be a string!")
        if isinstance(assumedLatitude, str) and (assumedLatitude.find("d")==-1):
            raise ValueError("Fix.getSightings:    missing 'd' in assumedLatitude!")
        if isinstance(assumedLongitude, str) and (assumedLongitude.find("d")==-1):
            raise ValueError("Fix.getSightings:    missing 'd' in assumedLongitude!")
        if isinstance(assumedLatitude, str) and assumedLatitude.find("d")>-1 and self.assumedLatiHas_h(assumedLatitude):
            if (not self.assumedLatitudeXisValid(assumedLatitude)) or (
                                                            not self.assumedLatiLongiYdotYisValid(assumedLatitude)):
                raise ValueError("Fix.getSightings:    assumedLatitude with h has X or Y.Y invalid!")
            else:
                strWithout_h=assumedLatitude[1:]
                if strWithout_h=="0d0.0":
                    raise ValueError("Fix.getSightings:    assumedLatitude with h cannot be 0d0.0!")
        if isinstance(assumedLatitude, str) and assumedLatitude.find("d")>-1 and (
                                                                        not self.assumedLatiHas_h(assumedLatitude)):
            if (not self.assumedLatitudeXisValid(assumedLatitude)) or (
                                                            not self.assumedLatiLongiYdotYisValid(assumedLatitude)):
                raise ValueError("Fix.getSightings:    assumedLatitude without h has X or Y.Y invalid!")
            else:
                if assumedLatitude!="0d0.0":
                    raise ValueError("Fix.getSightings:    assumedLatitude without h has to be 0d0.0!")
        
        if isinstance(assumedLongitude, str) and (assumedLongitude.find("d")>-1) and (
                (not self.assumedLongitudeXisValid(assumedLongitude)) or (not self.assumedLatiLongiYdotYisValid(assumedLongitude))):
            raise ValueError("Fix.getSightings:    assumedLongitude X or Y.Y is invalid!")
        # above code have exclude all invalid parameters that is not None
        # what remains are valid string parameters:  
        #         so we can directly use parameter values in our calculation
        if assumedLatitude is not None:
            self.assumedLatitude=assumedLatitude            # is a string
        if assumedLongitude is not None:
            self.assumedLongitude=assumedLongitude          # is a string
        #---- Step 1: Build Sighting Dictionary
        tree=self.buildDOM(self.xmlFileName)
        sightingDict=self.extractSighting(tree) 
        sightingDict=self.adjustedAltitude(sightingDict)
        sightingDict=self.calcGeoLatiLongi(sightingDict)    #goal is: add geoPostions of each sighting to dictionary 
                # update: azimuthAdjustment, distanceAdjustment,  in sightingDic.
        assLaLongTuple=(self.assumedLatitude, self.assumedLongitude)
        sightingDict=self.calculateDistanceAdjustment(sightingDict, assLaLongTuple)
        sightingDict=self.calculateAzimuthAdjustment(sightingDict, assLaLongTuple)
        #---- Step 2: Calculate return value
        self.approximateLatitude=self.calculateApproximateLatitude(sightingDict, assLaLongTuple)
        self.approximateLongitude=self.calculateApproximateLongitude(sightingDict, assLaLongTuple)
        resultTuple=(self.approximateLatitude, self.approximateLongitude)
        #---- Step 3: State Change
        self.writeToLog(sightingDict)
        self.logFileObject=open(self.logFileName,"a")
        self.logFileObject.write("End of sighting file "+self.xmlFileName+"\n") 
        self.logFileObject.close()
        return resultTuple
    
    def calculateApproximateLatitude(self, sightDic, assLaLonTuple):
        sumSighting=0
        #----iterate through sighting dictionary, calculate apprximateLatitude based on error-free sightings        
        for eachSighting in sightDic:
            attributeDict=sightDic.get(eachSighting)
            if attributeDict.get('errorflag')=="False":
                disAjst=attributeDict.get('distance adjustment')
                aziAjst=attributeDict.get('azimuth adjustment')
                disAjst=self.convertAngleStr_AngleFloat(disAjst)
                aziAjst=self.convertAngleStr_AngleFloat(aziAjst)
                sumSighting=sumSighting + disAjst*(math.cos(math.radians(aziAjst)))
        assLati=assLaLonTuple[0]        # is a string
        if self.assumedLatiHas_h(assLati):
            assumedLati_h=assLati[0]
            angleStr=assLati[1:]
            angleFloat=self.convertAngleStr_AngleFloat(angleStr)        #angleStr in form xdy.y
            approximateLatiNum=abs(angleFloat + sumSighting/60.0)
            approximateLati=self.convertAngleFloat_AngleStr(approximateLatiNum)
            approximateLati=assumedLati_h+approximateLati
        else:                   # not self.assumedLatiHas_h
            angleFloat=0.0
            approximateLatiNum=abs(angleFloat+ sumSighting/60.0)
            approximateLati=self.convertAngleFloat_AngleStr(approximateLatiNum)
        return approximateLati  
    
    def calculateApproximateLongitude(self, sightDic, assLaLonTuple): 
        sumSighting=0
        for sightNumber in sightDic:
            attributeDict=sightDic.get(sightNumber)
            if attributeDict.get('errorflag')=="False":
                disAjst=attributeDict.get('distance adjustment')
                aziAjst=attributeDict.get('azimuth adjustment')
                disAjst=self.convertAngleStr_AngleFloat(disAjst)
                aziAjst=self.convertAngleStr_AngleFloat(aziAjst)
                sumSighting=sumSighting +disAjst*(math.sin(math.radians(aziAjst)))
        assLongi=assLaLonTuple[1]        # is a string
        angleStr=assLongi
        angleFloat=self.convertAngleStr_AngleFloat(angleStr)
        approximateLongiNum=angleFloat + sumSighting/60.0
        approximateLongi=self.convertAngleFloat_AngleStr(approximateLongiNum)
        return approximateLongi
    
    def calculateDistanceAdjustment(self, sightDic, assLaLongTuple):   
        for eachSighting in sightDic:
            attributeDic=sightDic.get(eachSighting)
            if attributeDic.get('errorflag')=="False":
                adjustAltitudeStr=attributeDic.get('adjustedAltitude')
                adjustAltitudeFloat=self.convertAngleStr_AngleFloat(adjustAltitudeStr) 
                correctedAltitude=self.calculateCorrectedAltitude(attributeDic, assLaLongTuple)
                result=adjustAltitudeFloat-correctedAltitude
                result_degree=int(result)
                result_minute=round((result-result_degree)*60)
                result=result_degree+ result_minute/60
                distanceAdjust=self.convertAngleFloat_AngleStr(result)
                attributeDic['distance adjustment']=distanceAdjust
            else:
                attributeDic['distance adjustment']="None"
        return sightDic
    
    def calculateAzimuthAdjustment(self, sightDic, assLaLongTuple): 
        for sightNumber in sightDic:
            attributeDic=sightDic.get(sightNumber)
            if attributeDic.get('errorflag')=="False":           
                geoPosiLati=attributeDic.get('geographic position latitude')        # is a string
                assumedLati=assLaLongTuple[0]                                       # is a string
                distanceAdjust=attributeDic.get('distance adjustment')              # is a string
                if self.assumedLatiHas_h(assumedLati):
                    assumedLati_without_h=assumedLati[1:]
                    assumedLati_h=assumedLati[0]
                    x=self.convertAngleStr_AngleFloat(assumedLati_without_h)
                    if assumedLati_h=="S":
                        x=0-x
                else:
                    x=self.convertAngleStr_AngleFloat(assumedLati)
                #---- x=assumedLati; y=geoPosiLati; z=distanceAdjust
                y=self.convertAngleStr_AngleFloat(geoPosiLati)
                z=self.convertAngleStr_AngleFloat(distanceAdjust)
                x=math.radians(x)
                y=math.radians(y)
                z=math.radians(z)
                numerator=math.sin(y) - (math.sin(x)) * (math.sin(z)) 
                denomenator= (math.cos(x)) * (math.cos(z))
                result_radians=math.acos( numerator/denomenator  )
                result=math.degrees(result_radians)
                azimuthAdjust=self.convertAngleFloat_AngleStr(result)
                attributeDic['azimuth adjustment']=azimuthAdjust
            else:
                attributeDic['azimuth adjustment']="None"
        return sightDic
    
    def calculateCorrectedAltitude(self, attributeDic, assLaLongTuple):
        geoPosiLati=attributeDic.get('geographic position latitude')        # is a string
        assumedLati=assLaLongTuple[0]                               # is a string
        if self.assumedLatiHas_h(assumedLati):
            assumedLati_without_h=assumedLati[1:]
            y=self.convertAngleStr_AngleFloat(assumedLati_without_h)        # is a float in degree
            assumedLati_h=assumedLati[0]
            if assumedLati_h=="S":
                y=0-y               # is a float in degree
        else:
            y=self.convertAngleStr_AngleFloat(assumedLati)           
        LHA=self.calculateLHA(attributeDic, assLaLongTuple)         # is a float
        #---- x=geoPosiLati; y=assumedLati
        x=self.convertAngleStr_AngleFloat(geoPosiLati)          # float in degree
        #---- correctedAltitude= arcsin { sin(x)*sin(y) + cos(x)*cos(y)*cos(LHA) }
        x=math.radians(x)
        y=math.radians(y)
        LHA=math.radians(LHA)
        result_radians=math.asin((math.sin(x)) * (math.sin(y))   + (math.cos(x)) * (math.cos(y)) * (math.cos(LHA)) )
        result=math.degrees(result_radians)
        return result
        
    def calculateLHA(self, attributeDic, assLaLongTuple):
        geoPosiLongi=attributeDic.get('geographic position longitude')      # is a string
        assumedLongi=assLaLongTuple[1]              # is a string
        geoPosiLongi_Float=self.convertAngleStr_AngleFloat(geoPosiLongi)
        assumedLongi_Float=self.convertAngleStr_AngleFloat(assumedLongi)
        LHA=geoPosiLongi_Float-assumedLongi_Float
        return LHA
              
    def convertAngleStr_AngleFloat(self,angleStr):
        A=Angle.Angle()
        angleFloat=A.setDegreesAndMinutes(angleStr)
        return angleFloat
    
    def convertAngleFloat_AngleStr(self, angleFloat):
        A=Angle.Angle()
        A.setDegrees(angleFloat)
        angleStr=A.getString()
        return angleStr
    
    def assumedLatiHas_h(self, latiStr):
        if latiStr.find("N")>-1 or latiStr.find("S")>-1:
            return True
        else:
            return False   
    
    def assumedLatitudeXisValid(self, latiStr):
        d_index=latiStr.find("d")
        left_d_Str=latiStr[:d_index]
        if left_d_Str.find("N")>-1 or left_d_Str.find("S")>-1:
            if left_d_Str.find("N")>-1 and left_d_Str.find("S")>-1:
                return False
            elif left_d_Str.find("N")>-1 and left_d_Str.find("S")==-1:
                N_index=left_d_Str.find("N")
                left_N_Str=left_d_Str[:N_index]
                right_N_Str=left_d_Str[N_index+1:]
                if len(left_N_Str)>0:
                    return False
                if not right_N_Str.isdigit():
                    return False
                else:
                    right_N_num=int(right_N_Str)
                    if 0<=right_N_num<90:
                        return True
                    else:
                        return False
            else:
                S_index=left_d_Str.find("S")
                left_S_Str=left_d_Str[:S_index]
                right_S_Str=left_d_Str[S_index+1:]
                if len(left_S_Str)>0:
                    return False
                if not right_S_Str.isdigit():
                    return False
                else:
                    right_S_num=int(right_S_Str)
                    if 0<=right_S_num<90:
                        return True
                    else:
                        return False
        else:
            if not left_d_Str.isdigit():
                return False
            else:
                left_d_num=int(left_d_Str)
                if 0<=left_d_num<90:
                    return True
                else:
                    return False
    
    def assumedLongitudeXisValid(self, longiStr): 
        d_index=longiStr.find("d")
        stringX=longiStr[:d_index]
        if not stringX.isdigit():
            return False
        else:
            numX=int(stringX)
            if 0<=numX<360:
                return True
            else:
                return False
                
    def assumedLatiLongiYdotYisValid(self, latiLongiStr):
        d_index=latiLongiStr.find("d")
        stringYdotY=latiLongiStr[d_index+1:]
        if stringYdotY.find(".")==-1:
            return False
        else:
            dot_index=stringYdotY.find(".")
            leftDotStr=stringYdotY[:dot_index] 
            rightDotStr=stringYdotY[dot_index+1:]
            if (leftDotStr.find(".")>-1) or (rightDotStr.find(".")>-1):
                return False
            elif len(rightDotStr)!=1:
                return False
            elif not rightDotStr.isdigit():
                return False
            elif not leftDotStr.isdigit():
                return False
            else:
                numYdotY=float(stringYdotY)
                if 0.0<=numYdotY<60.0:
                    return True
                else:
                    return False        
            
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
                
            attributeDict['errorflag']=str(errorflag)
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
            if attributeDict.get('errorflag')=="False": 
                observation=attributeDict.get('observation')                    #observation value e.g "045d15.2"
                angleInstance=Angle.Angle()
                observationFloat=angleInstance.setDegreesAndMinutes(observation)
                if observationFloat<0.1:
                    raise ValueError("Fix.getSightings:  observed altitude is LT. 0.1arc-minutes!")   #???sighting error?       
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
            else:
                attributeDict['adjustedAltitude']="None"
        return sightingDict
    
    def calcGeoLatiLongi(self, sightDic):
        if (self.xmlFileName is None) or (self.ariesFile is None) or (self.starFile is None):
            raise ValueError("Fix.getSightings:  sighting file/aries file/star file, has not been set!")
        for sightNum in sightDic:
            attributeDic=sightDic.get(sightNum)
            if attributeDic.get('errorflag')==str(False):
                #---- Part A
                bodyName=attributeDic.get('body')       # is a string
                dateValue=attributeDic.get('date')      # is a string
                resultA=self.findAngularDisplacementOfStarRelativeToAries(bodyName, dateValue)
                SHA_star=resultA[0]         # is a string
                geoPosiLati=resultA[1]      # is a string
                #---- Part B
                timeValue=attributeDic.get('time')      # is a string
                GHA_aries=self.findGHAofAries(dateValue, timeValue)
                #---- Part C
                geoPosiLongi=self.calculateStarGHA(GHA_aries, SHA_star)     # is a string
                #---- write geoPosi to dictionary
                attributeDic['geographic position latitude']=geoPosiLati
                attributeDic['geographic position longitude']=geoPosiLongi
            else:
                attributeDic['geographic position latitude']="None"
                attributeDic['geographic position longitude']="None"
        return sightDic
    
    def calculateStarGHA(self, GHAaries_float, SHAstar_str):
        SHAstar_float=self.convertAngleStr_AngleFloat(SHAstar_str)
        GHAobservation_float=GHAaries_float+SHAstar_float
        GHAobservation_str=self.convertAngleFloat_AngleStr(GHAobservation_float)
        geoPosiLongi=GHAobservation_str
        return geoPosiLongi
    
    def findGHAofAries(self, dateValue, timeValue):
        self.ariesFileObject=open(self.ariesFile,'r')
        ariesFileContent=self.ariesFileObject.readlines()       # a list of lines
        self.ariesFileObject.close()
        hour1=time.strptime(timeValue,"%H:%M:%S")[3]            # is an integer
        dateValue_in_AriesFileFormat=time.strftime("%m-%d-%y", time.strptime(dateValue, "%Y-%m-%d"))
        entry1=self.findGHAentry(ariesFileContent, dateValue_in_AriesFileFormat, hour1)
        hour2=(hour1+1) % 24
        entry2=self.findGHAentry(ariesFileContent, dateValue_in_AriesFileFormat, hour2)
        GHAaries1=entry1.split()[2]         #is a string
        GHAaries2=entry2.split()[2]         #is a string
        time_minutes=time.strptime(timeValue,"%H:%M:%S")[4]
        time_seconds=time.strptime(timeValue,"%H:%M:%S")[5]
        s=time_minutes*60+time_seconds
        GHAaries1=self.convertAngleStr_AngleFloat(GHAaries1)
        GHAaries2=self.convertAngleStr_AngleFloat(GHAaries2)
        GHAaries_float=GHAaries1+ abs(GHAaries2-GHAaries1) * (s/3600.0)
        return GHAaries_float
    
    def findGHAentry(self, list_of_Lines, date_in_AriesFileFormat, hour_int):
        result=None    
        for lineIndex in range(0,len(list_of_Lines)):
            line=list_of_Lines[lineIndex]
            if line.find(date_in_AriesFileFormat):
                alist_of_oneLineContent=line.split()
                hourStr=alist_of_oneLineContent[1]
                if hourStr==str(hour_int):
                    result=line
        return result                 
   
    def findAngularDisplacementOfStarRelativeToAries(self, bodyStr, dateStr):
        #---- return a tuple, (SHAstar, geoPosiLati)
        dateStr=self.convertToDateFormat_in_StarFile_or_AriesFile(dateStr)
        self.starFileObject=open(self.starFile,'r')
        starFileContents=self.starFileObject.readlines()
        self.starFileObject.close()
        listOfLinesWithBodyValue_bodyStr=[]
        for line in starFileContents:
            if line.find(bodyStr)>-1:
                listOfLinesWithBodyValue_bodyStr.append(line)
        exactDateLine=self.findExactDateinList(dateStr, listOfLinesWithBodyValue_bodyStr)
        if exactDateLine is not None:
            starEntryStr=exactDateLine
        else:
            starEntryStr=self.findApproximateDateinList(dateStr, listOfLinesWithBodyValue_bodyStr)
        #---- assign value to result
        starEntry_List=starEntryStr.split()
        SHAstar=starEntry_List[2]           # column 3
        geoPosiLati=starEntry_List[3]         # column 4
        result=(SHAstar, geoPosiLati)       # is a tuple of strings
        return result        
    
    def convertToDateFormat_in_StarFile_or_AriesFile(self, dateStr):
        result=time.strftime("%m/%d/%y", time.strptime(dateStr, "%Y-%m-%d"))
        return result
    
    def findExactDateinList(self, date, list_ofLines):
        result=None
        for index in range(0, len(list_ofLines)):
            line=list_ofLines[index]
            if line.find(date)>-1:
                result=line
        return result
        
    def findApproximateDateinList(self, dateStr, listOfLines):
        #----convert listOfLines to dictionaries with date as key
        dic={}
        for eachElement_Line in listOfLines:
            date=eachElement_Line.split()[1]      
            key=time.strftime("%Y-%m-%d",time.strptime(date, "%m/%d/%y"))          
            dic[key]=eachElement_Line
        orderedList=sorted(dic.items(), key=lambda x: x[0])
        dateStr_ISOformat=time.strftime("%Y-%m-%d",time.strptime(dateStr, "%m/%d/%y"))
        for elementIndex in range(0,len(orderedList)):
            if orderedList[elementIndex][0]>dateStr_ISOformat:
                index=elementIndex-1
                break
        starEntryStr=orderedList[index][1]
        return starEntryStr                                    
        
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
            if element[1].get('errorflag')=="False":
                body=element[1].get('body')
                date=element[1].get('date')
                time=element[1].get('time')
                adjustedAltitude=element[1].get('adjustedAltitude')
                geoPosiLati=element[1].get('geographic position latitude')
                geoPosiLongi=element[1].get('geographic position longitude')
                azimuthAdjustment=element[1].get('azimuth adjustment')
                distanceAdjustment=element[1].get('distance adjustment')
                stringToWrite=body+"\t"+date+"\t"+time+"\t"+adjustedAltitude+"\t"
                stringToWrite=stringToWrite+geoPosiLati+"\t"+geoPosiLongi+"\t"
                stringToWrite=stringToWrite+self.assumedLatitude +"\t" + self.assumedLongitude+"\t"
                stringToWrite=stringToWrite+ azimuthAdjustment+ "\t"+ distanceAdjustment+ "\n"
                self.logFileObject.write(stringToWrite)              
        stringToWrite1="Sighting errors:"+"\t"+str(self.sightingErrors)+"\n"
        self.logFileObject.write(stringToWrite1)
        stringToWrite2="Approximate latitude:"+ "\t"+ self.approximateLatitude+ "\t"
        stringToWrite2=stringToWrite2+ "Approximate longitude:"+ "\t"+ self.approximateLongitude+ "\n"
        self.logFileObject.write(stringToWrite2)
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
    
    def getAssumedLatiLogi(self):
        return (self.assumedLatitude,self.assumedLongitude)
        