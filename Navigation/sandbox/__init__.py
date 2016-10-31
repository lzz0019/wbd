import time
from __builtin__ import str

# date=" 2016-03-01"
# try:
#     time.strptime(date, " %Y-%m-%d")
#     print "True"
# except:
#     print "False"

timeStr="23:40:01"
try:
    time.strptime(timeStr,"%H:%M:%S")
    print "True"
except:
    print "False"













































