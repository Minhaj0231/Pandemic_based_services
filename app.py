from flask import Flask, render_template, request, redirect, Blueprint
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from uploadUtils import photos
from flask_uploads import  configure_uploads

from productDB import Product, ProductDb
from homeNursingDB import *
import datetime
import time
from auth import auth
from test import test
from admin import admin
from shop import shop
from homeNursingRoute import homeNurse
from TestSample import testSample
from funeralService import fuService
from ambulanceRoute import ambulance
from healthCareRoute import healthCare

app = Flask(__name__)
app.secret_key = "abc"  

   # import this  before uploading files from any other py files 

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app,photos)


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(shop, url_prefix="/shop")
app.register_blueprint(homeNurse, url_prefix="/homeNurse")
app.register_blueprint(testSample, url_prefix="/testSample")
app.register_blueprint(fuService, url_prefix="/fuService")
app.register_blueprint(ambulance, url_prefix="/ambulance")
app.register_blueprint(healthCare, url_prefix="/healthCare")



connect(db='cse499', host='localhost', port=27017)

productDb = ProductDb()
nurseDb =  HomeNursingDb()


@app.route('/')
def index():
	return render_template("home.html")


@app.route('/addProduct_test')
def addProduct():
	return productDb.add_product(product_name="hand gloves", available_unit = 25, per_unit_charge = 15.00, product_image = "jkjjdf.jpeg", product_description = "This is hand gloves")

 
@app.route('/increaseProduct_test')
def increaseProduct():
	return productDb.increase_product("5f2e893cb21bfbc8153df3c8", 2009)   


@app.route('/getAllProducts_test')
def getAllProducts():
	productsList = productDb.get_all_products()
	return render_template('show_products.html', products = productsList)


@app.route('/addUserOrder_test')
def addUserOrder():
	return productDb.add_user_order(user_email="irfannisho8571@gmail.com", product_Id="5f2e893cb21bfbc8153df3c8", product_amount = 2, product_name = "hand gloves", total_price=50, date=datetime.datetime.utcnow)


@app.route('/getAllUserOrders_test')
def getAllUserOrders():
	ordersList = productDb.get_all_user_orders(user_email="irfannisho8571@gmail.com")
	return render_template('show_user_order.html', orders = ordersList)


@app.route('/addUserCart_test')
def addUserCart():
	return productDb.add_to_cart(user_email="irfannisho8571@gmail.com", product_Id="5f2e893cb21bfbc8153df3c8", product_name="hand_gloves",product_amount=10, total_price=500.00)	

@app.route('/removeFromCart_test')
def removeFromCart():
	return productDb.remove_from_cart(user_email="irfannisho8571@gmail.com", product_Id="5f2e893cb21bfbc8153df3c8")

@app.route('/getUserCart_test')
def getUserCart():
	user_cart =  productDb.get_user_cart(user_email="irfannisho8571@gmail.com")
	return render_template('cartDetails.html', carts=user_cart)

@app.route('/addNurse_test')
def addNurse():
	return nurseDb.add_nurses(city="Rangpur", num=200)

@app.route('/nursesNumberInCity_test')
def nursesNumberInCity():
	nurse_cnt = nurseDb.nursesNumberInCity(city="Rangpur", date=datetime.datetime(2020, 7, 7))
	return render_template('nurseDetails.html', cnt=nurse_cnt, func="show_nurse_cnt")

@app.route('/bookNurse_test')
def bookNurse():
	return nurseDb.bookNurse(city="Dhaka", user_email="laylaa@gmail.com", address="mirpur-12",  date=datetime.datetime(2020, 7, 7), done=False)

@app.route('/get_number_bookedNurse_test')
def get_number_bookedNurse():
	nurse_cnt = nurseDb.get_number_bookedNurses(city="Dhaka")
	return render_template('nurseDetails.html', cnt=nurse_cnt, func="show_booked_nurse_cnt")

@app.route('/remove_bookedNurse_test')
def remove_bookedNurse():
	return nurseDb.remove_bookedNUrse(bookedNurse_id="5f561c2656bd5bfa2e5cb930")	

@app.route('/get_users_booked_nurses_test')
def get_users_booked_nurses():
	nurses = nurseDb.get_users_booked_nurses(user_email="laylaa@gmail.com")
	return render_template('nurseDetails.html', nurses=nurses, func="show_users_booked_nurse")	

@app.route('/change_pending_bookedNurse_test')
def change_pending_bookedNurse():
	return nurseDb.change_pending_bookedNurses(bookedNurse_id="5f562e4c557f5b64828a00e0", done=True)	

@app.route('/get_all_bookedNurse_test')
def get_all_bookedNurse():
	nurses = nurseDb.get_all_bookedNurses()
	return render_template('nurseDetails.html', nurses=nurses, func="show_all_booked_nurse")

@app.route('/get_pending_bookedNurse_test')
def get_pending_bookedNurse():
	nurses = nurseDb.get_pending_bookedNurses(bookedNurse_id="5f562e4c557f5b64828a00e0", done=True)
	return render_template('nurseDetails.html', nurses=nurses, func="show_pending_booked_nurse")	



if __name__ == "__main__":
	app.run(debug=True)    