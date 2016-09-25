# '''
# Created on Sep 4, 2016
# 
# @author: lzz0019
# '''
# 
# import Navigation.prod.Angle as Angle
# #----Constructor----
# angle1=Angle.Angle()
# angle2=Angle.Angle()
# angle3=Angle.Angle()
# angle4=Angle.Angle()
# 
# #----setDegrees() Exception Test Case----
# angle1Degrees=angle1.setDegrees()
# print angle1Degrees
#  
# #----setDegreesAndMinutes() Normal Test Case----
# angle1Degrees=angle1.setDegreesAndMinutes("45d10.1")
# print "45d010.1 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("45d10")
# print "45d10 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("0d0")
# print "0d0 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("0d0.1")
# print "0d0.1 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("700d1")
# print "700d1 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("700d61")
# print "700d61 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("-10d0")
# print "-10d0 angle result is: ", angle1Degrees
# angle1Degrees=angle1.setDegreesAndMinutes("-10d1")
# print "-10d1 angle result is: ", angle1Degrees
#  
# #----setDegreesAndMinutes() Exception Test Case----
# angle1Degrees=angle1.setDegreesAndMinutes("d10.0")
# angle1Degrees=angle1.setDegreesAndMinutes("10d")
# angle1Degrees=angle1.setDegreesAndMinutes("10")
# angle1Degrees=angle1.setDegreesAndMinutes("0.1d0")
# angle1Degrees=angle1.setDegreesAndMinutes("0d-10")
# angle1Degrees=angle1.setDegreesAndMinutes("0d5.44")
# angle1Degrees=angle1.setDegreesAndMinutes("xd10")
# angle1Degrees=angle1.setDegreesAndMinutes("10dy")
# angle1Degrees=angle1.setDegreesAndMinutes("10:30")
# angle1Degrees=angle1.setDegreesAndMinutes("")
#  
# #----add() Normal Test Case----
# print "angle1=", angle1.setDegreesAndMinutes("45d0")
# print "angle2=", angle2.setDegreesAndMinutes("340d30")
# print "angle3=", angle3.setDegreesAndMinutes("0d30")
# addedDegrees1=angle1.add(angle2)
# print "addedDegrees1=", addedDegrees1
# addedDegrees3=angle2.add(angle3)
# print "addedDegrees3=", addedDegrees3
# 
# #----add() Exception Test Case----
# print "angle1=", angle1.setDegreesAndMinutes("45d0")
# angle1.add("42d0")
# angle1.add(42.5)
#  
# #----subtract() Normal Test Case----
# print "angle4=", angle4.setDegreesAndMinutes("0d0")
# print "angle1=", angle1.setDegreesAndMinutes("25d30")
# subtractedDegrees=angle4.subtract(angle1)
# print "subtractedDegrees=", subtractedDegrees
#  
# #----subtract() Exception Test Case----
# print "angle1=", angle1.setDegreesAndMinutes("25d30")
# angle1.subtract(0.0)
# angle1.subtract("0d0")
#  
# #----compare() Normal Test Case----
# print "angle1=", angle1.setDegrees(45.4)
# print "angle2=", angle2.setDegrees(45.1)
# result=angle1.compare(angle2)
# print "angle1.compare(angle2)=", result
#  
# #----compare() Exception Test Case----
# print "angle1=", angle1.setDegrees(45.4)
# angle1.compare(42.0)
# angle1.compare("42d0")
#  
# #----getString() Normal Test Case----
# print "angle1=", angle1.setDegrees(45.0)
# angle1String=angle1.getString()
# print "angle1String is: ", angle1String
# print "angle2=", angle2.setDegrees(45.1)
# angle2String=angle2.getString()
# print "angle2String is: ", angle2String
# print "angle3=", angle3.setDegrees(45.123)
# angle3String=angle3.getString()
# print "angle3String is: ", angle3String
#  
# #----getDegrees() Normal Test Case----
# print "angle1=", angle1.setDegrees(45.0)
# print "angle2=", angle2.setDegrees(45.1)
# print "angle3=", angle3.setDegrees(45.123)
# print "angle1Degrees=", angle1.getDegrees()
# print "angle2Degrees=", angle2.getDegrees()
# print "angle3Degrees=", angle3.getDegrees()