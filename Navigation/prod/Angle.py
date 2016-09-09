import math
from __builtin__ import str

class Angle():
    def __init__(self):
        self.angle = 0.0

    def setDegrees(self, degrees=None):
        if degrees is None:
            degrees = 0.0      
        if(not(isinstance(degrees, int and float))):
            raise ValueError
        self.angle = degrees % 360.0
        return round(self.angle, 1)  
    
    def setDegreesAndMinutes(self, angleString):
        separator = "d"
        index = angleString.find(separator)
        if index == -1:
            raise ValueError
        X = angleString[:index]  # degree as substring
        Y = angleString[(index + 1):]  # minutes as substring
        # now need to determine if X is legal? if illegal, raise a ValueError
        if self.isLegal_X(X) == False:
            raise ValueError
        # now need to determine if Y is legal? if illegal, raise a ValueError
        if self.isLegal_Y(Y) == False:
            raise ValueError
        # if both legal, set the degree&minutes, return value as format"45.0" 
        degree = int(X)
        minutes = float(Y)
        self.angle = round((degree % 360 + minutes / 60), 1)
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
        
    def add(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError
        self.angle = (self.angle + angle.angle) % 360.0
        return self.angle
    
    def subtract(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError
        self.angle = (self.angle - angle.angle) % 360.0
        return self.angle
    
    def compare(self, angle):
        if not(isinstance(angle, Angle)):
            raise ValueError
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
        degree = round(self.angle, 1)
        return degree
    
