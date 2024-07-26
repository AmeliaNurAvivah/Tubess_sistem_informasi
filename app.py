from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Menu, Order, Cart


app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

cart = Cart()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', menus=Menu.query.all())

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = Menu.query.get(item_id)
    if item:
        cart.add_item(item)
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart.get_items())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        customer_address = request.form['customer_address']

        items = ", ".join([item.name for item in cart.get_items()])
        new_order = Order(items, customer_name, customer_phone, customer_address)
        db.session.add(new_order)
        db.session.commit()
        cart.clear()
        return redirect(url_for('order_status', order_id=new_order.id))
    return render_template('checkout.html')

@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('status.html', order=order)

@app.route('/status', methods=['GET', 'POST'])
def status():
    order = None
    not_found = False
    if request.method == 'GET':
        order_id = request.args.get('order_id')
        if order_id:
            order = Order.get_order_by_id(order_id)
            if not order:
                not_found = True
    return render_template('status.html', order=order)


@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Simple authentication for demonstration purposes
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin_menu', methods=['GET', 'POST'])
def admin_menu():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])
        new_item = Menu(name=name, price=price)
        db.session.add(new_item)
        db.session.commit()
    return render_template('admin_menu.html', menus=Menu.query.all())

@app.route('/admin/delete_menu/<int:item_id>', methods=['POST'])
def delete_menu(item_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    item = Menu.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('admin_menu'))

@app.route('/admin_orders')
def admin_orders():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin_sales_report')
def admin_sales_report():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    orders = Order.query.all()
    return render_template('admin_sales_report.html', orders=orders)

@app.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    order = Order.query.get_or_404(order_id)
    if order:
        order.status = request.form['status']
        db.session.commit()
    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    app.run(debug=True)
