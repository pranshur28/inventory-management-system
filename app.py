from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Add context processor for current date
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Add template filter for calculating total inventory value
@app.template_filter('total_inventory_value')
def total_inventory_value(products):
    return sum(product.price * product.quantity for product in products)

# Define models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.name}', '{self.quantity}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'in' or 'out'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(200))
    product = db.relationship('Product', backref='transactions')

    def __repr__(self):
        return f"Transaction('{self.product.name}', '{self.transaction_type}', '{self.quantity}')"

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categories')
def categories():
    all_categories = Category.query.all()
    return render_template('categories.html', categories=all_categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        # Check if category already exists
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash('Category already exists!', 'danger')
            return redirect(url_for('add_category'))
        
        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html')

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('edit_category.html', category=category)

@app.route('/categories/delete/<int:id>')
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if category has products
    if category.products:
        flash('Cannot delete category with associated products!', 'danger')
        return redirect(url_for('categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories'))

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        
        new_product = Product(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            category_id=category_id
        )
        
        db.session.add(new_product)
        db.session.commit()  # Commit to get the product ID
        
        # Add transaction record for initial stock
        if quantity > 0:
            new_transaction = Transaction(
                product_id=new_product.id,
                quantity=quantity,
                transaction_type='in',
                notes='Initial stock'
            )
            db.session.add(new_transaction)
            db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        old_quantity = product.quantity
        new_quantity = int(request.form['quantity'])
        
        product.name = request.form['name']
        product.description = request.form['description']
        product.quantity = new_quantity
        product.price = float(request.form['price'])
        product.category_id = int(request.form['category_id'])
        
        # Add transaction record if quantity changed
        if new_quantity != old_quantity:
            quantity_diff = new_quantity - old_quantity
            transaction_type = 'in' if quantity_diff > 0 else 'out'
            
            new_transaction = Transaction(
                product_id=product.id,
                quantity=abs(quantity_diff),
                transaction_type=transaction_type,
                notes='Manual adjustment'
            )
            db.session.add(new_transaction)
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    categories = Category.query.all()
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # Delete associated transactions
    Transaction.query.filter_by(product_id=id).delete()
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

@app.route('/transactions')
def transactions():
    all_transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('transactions.html', transactions=all_transactions)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        transaction_type = request.form['transaction_type']
        notes = request.form['notes']
        
        product = Product.query.get_or_404(product_id)
        
        # Update product quantity
        if transaction_type == 'in':
            product.quantity += quantity
        else:  # 'out'
            if product.quantity < quantity:
                flash('Not enough stock available!', 'danger')
                products = Product.query.all()
                return render_template('add_transaction.html', products=products)
            product.quantity -= quantity
        
        new_transaction = Transaction(
            product_id=product_id,
            quantity=quantity,
            transaction_type=transaction_type,
            notes=notes
        )
        
        db.session.add(new_transaction)
        db.session.commit()
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))
    
    products = Product.query.all()
    return render_template('add_transaction.html', products=products)

@app.route('/dashboard')
def dashboard():
    # Get low stock products (less than 5 items)
    low_stock = Product.query.filter(Product.quantity < 5).all()
    
    # Get recent transactions
    recent_transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(5).all()
    
    # Get total inventory value
    total_value = sum(product.price * product.quantity for product in Product.query.all())
    
    # Get total number of products and categories
    product_count = Product.query.count()
    category_count = Category.query.count()
    
    return render_template(
        'dashboard.html',
        low_stock=low_stock,
        recent_transactions=recent_transactions,
        total_value=total_value,
        product_count=product_count,
        category_count=category_count
    )

if __name__ == '__main__':
    app.run(debug=True)
