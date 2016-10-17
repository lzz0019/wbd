# import xml.dom.minidom
# DOMTree=xml.dom.minidom.parse("test1.xml")
# collection=DOMTree.documentElement
# sightings=collection.getElementsByTagName("sighting")
# sightingList=[]
#    
# for sighting in sightings:
#     date=sighting.getElementsByTagName("date")
#     body=sighting.getElementsByTagName("body")
#     x=sighting.getElementsByTagName("x")
#     print len(x)
#     dateValue=date[0].firstChild.nodeValue
#     bodyValue=body[0].firstChild.nodeValue
#     attributeTuple=(dateValue, bodyValue, sighting)
#     sightingList.append(attributeTuple)
#    
# print "sightingList before sorting: "    
# for element in sightingList:
#     print element
# orderedList=sorted(sightingList, key=lambda x: (x[0],x[1]))
# print "sightingList after sorting"
# for element in orderedList:
#     print element
     
 
# student_tuples = [
#         ('john', 'A', 15, None),
#         ('jane', 'B', 12, None),
#         ('dave', 'B', 10, None),
#         ('li', 'A', 10, None),
#         ('Jack', 'A',12, None)
# ]
# b=sorted(student_tuples, key=lambda x: (x[2],x[1]))
# print len(b)
# print b[0]
# print b[1]
# print b[2]
# print b[3]
# print b[4]

# sightingDict={}
# sightingDict['age']=11
# sightingDict['name']='John'
# print "sightingDict['age']",sightingDict['age']
# print "sightingDict['name']",sightingDict['name']
# 
# import datetime
# print datetime.datetime.now().isoformat()
# print datetime.datetime.utcnow().isoformat()

# #SORT DICTIONARY
# dict={1:{'body':'Peacock', 'date': '2016-03-02', 'time': '00:05:05'},
#       2:{'body':'Aldebaran', 'date':'2016-03-01', 'time':'23:40:01'},
#       3:{'body':'Beck', 'date':'2016-03-02','time':'00:05:05'}
#       }
# list=dict.items()
# print "Value : %s" %  list
# print list[0][1].get('body')
# newList=sorted(list, key=lambda x: (x[1].get('date'),x[1].get('body')))
# print "newList is:"
# print "Value : %s" %  newList
# result={}
# for element in newList:
#     key=element[0]
#     print key
#     value=element[1]
#     print value
#     result[key]=value
# print "result dictionary is: "
# print "Value : %s" %  result

import Navigation.prod.Fix as Fix

fixInst=Fix.Fix()
DOMTree=fixInst.buildDOM("test1.xml")
collection=DOMTree.documentElement
sightings=collection.getElementsByTagName("sighting")       # sightings is a list
print "len(sightings)=",len(sightings)
print sightings[0]
print sightings[1]
print sightings[2]
sightingDict={}   
i=1                                     # create a sighting dictionary 
for sighting in sightings:
    attributeDict={}
    sightingDict[i]=attributeDict
    body=fixInst.extractElement("body", sighting)
    print "body=",body
    
#             date=self.extractElement("date", sighting)           
#             time=self.extractElement("time", sighting)
#             observation=self.extractElement("observation", sighting)
#             height=self.extractElement("height", sighting)
#             print "height0=",height










































