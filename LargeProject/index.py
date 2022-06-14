import os
from flask_sqlalchemy import SQLAlchemy
from forms import AddForm, DelForm, EditForm
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import uuid
import operator

#print(basedir)
app = Flask(__name__)

app.config['SECRET_KEY'] = "!@#$%^&*"

#SQL DB
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

class Products(db.Model):
    productID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    shoetype = db.Column(db.Text)
    condition = db.Column(db.Text)
    description = db.Column(db.Text)
    gender = db.Column(db.Text)
    size = db.Column(db.Integer)
    filename = db.Column(db.Text)
    price = db.Column(db.Text)
    contact = db.Column(db.Text)
    accesscode = db.Column(db.Text)
    quantity = db.Column(db.Integer)

    def __init__(self, name, shoetype, condition, description, size, gender, price, filename, contact, accesscode, quantity):
        self.name = name
        self.shoetype = shoetype
        self.condition = condition
        self.description = description
        self.size = size
        self.gender = gender
        self.price = price
        self.filename = filename
        self.contact = contact
        self.accesscode = accesscode
        self.quantity = quantity


    def __repr__(self):
        return "Shoe name is {} size{} {}".format(self.name, self.size, self.gender)

#View functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/postproduct', methods = ['GET', 'POST'])
def postproduct():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        shoetype = form.shoetype.data
        condition = form.condition.data
        description = form.description.data
        quantity = form.quantity.data
        size = form.size.data
        gender = form.gender.data
        price = form.price.data
        contact = form.contact.data
        accesscode = form.accesscode.data
        #filename = secure_filename(form.file.data.filename)
        filename = secure_filename(str(uuid.uuid1())+".jpg")
        form.file.data.save('your_folder_path/LargeProject/static/' + filename)
        new_product = Products(name, shoetype, condition, description, size, gender, price, filename, contact, accesscode, quantity)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('shopall'))
    else:
        print("Not valid")
    return render_template('postproduct.html', form = form)

@app.route('/postproduct/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/thankyou')
def thankyou():
    first = request.args.get('firstname')
    return render_template('thankyou.html', first = first)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/shop/lifestyle')
def lifestyle():
    return render_template('lifestyle.html')

@app.route('/shop/sports')
def sports():
    return render_template('sports.html')
@app.route('/loggedin')
def loggedinhome():
    email = request.args.get('logemail')
    email = email[:email.index('@')]
    return render_template('loggedinhome.html', email = email)
@app.route('/shop/dress')
def dress():
    return render_template('dress.html')

@app.route('/shop/shopall')
def shopall():
    allshoes = Products.query.all()
    allshoes = sorted(allshoes, key=operator.attrgetter("productID"), reverse=True)
    return render_template('shopall.html', allshoes= allshoes)

@app.route('/shop/shopall/<productID>')
def productpage(productID):
    product = Products.query.get(productID)
    return render_template('productpage.html', product = product)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/query')
def query():
    word = request.args.get('searchbar')
    print("Word = ", word)
    shoetypeprod = Products.query.filter(Products.shoetype.like(word + "%")).all()
    nameprod = Products.query.filter(Products.name.like(word + "%")).all()
    selprod = list()
    selprod.extend(shoetypeprod)
    selprod.extend(nameprod)
    selprod = sorted(selprod, key=operator.attrgetter("productID"), reverse=True)

    return render_template('query.html', word = word, selprod = selprod)

@app.route('/deleteproduct',methods=['GET', 'POST'])
def deleteproduct():
    form = DelForm()

    if form.validate_on_submit():
        prodaccesscode = form.accesscode.data
        product = Products.query.filter_by(accesscode = prodaccesscode).first()
        if product is not None:
            db.session.delete(product)
            db.session.commit()
            redirect(url_for('shopall'))
    else:
        print('No')
    return render_template('deleteproduct.html', form = form)

@app.route('/editproduct',methods=['GET', 'POST'])
def editproduct():
    form = EditForm()

    if form.validate_on_submit():
        name = form.name.data
        shoetype = form.shoetype.data
        condition = form.condition.data
        description = form.description.data
        quantity = form.quantity.data
        size = form.size.data
        gender = form.gender.data
        price = form.price.data
        contact = form.contact.data
        prodaccesscode = form.accesscode.data
        filename = secure_filename(str(uuid.uuid1())+".jpg")
        form.file.data.save('your_folder_path/LargeProject/static/' + filename)
        product = Products.query.filter_by(accesscode = prodaccesscode).first()
        if product is not None:
            product.name = name
            product.shoetype = shoetype
            product.condition = condition
            product.description = description
            product.quantity = quantity
            product.size = size
            product.gender = gender
            product.price = price
            product.contact = contact
            product.filename = filename
            db.session.commit()
            redirect(url_for('shopall'))
    else:
        print('No')
    return render_template('editproduct.html', form = form)


@app.route('/shop/shopall/thanksforshopping/<productID>', methods = ['GET', 'POST'])
def thanksforshopping(productID):
    product = Products.query.get(productID)
    product.quantity-=1
    db.session.commit()
    return render_template('thanksforshopping.html', product = product)


if __name__ == '__main__':
    app.run(debug = True)
