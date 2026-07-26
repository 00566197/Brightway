from app import app,db
from flask import render_template,redirect,url_for,flash,request,current_app,request,abort,jsonify
from app.models import *
from app.types import*
from app.forms import *
from flask_login import current_user,login_user,logout_user,login_required
from sqlalchemy import and_, func, select, or_
import os
import sqlalchemy as sa
from werkzeug.utils import secure_filename
import requests
from lxml import etree
from flask import Response
from r2_storage import upload_image


##feeding 
@app.route('/feed/autotrader.xml')
def autotrader_feed():
    cars = Car.query.all()
    
    root = etree.Element("vehicles")
    
    for car in cars:
        v = etree.SubElement(root, "vehicle")
        
        etree.SubElement(v, "id").text              = str(car.id)
        etree.SubElement(v, "make").text             = car.car_name or ''
        etree.SubElement(v, "model").text            = car.car_model or ''
        etree.SubElement(v, "year").text             = str(car.car_year or '')
        etree.SubElement(v, "price").text            = str(car.car_price or '')
        etree.SubElement(v, "colour").text           = car.car_color or ''
        etree.SubElement(v, "body_type").text        = car.car_type or ''
        etree.SubElement(v, "horse_power").text      = str(car.horse_power or '')
        etree.SubElement(v, "top_speed").text        = str(car.top_speed or '')
        etree.SubElement(v, "availability").text     = car.availability or ''
        etree.SubElement(v, "description").text      = car.information or ''
        
        # Images
        images_el = etree.SubElement(v, "images")
        for img in car.images:
            etree.SubElement(images_el, "image").text = (
                f"https://yoursite.com/static/uploads/{img.image_filename}"
            )
    
    xml_bytes = etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )
    return Response(xml_bytes, mimetype="application/xml")



### car infor autofill using reg number 
@app.route('/lookup-plate/<vrm>', methods=['GET'])
def lookup_plate(vrm):
    api_key = 'YOUR_DVLA_API_KEY'
    
    response = requests.post(
        'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles',
        headers={
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        },
        json={'registrationNumber': vrm.upper()}
    )
    
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            'success': True,
            'make': data.get('make', ''),
            'year': data.get('yearOfManufacture', ''),
            'colour': data.get('colour', ''),
            'fuel_type': data.get('fuelType', ''),
            'engine_size': data.get('engineCapacity', '')
        })
    else:
        return jsonify({'success': False, 'error': 'Plate not found'}), 404
@app.route('/',methods=['GET','POST'])
def index():
    form=MessageUs()
    cars=Car.query.all()
    if form.validate_on_submit():
            message=Message(
                form.f_name.data,
                form.l_name.data,
                form.email.data,
                form.phone_number.data,
                form.enquiry_type.data,
                form.message.data
            )
            db.session.add(message)
            db.session.commit()
            return jsonify({'success':True})
    
    
    return render_template(
        'base.html',
        cars=cars,
        form=form
    )

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    availability = request.args.get('availability', '').strip()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()
    car_type = request.args.get('car_type', '').strip()

    results = Car.query

    if query:
        search_term = f'%{query}%'
        results = results.filter(
            db.or_(
                Car.car_name.ilike(search_term),
                Car.car_model.ilike(search_term),
                Car.car_color.ilike(search_term),
                Car.car_type.ilike(search_term),
                Car.car_year.ilike(search_term)
            )
        )

    if availability:
        results = results.filter(Car.availability == availability)

    if min_price:
        results = results.filter(Car.car_price >= float(min_price))

    if max_price:
        results = results.filter(Car.car_price <= float(max_price))

    if car_type:
        results = results.filter(Car.car_type.ilike(f'%{car_type}%'))

    cars = results.all()

    return jsonify([{
        'id': car.id,
        'make': car.car_name,
        'model': car.car_model,
        'year': str(car.car_year) if car.car_year else '',
        'colour': car.car_color,
        'hp': car.horse_power,
        'top': car.top_speed,
        'price': '{:,.0f}'.format(car.car_price) if car.car_price else '0',
        'availability': car.availability,
        'description': car.information or '',
        'images': [
    img.image_filename
    for img in car.images
]
    } for car in cars])

@app.route('/add/car', methods=['POST','GET'])
@login_required
def add_car():
    form=CarUpload()
    if form.validate_on_submit():
        new_car = Car(
            car_name=form.car_name.data,
            car_model=form.car_model.data,
            car_year=form.car_year.data,
            horse_power=form.horse_power.data,
            top_speed=form.top_speed.data,
            rating=form.rating.data,
            car_color=form.car_color.data,
            availability=form.availability.data,
            car_price=form.car_price.data,
            car_type=form.car_type.data,
            information=form.information.data
        )
        db.session.add(new_car)
        db.session.commit()  

        uploaded_files = request.files.getlist('images')
            
        for file in uploaded_files[:30]:  # cap at 30
            if file and file.filename:
                image_url = upload_image(file)
            new_image = CarImages(image_filename=image_url, car_id=new_car.id)
            db.session.add(new_image)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template(
        'car_upload.html',
        form=form
    )

@app.route('/view/messages')
@login_required
def messages():
    all_messages = Message.query.order_by(Message.id.desc()).all()
    unread_count = Message.query.filter_by(is_read='unread').count()
    return render_template('view_messages.html', messages=all_messages, unread_count=unread_count)

@app.route('/mark-read/<int:id>', methods=['POST'])
@login_required
def mark_read(id):
    message = Message.query.get_or_404(id)
    message.is_read = 'read'
    db.session.commit()
    unread_count = Message.query.filter_by(is_read='unread').count()
    return jsonify({
        'success': True,
        'unread_count': unread_count
    })

@app.route('/edit/car/<int:id>',methods=['GET','POST'])
@login_required
def edit_car(id):
    car=Car.query.get_or_404(id)
    form=CarUpload()
    if form.validate_on_submit():
            car.car_name=form.car_name.data
            car.car_model=form.car_model.data
            car.car_year=form.car_year.data
            car.horse_power=form.horse_power.data
            car.top_speed=form.top_speed.data
            car.rating=form.rating.data
            car.car_color=form.car_color.data
            car.availability=form.availability.data
            car.car_price=form.car_price.data
            car.car_type=form.car_type.data
            car.information=form.information.data
            db.session.commit()
            flash('Car Innformation successfully edited','success')
            return redirect(url_for('car_info',id=car.id))
        
    form.car_name.data=car.car_name
    form.car_model.data=car.car_model
    form.car_year.data=car.car_year
    form.horse_power.data=car.horse_power
    form.top_speed.data=car.top_speed
    form.rating.data=car.rating
    form.car_color.data=car.car_color
    form.availability.data=car.availability
    form.car_price.data=car.car_price
    form.car_type.data=car.car_type
    form.information.data=car.information
    return render_template(
        'edit_car.html',
        form=form
    )

@app.route('/staff/home',methods=['GET','POST'])
@login_required
def staff_page():
    cars=Car.query.all()
    return render_template(
          'all_car.html',
          cars=cars
     )

@app.route('/car/information/<int:id>')

def car_info(id):

    car = Car.query.get_or_404(id)
    images = CarImages.query.filter_by(car_id=car.id).all()
    return render_template('view_info.html', car=car, images=images)



@app.route('/delete/<int:id>',methods=['GET','POST','DELETE'])
@login_required
def car_delete(id):
    car=Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    flash('Car information successfully deleted', 'success')
    return redirect(url_for('staff_page'))

@app.route('/privacy')
def privacy_policy():
    return render_template(
        'privacy_policy.html'
    )

@app.route('/tos')
def Tos():
    return render_template(
        'tos.html'
    )



import os

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != os.environ.get('STAFF_USERNAME'):
            return redirect(url_for('staff_login'))
        if form.password.data != os.environ.get('STAFF_PASSWORD'):
            return redirect(url_for('staff_login'))
        else:
            login_user(staff_user)
            return redirect(url_for('staff_page'))
    return render_template('login.html', form=form)

@app.route('/sitemap.xml')
def sitemap():
    pages = [{'loc': url_for('index', _external=True)}]

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = app.response_class(sitemap_xml, mimetype='application/xml')
    return response