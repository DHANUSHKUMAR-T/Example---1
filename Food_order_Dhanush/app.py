# flask_app.py
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

menu_items = {
    'western_food': {
        'Burger': {'price': 50, 'image': 'burger.jpg', 'description': 'Delicious beef burger'},
        'Pizza': {'price': 80, 'image': 'pizza.jpg', 'description': 'Cheesy pepperoni pizza'},
        'Pasta': {'price': 70, 'image': 'Pasta.jpg', 'description': 'Creamy alfredo pasta'},
        'Steak': {'price': 50, 'image': 'steak.jpg', 'description': 'Juicy grilled steak'},
        'Hot Dog': {'price': 50, 'image': 'hotdog.jpg', 'description': 'Classic hot dog'},
        'Fish & Chips': {'price': 90, 'image': 'fishchips.jpg', 'description': 'Crispy fish and chips'},
        'Ice Cream': {'price': 40, 'image': 'icecream.jpg', 'description': 'Vanilla ice cream'},
        'Salad': {'price': 60, 'image': 'salad.jpg', 'description': 'Fresh garden salad'},
        'Sandwich': {'price': 50, 'image': 'sandwich.jpg', 'description': 'Ham and cheese sandwich'},
        'Fries': {'price': 30, 'image': 'fries.jpg', 'description': 'Crispy french fries'},
        'BBQ Ribs': {'price': 120, 'image': 'bbqribs.jpg', 'description': 'Smoky BBQ ribs'},
        'Soup': {'price': 40, 'image': 'soup.jpg', 'description': 'Tomato soup'},
        'Pancakes': {'price': 50, 'image': 'pancakes.jpg', 'description': 'Fluffy pancakes'},
        'Tacos': {'price': 70, 'image': 'Tacos.jpg', 'description': 'Beef tacos'},
        'Milkshake': {'price': 40, 'image': 'milkshake.jpg', 'description': 'Chocolate milkshake'}
    },
    'indian_food': {
        'Butter Chicken': {'price': 100, 'image': 'butter_chicken.jpg', 'description': 'Creamy butter chicken'},
        'Naan': {'price': 20, 'image': 'naan.jpg', 'description': 'Soft and fluffy naan'},
        'Biryani': {'price': 120, 'image': 'biryani.jpg', 'description': 'Spicy chicken biryani'},
        'Paneer Tikka': {'price': 80, 'image': 'paneer_tikka.jpg', 'description': 'Grilled paneer tikka'},
        'Samosa': {'price': 30, 'image': 'samosa.jpg', 'description': 'Crispy samosa'},
        'Chole Bhature': {'price': 60, 'image': 'chole_bhature.jpg', 'description': 'Chickpeas with fried bread'},
        'Dosa': {'price': 50, 'image': 'dosa.jpg', 'description': 'Crispy dosa'},
        'Idli': {'price': 40, 'image': 'idli.jpg', 'description': 'Steamed idli'},
        'Vada': {'price': 30, 'image': 'vada.jpg', 'description': 'Fried vada'},
        'Gulab Jamun': {'price': 40, 'image': 'gulab_jamun.jpg', 'description': 'Sweet gulab jamun'},
        'Pani Puri': {'price': 40, 'image': 'pani_puri.jpg', 'description': 'Spicy pani puri'},
        'Rajma': {'price': 60, 'image': 'rajma.jpg', 'description': 'Kidney bean curry'},
        'Palak Paneer': {'price': 90, 'image': 'palak_paneer.jpg', 'description': 'Spinach paneer'},
        'Roti': {'price': 100, 'image': 'roti.jpg', 'description': 'Whole wheat roti'},
        'Lassi': {'price': 30, 'image': 'lassi.jpg', 'description': 'Sweet lassi'}
    }
}

home_images = ['home1.jpg', 'home2.jpg', 'home3.jpg']

@app.route('/')
def home():
    random_image = random.choice(home_images)
    return render_template('home.html', random_image=random_image)

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/menu/western')
def western_food():
    return render_template('western_food.html', menu=menu_items['western_food'])

@app.route('/menu/indian')
def indian_food():
    return render_template('indian_food.html', menu=menu_items['indian_food'])

@app.route('/order', methods=['POST'])
def order():
    ordered_items = []
    grand_total = 0
    for item_name, item_details in {**menu_items['western_food'], **menu_items['indian_food']}.items():
        quantity = int(request.form.get(item_name, 0))
        if quantity > 0:
            total = quantity * item_details['price']
            ordered_items.append({'name': item_name, 'quantity': quantity, 'price': item_details['price'], 'total': total})
            grand_total += total
    
    return render_template('order.html', ordered_items=ordered_items, grand_total=grand_total)

@app.route('/order/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        payment_type = request.form['payment_type']
        if payment_type == 'online':
            return redirect(url_for('online_payment'))
        elif payment_type == 'offline':
            return redirect(url_for('offline_payment'))
    return render_template('payment.html')

@app.route('/payment/online', methods=['GET', 'POST'])
def online_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        password = request.form['password']
        if password == 'A1B2C3':
            return render_template('payment_success.html', message='Payment Successful')
        else:
            return render_template('oonline_payment.html', error='Incorrect password. Please try again. The password is [A1B2C3]')
    return render_template('online_payment.html')

@app.route('/payment/offline', methods=['GET', 'POST'])
def offline_payment():
    if request.method == 'POST':
        return render_template('payment_success.html', message='Offline Payment Successful')
    return render_template('offline_payment.html')

@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7860)