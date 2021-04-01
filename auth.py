from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from userDB import UserGeneralDb
auth = Blueprint("auth",__name__, static_folder="static", template_folder="templates")

authDb = UserGeneralDb()

# shows  signup page
@auth.route("/getSignup", methods =["GET"])
def getSignup():
    return render_template("signup.html")


#   add a new user to database . if error  redirects to getsignup view
@auth.route("/postSignup", methods =["POST"])
def postSignup():
    
    # print(request.form.get('UserName'))

    # user Roles  Which can be accepted . 
    valid_User_Roles = set(['user',  'admin' ,'nurse', 'ambulance', 'funeralVolunteer', 'healthCare'])
    # checking if UserRole is valid from form submisson 
    if request.form.get('UserRole') not in  valid_User_Roles:
        flash("This Role is not accepted. Only 'user','ambulance', 'funeralVolunteer', 'healthCare' and 'nurse' roles are  valid ")
        return redirect(url_for('auth.getSignup'))

    if not request.form.get('UserPhone').isnumeric() :
        flash("Enter a valid phone Number")
        return redirect(url_for('auth.getSignup'))

    if  len(request.form.get('UserPhone')) != 11:
        flash("Enter a valid phone Number")
        return redirect(url_for('auth.getSignup'))

    try:
        
        success =  authDb.signup(user_name=request.form.get('UserName'),user_phone=request.form.get('UserPhone'), user_password=request.form.get('UserPassword'), user_role=request.form.get('UserRole'))
        if success["success"]:
            flash("You have successfully signed up ")
        else:
            flash("Error during SignUp Try again. Use new phone nubmer.")
            return redirect(url_for('auth.getSignup'))

    except Exception as e:
        print( "exception: " + str(e))

    session['UserPhone'] = request.form.get('UserPhone')
    session['UserName'] = request.form.get('UserName')
    session['UserRole'] = request.form.get('UserRole')

    if success["success"] and request.form.get('UserRole') == 'nurse':
        return redirect(url_for('homeNurse.getAddNurseinfo'))
    
    if success["success"] and request.form.get('UserRole') == 'ambulance':
        return redirect(url_for('ambulance.getAddAmbulanceinfo'))

    if success["success"] and request.form.get('UserRole') == 'funeralVolunteer':
        return redirect(url_for('fuService.getAddFUinfo'))

    if success["success"] and request.form.get('UserRole') == 'healthCare':
        return redirect(url_for('healthCare.getAddHealthCareinfo'))
   


    session.clear()

    return redirect(url_for('auth.getLogin'))

    

# shows  login page
@auth.route("/getLogin", methods =["GET"])
def getLogin():
    return render_template("login.html")


# login a new user  if error redirects to getLog in view
@auth.route("/postLogin", methods =["POST"])
def postLogin():
    print(request.form.get('UserPassword'))

    try:
        LoggedInUser = authDb.login(user_phone=request.form.get('UserPhone'), user_password=request.form.get('UserPassword'))
        print(LoggedInUser['success'] )
        if LoggedInUser['success']:
            print("usermatched")
            session['UserPhone'] = LoggedInUser['userPhone']
            session['UserName'] = LoggedInUser['userName']
            session['UserRole'] = LoggedInUser['userRole']

            print(session['UserPhone'])
            
            if session['UserRole'] == "nurse" :
               return redirect(url_for('homeNurse.getSingelNurseinfo', nurse_phone =str(session['UserPhone']) ))

            if session['UserRole'] == "ambulance" :
               return redirect(url_for('ambulance.getSingelAmbulanceinfo', ambulance_phone =str(session['UserPhone']) ))

            if session['UserRole'] == "funeralVolunteer" :
               return redirect(url_for('fuService.getSingelFUinfo', FU_phone =str(session['UserPhone']) ))

            if session['UserRole'] == "'healthCare'" :
               return redirect(url_for('healthCare.getSingelHealthCareinfo', healthCare_phone =str(session['UserPhone']) ))

           


            return redirect(url_for('index'))
        else:
            flash("Error during log in .Try again ")
    except Exception as e:
        print(str(e))
        pass
    
     
    
    
    return redirect(url_for('auth.getLogin'))



# clears all session . then  redircts to getLogin view    
@auth.route("/getLogout", methods =["GET"])
def getLogout():
    session.clear()
    
    return redirect(url_for('auth.getLogin'))