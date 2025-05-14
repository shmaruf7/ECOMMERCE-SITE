from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secret'

# Categories with online image URLs
categories = [
    {"id": 1, "name": "Men", "image": "https://via.placeholder.com/200x150?text=Men"},
    {"id": 2, "name": "Women", "image": "https://via.placeholder.com/200x150?text=Women"},
    {"id": 3, "name": "Kids", "image": "https://via.placeholder.com/200x150?text=Kids"},
    {"id": 4, "name": "Accessories", "image": "https://via.placeholder.com/200x150?text=Accessories"}
]

# Products with online images
products = [
    {
        "id": i,
        "name": f"Item {i}",
        "price": 100 + i * 5,
        "category_id": (i % 4) + 1,
        "image": f"https://via.placeholder.com/200x200?text=Item+{i}",
        "description": f"Description for Item {i}"
    }
    for i in range(1, 81)
]

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/category/<int:cat_id>')
def category(cat_id):
    filtered = [p for p in products if p['category_id'] == cat_id]
    cat = next((c for c in categories if c['id'] == cat_id), {})
    return render_template('category.html', category=cat, products=filtered)

@app.route('/product/<int:prod_id>')
def product(prod_id):
    prod = next((p for p in products if p['id'] == prod_id), {})
    return render_template('product.html', product=prod)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    prod_id = int(request.form['product_id'])
    cart = session.get('cart', {})
    cart[str(prod_id)] = cart.get(str(prod_id), 0) + 1
    session['cart'] = cart
    return redirect('/cart')
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    return redirect('/cart')


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        prod = next((p for p in products if p['id'] == int(pid)), None)
        if prod:
            total += prod['price'] * qty
            items.append({"product": prod, "qty": qty})
    return render_template('cart.html', items=items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for pid in list(cart.keys()):
        qty = int(request.form.get(f'qty_{pid}', 1))
        if qty > 0:
            cart[pid] = qty
        else:
            del cart[pid]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    phone = request.form['phone']
    address = request.form['address']
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        prod = next((p for p in products if p['id'] == int(pid)), None)
        if prod:
            total += prod['price'] * qty
            items.append({"product": prod, "qty": qty})
    delivery = 120
    grand_total = total + delivery
    session['cart'] = {}  # Clear cart after confirming order
    return render_template('confirm.html', items=items, total=total, delivery=delivery, grand_total=grand_total, phone=phone, address=address)

if __name__ == '__main__':
    app.run(debug=True)
