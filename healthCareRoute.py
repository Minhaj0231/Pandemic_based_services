from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from healthCareSpecialistDB import HealthCareSpecialistDb
from middleware import is_loggedIn, has_permission 
from datetime import datetime
from uploadUtils import photos

healthCare = Blueprint("healthCare",__name__, static_folder="static", template_folder="templates")

# nurseDb = HomeNursingDb()

healthCareDb = HealthCareSpecialistDb()


@healthCare.route("/getAddHealthCareinfo", methods =["GET"])
def getAddHealthCareinfo():
    return render_template("healthCare_signup.html")


@healthCare.route("/postAddHealthCareInfo", methods =["POST"])
def postAddHealthCareInfo():
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    name = name+ "."

    if 'UserImage' in request.files:
        filename = photos.save(request.files['UserImage'],name=name)

    try:

        
        result = healthCareDb.add_health_care_specialist(image=filename,
        name =session['UserName'] , 
        specialized = request.form.get('specialized'), 
        phone = str(session['UserPhone']), 
        area = request.form.get('Area'), 
        certification_experience = request.form.get('Certification'),
        charge =int(request.form.get('PerUnitCharge')))

    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    
    session.clear()
    
    return redirect(url_for('auth.getLogin'))
    

@healthCare.route("/getAllHealthCareinfo", methods =["GET"])
def getAllHealthCareinfo():

    result = None
    try:

        result = healthCareDb.get_all_hc_specialist()
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    print(result)


    return render_template("healthCare_all.html", result = result)            


#### done till now

@healthCare.route("/getSingelHealthCareinfo/<healthCare_phone>", methods =["GET"])
def getSingelHealthCareinfo(healthCare_phone):

    result = None
    try:

        result = healthCareDb.get_single_hc_specialist(healthCare_phone)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    try:

        comment = healthCareDb.get_all_hc_specialist_comments(healthCare_phone)
    except Exception as e:
        flash(" Error try again")
        print( "exception: " + str(e))
        

    print(comment)

    return render_template("healthCare_Details.html", result = result[0], comment = comment)      


@healthCare.route("/postADDHealthCareComment/", methods =["POST"])
@is_loggedIn 
def postADDHealthCareComment():


    hc_specialist_phone = request.form.get('Pphone')
    comment = request.form.get('Ucommnet')

    if( str(hc_specialist_phone) ==str(session['UserPhone'])):
        flash("You cannot  comment in your profile")
        
        # need to redirect to comment page

    result = None
    try:

        result = healthCareDb.add_comment(hc_specialist_phone=hc_specialist_phone, user_phone= str(session['UserPhone']), user_name=session['UserName'], comment=comment)
        
    except Exception as e:
        flash( "Error try again ")
        print( " exception: " + str(e))


    return redirect(url_for('healthCare.getSingelHealthCareinfo', healthCare_phone =str(hc_specialist_phone) ))      





