


def main():
    d = {
        "time1":"4",
        "time1ap":"PM",
        "time2":"7",
        "time2ap":"PM",
        "days":[0,"MON","FRI"],
        "arrow":0
        }

    
    print(noStanding(formatData(d)))








##########
##
##  METERED PARKING START
##
##########


def meteredParking(d):
    return """
	  <table class="sign meterParking" cellspacing="0">
	    <tr>
	      <td class="td_topLeft" rowspan="2">%(limit)s</td>
	      <td class="td_headerSmall">HOUR PARKING</td>
	    </tr>
	    <tr>
	      <td class="td_time" rowspan="2">
		<div>
		  <span class="number">%(time1)s</span>
		  <span class="ampm">%(time1ap)s</span>
		  <span class="dash">-</span>
		  <span class="number">%(time2)s</span>
		  <span class="ampm">%(time2ap)s</span>
		</div>
	      </td>
	    </tr>
	    <tr>
	      <td class="td_holder">&nbsp;</td>
	    </tr>
	    <tr>
	      <td class="td_time" colspan="2">
		%(days)s
	      </td>
	    </tr>
	    <tr>
	      <td class="td_arrow" colspan="2">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)


##########
##
##  METERED PARKING END
##
##########


##########
## 
##  NO PARKING START
##
##########


# NO PARKING HOURS/DAYS
def noParking(d):
    if d["days"] == 1:
        return noParkingAnytime(d)
    else:
        return """
	  <table class="sign noParking" cellspacing="0">
	    <tr>
	      <td class="td_topLeft" rowspan="2">NO</td>
	      <td class="td_header">PARKING</td>
	    </tr>
	    <tr>
	      <td class="td_time" rowspan="2">
		<div>
		  <span class="number">%(time1)s</span>
		  <span class="ampm">%(time1ap)s</span>
		  <span class="dash">-</span>
		  <span class="number">%(time2)s</span>
		  <span class="ampm">%(time2ap)s</span>
		</div>
	      </td>
	    </tr>
	    <tr>
	      <td class="td_holder">&nbsp;</td>
	    </tr>
	    <tr>
	      <td class="td_time" colspan="2">
		%(days)s
	      </td>
	    </tr>
	    <tr>
	      <td class="td_arrow" colspan="2">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)


# NO PARKING ANYTIME
def noParkingAnytime(d):
    return """
	  <table class="sign noParking" cellspacing="0">
	    <tr>
	      <td class="td_topLeft">NO</td>
	      <td class="td_header">PARKING</td>
	    </tr>
	    <tr>
	      <td class="td_anytime" colspan="2">
		ANYTIME
	      </td>
	    </tr>
	    <tr>
	      <td class="td_arrow" colspan="2">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)

##########
##
##  NO PARKING END
##
##########


##########
##
##  NO STANDING START
##
##########


# NO STANDING HOURS/DAYS
def noStanding(d):
    if d["days"] == 1:
        return noStandingAnytime(d)
    else:
        return """
	  <table class="sign noStanding" cellspacing="0">
	    <tr>
	      <td class="td_header">NO STANDING</td>
	    </tr>
	    <tr>
	      <td class="td_time">
		<div>
		  <span class="number">%(time1)s</span>
		  <span class="ampm">%(time1ap)s</span>
		  <span class="dash">-</span>
		  <span class="number">%(time2)s</span>
		  <span class="ampm">%(time2ap)s</span>
		</div>
	      </td>
	    </tr>
	    <tr>
	      <td class="td_time">
		%(days)s
	      </td>
	    </tr>
	    <tr>
	      <td class="td_arrow">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)



# NO STANDING ANYTIME
def noStandingAnytime(d):
    return """
	  <table class="sign noStanding" cellspacing="0">
	    <tr>
	      <td class="td_header">NO STANDING<br />ANYTIME</td>
	    </tr>
	    <tr>
	      <td class="td_arrow">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)


# NO STANDING ANYTIME TAXI STAND
def noStandingAnytimeTaxi(d):
    return """
	  <table class="sign noStanding" cellspacing="0">
	    <tr>
	      <td class="td_header">NO STANDING<br />ANYTIME<br />TAXI STAND</td>
	    </tr>
	    <tr>
	      <td class="td_arrow">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)


# NO STANDING EXCEPT TRUCKS - LOADING & UNLOADING
def noStandingExceptTrucks():
    return """
	  <table class="sign noStanding" cellspacing="0">
	    <tr>
	      <td class="td_header">NO STANDING</td>
	    </tr>
	    <tr>
	      <td class="td_headerSmall">EXCEPT TRUCKS<br />LOADING & UNLOADING</td>
	    </tr>
	    <tr>
	      <td class="td_time">
		<div>
		  <span class="number">%(time1)s</span>
		  <span class="ampm">%(time1ap)s</span>
		  <span class="dash">-</span>
		  <span class="number">%(time2)s</span>
		  <span class="ampm">%(time2ap)s</span>
		</div>
	      </td>
	    </tr>
	    <tr>
	      <td class="td_headerSmall">EXCEPT SUNDAY</td>
	    </tr>
	    <tr>
	      <td class="td_arrow">
		%(arrow)s
	      </td>
	    </tr>
	  </table>"""%(d)



##########
##
##  NO STANDING END
##
##########

##########
##
##  NO STOPPING START
##
##########

##########
##
##  NO STOPPING END
##
##########







def formatData(d):
    if d["days"] == 1:
        pass
    elif d["days"] == 2:       # EXCEPT SUNDAY
        d["days"] = """
		  <div class="exceptSunday">EXCEPT SUNDAY</div>"""
    elif d["days"][0] == 0:   # THRU
        d["days"] = """
		  <span class="day">%s</span>
		  <span class="thru">thru</span>
		  <span class="day">%s</span>"""%(d["days"][1],d["days"][2])
    elif d["days"][0] == 1: # AND 
        d["days"] = """
		  <span class="day">%s</span>
		  <span class="thru">&</span>
		  <span class="day">%s</span>"""%(d["days"][1],d["days"][2])
    else:                   # LIST DAYS
        temp = ""
        for x in range(1,len(d["days"])):
            temp += """
		  <span class="day">%s</span>"""%(d["days"][x])
            if x != len(d["days"])-1:
                temp += " &nbsp; "
        d["days"] = temp
        

    if d["arrow"] == 0:   # LEFT ARROW
        d["arrow"] = "&lt;---------"
    elif d["arrow"] == 1: # RIGHT ARROW
        d["arrow"] = "---------&gt;"
    else:                 # BOTH DIRECTIONS
        d["arrow"] = "&lt;--------&gt;"


    return d



if __name__ == "__main__":
    main()
