

from flask import Flask
from flask import render_template, request
import csv, StringIO
from operator import itemgetter


app = Flask(__name__)
app.debug = True



maxBarWidth = 700


signsBlack = ["Curb Line","Property Line","Building Line"]
signsNoStanding = ["NO STANDING ANYTIME",
                   "BUS STOP",
                   "NO STOPPING ANYTIME",
                   "DIPLOMAT",
                   "HANDICAP BUS",
                   "AMBULETTE",
                   "NO STANDING HOTEL LOADING ZONE",
                   "NO STANDING /BUS",
                   "BUS LAYOVER AREA"]
signsNoParking = ["NO PARKING ANYTIME"]
signsHourParking = ["HOUR PARKING","HR MUNI-METER"]
signsFreeParking = ["(SANITATION BROOM SYMBOL)"]
signsCheckNext = ["NO PARKING"]#,"Building Line"]


@app.route("/")
def index():
    r = ""

    borough = "M"
    street = request.args.get("street")#"34 STREET"

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

    r = "<strong>"+street[2]+" ["+street[5]+"] between "+street[3]+" and "+street[4]+"</strong> <em>(ID: "+street[1]+")</em><ul>"

    for n in signs:
        r += "<li>"+n[5]+"</li>"

    r += "</ul>"

    return r



def parkingArray(street,signs):    

    # 0 = black
    # 1 = No Standing
    # 2 = No Parking
    # 3 = Hour Parking
    # 4 = Free Parking


    r = []
    signs.sort(key=lambda x:int(x[2]))

    totalDist = int(signs[len(signs)-1][3])

    prev = 0
    prevTotal = 0

    count = 0
    
    prevWidth = 0


    for x in range(0,len(signs)):

        n = signs[x]

        width = int(n[3])-prev+prevWidth
        prevWidth = 0
        

        if width > 0:

            tmp = ["",prev,width]

            if inArray(signsBlack,n[5]):
                if count == 0:
                    prevWidth = width
                elif x+1 == len(n):
                    r[len(r)-1][2] += width
                continue
            elif inArray(signsNoStanding,n[5]):
                tmp[0] = "noStanding"
            elif inArray(signsNoParking,n[5]):
                tmp[0] = "noParking"
            elif inArray(signsHourParking,n[5]):
                tmp[0] = "hourParking"
            elif inArray(signsFreeParking,n[5]) and len(signs) > x and not inArray(signsHourParking,signs[x+1][5]):
                tmp[0] = "freeParking"
            elif inArray(signsCheckNext,n[5]) and len(signs) > x and inArray(signsHourParking,signs[x+1][5]):
                tmp[0] = "hourParking"
    
            if len(r) > 0 and r[count-1][0] == tmp[0]:
                r[count-1][2] = r[count-1][2]+width
            else:
                r.append(tmp)
                count += 1    
        
            prevTotal += width
                
            prev = int(n[3])        
                


    

    return r



def parkingbar(street,signs):
    n = parkingArray(street,signs)

    r = genSign(street,signs)
    r += '<div class="street"><div class="stinfo">'+street[3]+'</div>'

    total = 0
    for x in range(0,len(n)):
        r += '<div class="bar '+n[x][0]+'" style="width:'+str(n[x][2])+'px;margin-left:'+str(n[x][1])+'px;">&nbsp;</div>'
        total += n[x][2]

    k = str(total)
#    k = str(n[len(n)-1][1]+n[len(n)-1][2])
    r += '<div>&nbsp;</div><div class="stinfo" style="text-align:right;width:'+k+'px">'+street[4]+'</div></div>'

    return r


def parkingbar2(street,signs):
    r = genSign(street,signs)
    r += '<div class="street"><div class="stinfo">'+street[3]+'</div>'



    #signs = sorted(signs, key=itemgetter(2))
    signs.sort(key=lambda x:int(x[2]))

    totalDist = int(signs[len(signs)-1][3])

    prev = 0
    prevTotal = 0


    for x in range(0,len(signs)):

        n = signs[x]

        width = int(n[3])-prev


#        width = int((float(n[3])-prev)/totalDist*barWidth)
#        width = int((float(n[3])-prev)/totalDist)
        #r += '<div>'+n[3]+' - '+str(totalDist)+' - '+str(n)+'</div>'


        className = ""
#        if "Curb Line" in n[5] or "Property Line" in n[5]:



        if inArray(signsBlack,n[5]):
            className = "barEnd"
#        elif "NO STANDING ANYTIME" in n[5] or "BUS STOP" in n[5]:
        elif inArray(signsNoStanding,n[5]):
            className = "noStanding"
#        elif "NO PARKING ANYTIME" in n[5]:
        elif inArray(signsNoParking,n[5]):
            className = "noParking"
#        elif "HOUR PARKING" in n[5]:
        elif inArray(signsHourParking,n[5]):
            className = "hourParking"
        elif inArray(signsFreeParking,n[5]) and len(signs) > x and not inArray(signsHourParking,signs[x+1][5]):
            className = "freeParking"
        elif inArray(signsCheckNext,n[5]) and len(signs) > x and inArray(signsHourParking,signs[x+1][5]):
            className = "hourParking"


#        r += '<div class="bar '+className+'" style="width:'+str(width)+'px;margin-left:'+str(prevTotal)+'px;">&nbsp;</div>'
        r += '<div class="bar '+className+'" style="width:'+str(width)+'px;margin-left:'+str(prevTotal)+'px;">&nbsp;</div>'
        
#        prev = int(n[3])
        prevTotal += width





        prev = int(n[3])        


    r += '<div>&nbsp;</div><div class="stinfo" style="text-align:right;width:'+str(prev)+'px">'+street[4]+'</div></div>'

    return r



def inArray(array,string):
    for n in array:
        if n in string:
            return True
        
    return False




if __name__ == "__main__":
    app.run()
