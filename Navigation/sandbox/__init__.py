# import Navigation.prod.Angle as Angle
# # calculate GHAaries: step1, temp=GHAaries2-GHAaries1
# #                     step2, temp=|temp|---get absolute value
# #                     step3, temp=temp*(s/3600)
# #                     step4, temp=temp+GHAaries1
# #                     step5, GHAaries=temp
#              
# GHAaries1="188d32.5"   
# GHAaries2="203d35"
# s=3014
# SHAstar="243d25.3"
#              
# GHAaries1Angle=Angle.Angle()
# GHAaries1Angle.setDegreesAndMinutes(GHAaries1)
# GHAaries2Angle=Angle.Angle()
# GHAaries2Angle.setDegreesAndMinutes(GHAaries2)
# temp=GHAaries2Angle.subtract(GHAaries1Angle)
# temp=abs(temp)
# print "absolute value of subtraction is: ", temp
# tempAngle0=Angle.Angle()
# tempAngle0.setDegrees(temp)
# print "absolute value of subtraction is: ",tempAngle0.getString()
# temp=temp*(s/3600.0)                      # temp----float
# print "absValue*(s/3600.0)=", temp
# tempAngle1=Angle.Angle()
# tempAngle1.setDegrees(temp)
# temp=tempAngle1.add(GHAaries1Angle)
# GHAaries=temp                           # GHAaries----float
# GHAariesAngle=Angle.Angle()
# GHAariesAngle.setDegrees(GHAaries)
# SHAstarAngle=Angle.Angle()
# SHAstarAngle.setDegreesAndMinutes(SHAstar)
# GHAobservation=GHAariesAngle.add(SHAstarAngle)  # result is float
# print "GHAobservation=",GHAobservation
# GHAobservationAngle=Angle.Angle()
# GHAobservationAngle.setDegrees(GHAobservation)
# longitude=GHAobservationAngle.getString()
# print "longitude=",longitude


# x="2.34.5"
# dot_index=x.find(".")
# print "dot_index=",dot_index
# x1=x[dot_index+1:]
# dot_index2=x1.find(".")
# print "dot_index2=",dot_index2



































