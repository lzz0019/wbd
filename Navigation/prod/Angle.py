'''
Created on Sep 4, 2016

@author: lzz0019
'''

import math
from __builtin__ import str

class Angle():
    def __init__(self):
        self.angle = 0.0

    def setDegrees(self, degrees=None):
        if degrees is None:
            degrees = 0.0
        elif(not isinstance(degrees, int)  and not isinstance(degrees, float)):
            raise ValueError("Angle.setDegrees: The input should be an integer or a float!")
        else:
            self.angle = degrees % 360.0
        return self.angle 
    
    def setDegreesAndMinutes(self, angleString):
        separator = "d"
        index = angleString.find(separator)
        if index == -1:
            raise ValueError("Angle.setDegreesAndMinutes: Missing separator!")
        X = angleString[:index]  # degree as substring
        Y = angleString[(index + 1):]  # minutes as substring
        # now need to determine if X is legal? if illegal, raise a ValueError
        if self.isLegal_X(X) == False:
            raise ValueError("Angle.setDegreesAndMinutes: Degree portion of angleString is illegal!")
        # now need to determine if Y is legal? if illegal, raise a ValueError
        if self.isLegal_Y(Y) == False:
            raise ValueError("Angle.setDegreesAndMinutes: Minute portion of angleString is illegal!")
        # if both legal, set the degree&minutes, return value as format"45.0" 
        degree = int(X)
        minutes = float(Y)
        self.angle = (degree % 360)+ (minutes / 60)
        return self.angle
    
    def isLegal_X(self, X):
        try:
            int(X)
            return True
        except ValueError:
            return False  
    
    def isLegal_Y(self, Y):
        try:
            fl = float(Y)       
        except ValueError:
            return False     
        if fl < 0:
            return False
        if Y[::-1].find('.') > 1:  # Y is a string of minutes
            return False
        else:
            return True
        
    def add(self, angle=None):
        if angle is None:
            raise ValueError("Angle.add: missing parameter!")
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.add: angle is not an instance of Angle!")
        self.angle = (self.angle + angle.angle) % 360.0
        return self.angle
    
    def subtract(self, angle=None):
        if angle is None:
            raise ValueError("Angle.subtract: missing parameter!")
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.subtract: angle is not an instance of Angle!")
        self.angle = (self.angle - angle.angle) % 360.0
        return self.angle
    
    def compare(self, angle=None):
        if angle is None:
            raise ValueError("Angle.compare: missing parameter!")
        if not(isinstance(angle, Angle)):
            raise ValueError("Angle.compare: angle is not an instance of Angle!")
        if self.angle < angle.angle:
            return -1
        elif self.angle == angle.angle:
            return 0
        else:
            return 1
    
    def getString(self):
        tuple = math.modf(self.angle)
        Y = round(tuple[0] * 60.0, 1)
        X = int(tuple[1])
        string = str(X) + "d" + str(Y)
        return string
    
    def getDegrees(self):
        return self.angle
    
