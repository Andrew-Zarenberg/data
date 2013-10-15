

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


app = Flask(__name__)
app.debug = True



maxBarWidth = 700

signsSkip = ["METERS ARE NOT IN EFFECT ABOVE TIMES"]
signsBlack = ["Curb Line","Property Line","Building Line"]
signsNoStanding = ["NO STANDING",
                   "BUS STOP",
                   "NO STOPPING",
                   "DIPLOMAT",
                   "HANDICAP BUS",
                   "AMBULETTE",
                   "BUS LAYOVER AREA"]
signsNoParking = ["NO PARKING"]
signsHourParking = ["HOUR PARKING","HR MUNI-METER"]
#signsFreeParking = ["(SANITATION BROOM SYMBOL)"]
signsCheckNext = ["NO PARKING"]#,"Building Line"]


dayArray = ["SUN","MON","TUES","WED","THURS","FRI","SAT"]



@app.route("/")
def index():
    r = ""

    borough = "M"
    street = request.args.get("street")

    streets = loadStreets(borough,street)

    signs = loadSigns()

    r = str(len(streets))+" - "+str(len(signs))

#    r += "<hr />"+genSign(streets[0],signs[streets[0][1]])
    
    for x in range(0,len(streets)):
        if streets[x][1] in signs.keys():
            r += "<hr />"+parkingbar(streets[x],signs[streets[x][1]])

    return render_template("page.html",d=r)


def loadStreets(borough, street):
    data = []
    with open("streets.csv", "rb") as c:
        read = csv.reader(c, delimiter=',', quotechar='"')

        for row in read:
            if street in row[2] and row[0] == borough:
                data.append(row)

    data = sorted(data, key=itemgetter(0,2))


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
            #if not n[5] in signIgnore:
            ret[n[1]] = [n]
            prev = n[1]
        else:
            #if not n[5] in signIgnore:
            ret[n[1]].append(n)


    return ret



def genSign(street,signs):

    r = '<div class="parkingHeader"><strong>'+street[2]+' ['+street[5]+'] between '+street[3]+' and '+street[4]+'</strong> <em>(ID: '+street[1]+')</em></div><div class="genParking"><ul>'

    for n in signs:
        r += "<li>"+n[5]+"</li>"

    r += "</ul>"

    r += '</div>'

    return r



def parkingArray(street,signs):    

    # 0 = black
    # 1 = No Standing
    # 2 = No Parking
    # 3 = Hour Parking
    # 4 = Free Parking


    r = [0]
    signs.sort(key=lambda x:int(x[2]))

    totalDist = int(signs[len(signs)-1][3])

    prev = 0
    prevTotal = 0

    count = 1
    
    prevWidth = 0


    for x in range(0,len(signs)):

        n = signs[x]


        width = int(n[3])-prev+prevWidth
        prevWidth = 0
        

#        if width > 0:
        if True:

            spl = re.split('\s+',n[5])#.split(" ")

            times = []
            days = []
            
            for aa in spl:
                if aa in dayArray:
                    days.append(dayArray.index(aa))
                elif "-" in aa:
                    ak = aa.split("-")
                    if re.match('\d+',ak[0]) and re.match('\d+',ak[1]):
                        times.append(strToTime(ak[0]))
                        times.append(strToTime(ak[1]))


#            print(str(times))
#            if days or times:
#                print(str(days)+" === "+str(times))

            tmp = ["",prev,width,times]


            tmp[0] = getClassName(n[5])
            if not tmp[0]:
                continue
            
            if width <= 0 and tmp[0] == "hourParking" and len(r) > 1:
                tmp[1] = r[count-1][1]
                tmp[2] = r[count-1][2]

#            if inArray(signsBlack,n[5]):
#                if count == 0:
#                    prevWidth = width
#                elif x+1 == len(n):
#                    r[len(r)-1][2] += width
#                continue
#            elif inArray(signsNoStanding,n[5]):
#                tmp[0] = "noStanding"
#            elif inArray(signsNoParking,n[5]):
#                tmp[0] = "noParking"
#            elif inArray(signsHourParking,n[5]):
#                tmp[0] = "hourParking"
#            elif inArray(signsCheckNext,n[5]) and len(signs) > x and inArray(signsHourParking,signs[x+1][5]):
#                tmp[0] = "hourParking"
    
            if len(r) > 1 and r[count-1][0] == tmp[0]:
                r[count-1][2] = r[count-1][2]+width
            else:
                r.append(tmp)
                count += 1    
        
            prevTotal += width
                
            prev = int(n[3])        
                

    r[0] = str(prevTotal)
    

    return r



def parkingbar(street,signs):
    n = parkingArray(street,signs)

    
    times = [0] # start at 0
    for aa in range(1,len(n)):
        if len(n[aa][3]) > 0:
            for bb in n[aa][3]:
                if not bb in times:
                    times.append(bb)

    times.append(1440) # end of day


    times.sort()
    

    r = genSign(street,signs)
#    r += '<div>'+str(n)+'</div>'

    r += '<table class="streetHolder">'
#    r += <tr><td colspan="2">'+str(times)+'</td></tr>'

    tmp = []
    for z in range(0,len(times)-1):
        tmp.append([])
        count = 0
        for x in range(1,len(n)):
            if len(n[x][3]) == 0 or (times[z] >= n[x][3][0] and times[z+1] <= n[x][3][1]):
                if count > 0 and tmp[z][count-1][0] == n[x][0]:
                    tmp[z][count-1][2] = tmp[z][count-1][2]+n[x][2]
                else:
                    tmp[z].append(n[x])
                    count += 1




    for z in range(0,len(times)-1):

        r += '<tr>'
#        r += '<div class="stinfo">'+street[3]+'</div>'
        r += '<td class="time">'+timeToStr(times[z])+' - '+timeToStr(times[z+1])+'</td>'
        r += '<td class="parkingbar">'
        
        r += '<div class="bar" style="width:'+n[0]+'px">&nbsp;</div>'

        total = 0
#        tmp = ""

#        for x in range(1,len(n)):
#            if len(n[x][3]) == 0 or (times[z] >= n[x][3][0] and times[z+1] <= n[x][3][1]):
#                tmp += '<div class="bar '+n[x][0]+'" style="width:'+str(n[x][2])+'px;margin-left:'+str(n[x][1])+'px;">&nbsp;</div>'
#                total += n[x][2]

        for a in tmp[z]:
            r += '<div class="bar '+a[0]+'" style="width:'+str(a[2])+'px;margin-left:'+str(a[1])+'px;">&nbsp;</div>'

        k = str(total)

#        r += tmp

        r += '<div>&nbsp;</div>'
#        r += '<div class="stinfo" style="text-align:right;width:'+k+'px">'+street[4]+'</div>'
        r += '</td></tr>'
        
    r += '</table>'

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

    
def getClassName(n):
    if inArray(signsNoStanding,n):
        return "noStanding"
    elif inArray(signsNoParking,n):
        return "noParking"
    elif inArray(signsHourParking,n):
        return "hourParking"
    elif inArray(signsHourParking,n):
        return "hourParking"
    else:
        return None



if __name__ == "__main__":
    app.run()
