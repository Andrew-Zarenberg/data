

from flask import Flask, render_template
import signs

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
#    return render_template("signs.html")


    r = """
<html><head>
    <style type="text/css">
      body {
         font-family:Arial,Verdana;
      }

      .sign {
         border-width:5px;
         border-style:solid;
         font-weight:bold;
         padding:0;
         width:237px;
         font-size:23px;
         color:white;
      }
      
      .td_topLeft {
         font-size:48px;
         padding:7px 7px 7px 0;
         color:white;
         width:50px;
         text-align:center;
      }

      .td_header, .td_headerSmall {
         text-align:center;
         vertical-align:bottom;
         padding-top:10px;
      }
      .td_header, .td_anytime { 
         font-size:30px; 
         vertical-align:top;
      }
      .td_headerSmall { font-size:18px; }
      .td_anytime { text-align:center; }

      .td_time {
         text-align:center;
         vertical-align:top;
         padding-top:10px;
      }

      .td_holder { font-size:5px; }
         
      .td_time span { vertical-align:middle }
      .td_arrow { 
         text-align:center; 
         padding-bottom:10px; 
      }


      .number, .dash { font-size:31px; }
      .day { font-size:23px; }
      .ampm {
         font-size:12px; 
         padding-top:8px;
      }
      .thru {
         font-size:12px;
         padding-left:5px;
         padding-right:5px;
      }

      .exceptSunday { 
         color:white; 
         padding-top:2px;
         padding-bottom:2px;
         margin-left:4px;
         margin-right:4px;
      }

      .noParking .td_topLeft, .noParking .exceptSunday { background:#94272D; }
      .noParking { 
         color: #94272D; 
         border-color:#94272D;
      }

      .meterParking .td_topLeft, .meterParking .exceptSunday { background:#034F28; }
      .meterParking { 
         color:#034F28; 
         border-color:#034F28;
      }

      .noStanding {
         background:#B50F03; 
         border:2px solid gray; 
      }


     

    </style>

</head><body>"""

    d = {
        "limit":2,
        "time1":5,
        "time1ap":"AM",
        "time2":10,
        "time2ap":"PM",
        "days":2,#[0,"MON","FRI"],
        "arrow":1
        }

    data = signs.formatData(d)


    r += signs.meteredParking(data)
    r += "<br /><hr /><br />"
    r += signs.noParking(data)
    r += "<br /><hr /><br />"
    r += signs.noParkingAnytime(data)
    r += "<br /><hr /><br />"
    r += signs.noStanding(data)
    r += "<br /><hr /><br />"
    r += signs.noStandingAnytime(data)


    r += """</body></html>"""

    return r

if __name__ == "__main__":
    app.run()
