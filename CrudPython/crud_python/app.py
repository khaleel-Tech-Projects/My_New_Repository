from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)  # Set the session lifetime

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # Create users table with role
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form.get('role', 'user')  # Optional: admin or user

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
            return redirect('/signup')
        finally:
            conn.close()

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()

        if row and check_password_hash(row[2], password):
            session['user'] = {
                'id': row[0],
                'username': row[1],
                'role': row[3]
            }
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid credentials', 'danger')
            return redirect('/login')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    user = session['user']

    if user['role'] == 'admin':
        products = get_all_products()
        return render_template('admin_dashboard.html',
                               user=user,
                               products=products,
                               total_products=len(products),
                               total_in_stock=sum(1 for p in products if p['quantity'] > 0),
                               total_out_of_stock=sum(1 for p in products if p['quantity'] == 0))
    else:
        user_products = get_user_products(user['id'])  # Currently returns all products
        return render_template('user_dashboard.html', user=user, products=user_products)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect('/')

# Show all products
@app.route('/products')
def show_products():
    if 'user' not in session:
        return redirect('/login')

    products = get_all_products()
    return render_template('product_list.html', products=products)

# Add product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('show_products'))

    return render_template('add_product.html')

# Edit product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        c.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?", (name, price, quantity, id))
        conn.commit()
        conn.close()
        return redirect(url_for('show_products'))

    c.execute("SELECT * FROM products WHERE id=?", (id,))
    product = c.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

# Delete product
@app.route('/delete/<int:id>')
def delete_product(id):
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_products'))

# View product
@app.route('/view/<int:id>')
def view_product(id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (id,))
    product = c.fetchone()
    conn.close()
    return render_template('view_product.html', product=product)

# About and Contact
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Helper Functions
def get_all_products():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_user_products(user_id):
    # Placeholder: all users see all products for now
    return get_all_products()


@app.route('/view_product_details/<int:product_id>')
def view_product_details(product_id):
    # Your logic to fetch and display the product details
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    
    if product:
        return render_template('product_view.html', product=product)
    else:
        return redirect('/products')


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect('/login')  # Redirect if user is not logged in

    user_id = session['user_id']
    quantity = request.form.get('quantity', 1, type=int)  # Get quantity, default is 1

    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if product already exists in the user's cart
    c.execute("SELECT * FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    cart_item = c.fetchone()

    if cart_item:
        # If product is already in the cart, update the quantity
        c.execute("UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?",
                  (quantity, user_id, product_id))
    else:
        # Otherwise, add a new product to the cart
        c.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                  (user_id, product_id, quantity))

    conn.commit()
    conn.close()

    return redirect('/cart')  # Redirect to the cart page

@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect if user is not logged in

    user_id = session['user_id']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Fetch all items in the user's cart
    c.execute("""
        SELECT p.id, p.name, p.category, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,))
    cart_items = c.fetchall()

    conn.close()

    return render_template('cart.html', cart_items=cart_items)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Implement reset logic (e.g., email a link or token)
        flash('Reset instructions sent to your email.', 'success')
        return redirect(url_for('login'))
    return render_template('forgot-password.html')

# Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
