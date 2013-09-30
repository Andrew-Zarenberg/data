

from flask import Flask
from flask import render_template
import csv, StringIO
from operator import itemgetter


app = Flask(__name__)
app.debug = True

@app.route("/")
@app.route("/sort/<r>")
def index(r="0"):
    ret = '<table cellspacing="0">'

    data = loadData(int(r))

    totalNum = len(data)

    ret += '<tr><td class="info" colspan="5">Total results: <strong>'+str(totalNum)+'</strong></td></tr>'
    ret += '<tr><th>&nbsp;</th><th>License #</th><th>Last Name</th><th>First Name</th><th>Expiration Date</th></tr>'

    temp = ""
    prev = ""
    curNum = 0
    for x in range(0,len(data)-1):

        cur = data[int(x+1)][int(r)]
        temp += '<tr><td class="num">'+str(x+1)+'</td>'
        
        for k in data[x]:
            temp += "<td>"+k+"</td>"

        temp += "</tr>"

        if cur == prev:
            curNum += 1

        else:

            if curNum > 1:
                perc = "%.3f"%(float(curNum)/totalNum)
                temp = '<tr><td class="info" colspan="5"><span class="infoTitle">'+prev+'</span> - <strong>'+str(curNum)+'</strong> results - <strong>'+perc+'%</strong></td></tr>'+temp


            curNum = 0
            ret += temp
            temp = ""



        prev = cur

    if curNum > 1:
        perc = "%.3f"%(float(curNum)/totalNum)
        temp = '<tr><td class="info" colspan="5"><span class="infoTitle">'+cur+'</span> - <strong>'+str(curNum)+'</strong> results - <strong>'+perc+'%</strong></td></tr>'+temp
        ret += temp

    ret += "</table>"

    return render_template("page.html",d=ret)





def loadData(r):
    data = []
    with open("current_medallion_drivers.csv", "rb") as c:
        read = csv.reader(c, delimiter=',', quotechar='"')
        fir = False
        for row in read:
            if fir:
                temp = []
                for k in range(0,len(row)):
                    if k == 1:
                        spl = row[k].split(",")
                        temp.append(spl[0])
                        temp.append(spl[1])
                    elif k != 2:
                        temp.append(row[k])
                data.append(temp)

            else:
                fir = True

    if r != 0:
        data = sorted(data, key=itemgetter(r))

    return data
            
    

if __name__ == "__main__":
    app.run()

