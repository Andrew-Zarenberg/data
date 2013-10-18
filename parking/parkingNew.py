

#####
#
#  ANDREW ZARENBERG
#
#  SOFTDEV PERIOD 6
#
#####




from flask import Flask
from flask import render_template, request
import csv, StringIO, re
from operator import itemgetter
import signs



signsSkip = ["METERS ARE NOT IN EFFECT ABOVE TIMES"]
signsIgnore = ["Curb Line","Property Line","Building Line"]
signsNoStanding = ["NO STANDING",
                   "BUS STOP",
                   "NO STOPPING",
                   "DIPLOMAT",
                   "HANDICAP BUS",
                   "AMBULETTE",
                   "BUS LAYOVER AREA"]
signsNoParking = ["NO PARKING"]
signsHourParking = ["HOUR PARKING","HR MUNI-METER"]
signsAnytime = ["ANYTIME"]







app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    r = """
<form action="/search" method="get">
<table>
<tr>
<th>Borough</th>
<td><select name="borough">
<option value="K">Brooklyn</option>
<option value="M" selected>Manhattan</option>
<option value="Q">Queens</option>
<option value="S">Staten Island</option>
<option value="B">The Bronx</option>
</select></td>
</tr><tr>
<th>Street</th>
<td><input name="street" size="25" /></td>
</tr>
<tr>
<th>Time</th>
<td><select name="time">
"""
    
    for x in range(0,47):
        r += '<option value="'+str(x)+'">'+timeToStr(x*30)+'</option>'

    r += """
</select></td>
</tr>
<tr>
<td colspan="2" style="text-align:center;"><input type="submit" value="Search" /></td>
</tr>
</table>
</form>
"""
    return render_template("page.html",d=r)


@app.route("/search")
def search():

    borough = request.args.get("borough")
    if borough == None:
        borough = "M"

    street = request.args.get("street")
    if street == None:
        street = "YORK AVENUE"

    streets = loadStreets(borough,street)
    signs = loadSigns()

    r = ""
#    streets["E"] = sortStreets(streets["E"])
    
#    streets["N"] = sortStreets(streets["N"])

    
    r += str(streets["E"][0])        

    r += createSign(signs[streets["E"][0][1]],"E")


    return render_template("s2.html",d=r)



def loadStreets(borough, street):
    data = {
        "N":[],
        "S":[],
        "E":[],
        "W":[]
        }
    with open("streets.csv", "rb") as c:
        read = csv.reader(c, delimiter=',', quotechar='"')

        for row in read:
            if street == row[2] and row[0] == borough:
                data[row[5]].append(row)

#    for k in data:
#        k = sorted(k, key=itemgetter(0,2))

    return data


def loadSigns():
    data = []
    with open("signs.csv", "rb") as c:
        read = csv.reader(c, delimiter=',', quotechar='"')

        for row in read:
            data.append(row)

    data = sorted(data, key=itemgetter(1))

    ret = {}
    prev = ""
    for n in data:
        if n[1] != prev:
            ret[n[1]] = [n]
            prev = n[1]
        else:
            ret[n[1]].append(n)


    return ret


def sortStreets(d):

    for line in d:
        d.append(0)

    d[0][6] = len(d)



    for one in range(0,len(d)):
        for two in range(one+1,len(d)):
            if one != two:# and len(d[one]) == 6 and len(d[two]) == 5:
                if d[one][4] == d[two][3]:   # if ONE END == TWO START
                    d[two][6] = d[one][6]+1
                    #d[two].append(d[one][6]+1)
                    temp = d[two]
                    d.remove(d[two])
                    d.insert(one+1,temp)
                elif d[one][3] == d[two][4]: # if TWO END == ONE START
                    d[two][6] = d[one][6]-1
#                    d[two].append(d[one][6]-1)
                    temp = d[two]
                    d.remove(d[two])
                    d.insert(one+1,temp)


    return sorted(d, key=itemgetter(6), reverse=False)

    
            
def createSign(n,side):
    r = "<br />"
    for line in n:
        if not inArray(signsIgnore, line[5]):
            r += formatItem(line,side)+"<br />"

    return r


def formatItem(n,s):
    # s = side of street
    # ar = arrow pointing

    ar = re.sub('\s+',"",n[4])
    s = re.sub('\s+',"",s)
    r = str(n)+":<br />"
    a = n[5] # data to parse into sign

    d = {
        "limit":"",
        "time1":"",
        "time1ap":"PM",
        "time2":"",
        "time2ap":"PM",
        "days":2,
        "arrow":2
        }

    
    r += "<span style='color:red;font-weight:bold;'>"+s+" - "+ar+"</span>"
    # ARROW DIRECTION
    if re.sub('\s+',"",ar) == "":
        d["arrow"] = 2
    elif (s == "N" and ar == "E") or (s == "E" and ar == "S") or (s == "S" and ar == "W") or (s == "W" and ar == "N"):
        d["arrow"] = 1
    else:
        d["arrow"] = 0



    
    ak = a.split("-")
    r += str(ak)+" #<br />"

    
    
    if "NO STANDING ANYTIME" in a and "TAXI" in a:
        d = signs.formatData(d)
        r += signs.noStandingAnytimeTaxi(d)
        return r




    if re.match('\d+ HR MUNI',a):
        d["limit"] = a.split(" HR MUNI")[0]
    elif re.match('\d+ HOUR PARKING',a):
        d["limit"] = a.split(" HOUR PARKING")[0]

    if "EXCEPT SUNDAY" in a or "EXCEPT SUN" in a:
        d["days"] = 2
    elif "ANYTIME" in a:
        d["days"] = 1

    spl = re.split('\s+',a)
    for aa in spl:
        if "-" in aa:
            ak = aa.split("-")
            if re.match('\d+',ak[0]) and re.match('\d+',ak[1]):
                d["time1"] = re.sub('[A-Z]+','',ak[0])
                d["time2"] = re.sub('[A-Z]+','',ak[1])
                d["time1ap"] = re.sub('\d+','',ak[0])
                d["time2ap"] = re.sub('\d+','',ak[1])

                if("AM" not in d["time1ap"] and "PM" not in d["time1ap"]):
                    d["time1ap"] = d["time2ap"]


    d = signs.formatData(d)

    if inArray(signsNoParking,a):
        r += signs.noParking(d)

    elif inArray(signsNoStanding, a):
        r += signs.noStanding(d)

    elif inArray(signsHourParking,a):
        r += signs.meteredParking(d)


    return r

    



        






# Utility functions

def inArray(array,string):
    for n in array:
        if n in string:
            return True
        
    return False


def strToTime(n):
    hour = 0
    minute = 0

    if "PM" in n:
        hour = 12

    n = n.replace("AM","").replace("PM","")

    spl = n.split(":")
    hour += int(spl[0])
    
    if len(spl) > 1:
        minute = int(spl[1])

    return hour*60+minute


def timeToStr(n):
    hour = n/60
    minute = str(n%60)

    if len(minute) == 1:
        minute = "0"+minute

    ti = "AM"
    if hour > 11:
        ti = "PM"

    if hour > 12:
        hour -= 12

    if hour == 0:
        hour = 12

    return str(hour)+":"+minute+ti



if __name__ == "__main__":
    app.run()
