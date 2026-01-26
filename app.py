from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Job Cards Storage
DATA_FILE = "jobs_data.json"

def load_jobs():
    """Load jobs from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return [
        {"job_id": "JC1234", "status": "Open",   "remarks": "Initial review", "assigned_to": "Alice"},
        {"job_id": "JC5678", "status": "Closed", "remarks": "Completed",      "assigned_to": "Bob"},
    ]

def save_jobs(jobs):
    """Save jobs to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

jobs = load_jobs()

# Orders Storage
ORDERS_FILE = "orders_data.json"
CART_FILE = "cart_data.json"

def load_orders():
    """Load orders from JSON file"""
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_orders(orders):
    """Save orders to JSON file"""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def load_cart():
    """Load shopping cart from JSON file"""
    if os.path.exists(CART_FILE):
        with open(CART_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_cart(cart):
    """Save shopping cart to JSON file"""
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=2)

# Rewards Storage
REWARDS_FILE = "rewards_data.json"

def load_rewards():
    """
    Stored format (list of dicts):
    [
      {"customer_id": "S1234567A", "name": "Alice Tan", "purchases": 2, "redeemed": 0}
    ]
    """
    if os.path.exists(REWARDS_FILE):
        with open(REWARDS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_rewards(customers):
    with open(REWARDS_FILE, "w") as f:
        json.dump(customers, f, indent=2)

def compute_reward_balance(customer):
    """
    1 discount per 3 purchases.
    balance = floor(purchases/3) - redeemed
    """
    earned = customer.get("purchases", 0) // 3
    redeemed = customer.get("redeemed", 0)
    return max(0, earned - redeemed)

# Catalog Storage
CATALOG_FILE = "catalog_data.json"

def load_catalog():
    """Load catalog items from JSON file"""
    if os.path.exists(CATALOG_FILE):
        with open(CATALOG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_catalog(catalog):
    """Save catalog items to JSON file"""
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def home():
    global jobs
    jobs = load_jobs()

    search_query = request.args.get("search", "").strip().lower()

    if request.method == "POST":
        job_id = request.form.get("job_id", "").strip()
        status = request.form.get("status", "").strip()
        remarks = request.form.get("remarks", "").strip()
        assigned_to = request.form.get("assigned_to", "").strip()

        if job_id and status:
            # Prevent duplicate Job ID
            if any(j.get("job_id") == job_id for j in jobs):
                return redirect(url_for("home")) 
            jobs.append({
                "job_id": job_id,
                "status": status,
                "remarks": remarks,
                "assigned_to": assigned_to,
            })
            save_jobs(jobs)

        return redirect(url_for("home"))

    filtered_jobs = jobs
    if search_query:
        filtered_jobs = [
            job for job in jobs
            if search_query in job.get("job_id", "").lower()
            or search_query in job.get("status", "").lower()
            or search_query in job.get("remarks", "").lower()
            or search_query in job.get("assigned_to", "").lower()
        ]

    return render_template("index.html", jobs=filtered_jobs, search_query=search_query)

@app.route("/update/<job_id>", methods=["GET", "POST"])
def update(job_id):
    global jobs
    jobs = load_jobs()

    job = next((j for j in jobs if j["job_id"] == job_id), None)
    if not job:
        return redirect(url_for("home"))

    if request.method == "POST":
        job["status"] = request.form.get("status", "").strip()
        job["remarks"] = request.form.get("remarks", "").strip()
        job["assigned_to"] = request.form.get("assigned_to", "").strip()
        save_jobs(jobs)
        return redirect(url_for("home"))

    return render_template("update.html", job=job)

@app.route("/delete/<job_id>", methods=["POST"])
def delete(job_id):
    global jobs
    jobs = load_jobs()
    jobs = [j for j in jobs if j["job_id"] != job_id]
    save_jobs(jobs)
    return redirect(url_for("home"))

@app.route("/rewards", methods=["GET", "POST"])
def rewards():
    customers = load_rewards()
    search_query = request.args.get("search", "").strip().lower()

    if request.method == "POST":
        action = request.form.get("action", "").strip()

        # Create/Update customer
        if action == "create_customer":
            customer_id = request.form.get("customer_id", "").strip()
            name = request.form.get("name", "").strip()

            if customer_id:
                existing = next((c for c in customers if c["customer_id"] == customer_id), None)
                if not existing:
                    customers.append({
                        "customer_id": customer_id,
                        "name": name,
                        "purchases": 0,
                        "redeemed": 0
                    })
                else:
                    # allow updating name if provided
                    if name:
                        existing["name"] = name

                save_rewards(customers)

            return redirect(url_for("rewards"))

        # Add purchase to a customer
        if action == "add_purchase":
            customer_id = request.form.get("customer_id", "").strip()
            amount = request.form.get("amount", "1").strip()

            try:
                amount_int = int(amount)
            except ValueError:
                amount_int = 1

            if amount_int < 1:
                amount_int = 1

            cust = next((c for c in customers if c["customer_id"] == customer_id), None)
            if cust:
                cust["purchases"] = int(cust.get("purchases", 0)) + amount_int
                save_rewards(customers)

            return redirect(url_for("rewards"))

    # filter/search
    filtered = customers
    if search_query:
        filtered = [
            c for c in customers
            if search_query in c.get("customer_id", "").lower()
            or search_query in c.get("name", "").lower()
        ]

    # add computed fields for display
    display_customers = []
    for c in filtered:
        c2 = dict(c)
        c2["reward_balance"] = compute_reward_balance(c)
        c2["next_reward_at"] = ((c.get("purchases", 0) // 3) + 1) * 3  # next threshold
        display_customers.append(c2)

    # sort by most purchases desc
    display_customers.sort(key=lambda x: x.get("purchases", 0), reverse=True)

    return render_template(
        "rewards.html",
        customers=display_customers,
        search_query=search_query
    )

@app.route("/rewards/redeem/<customer_id>", methods=["POST"])
def redeem_reward(customer_id):
    customers = load_rewards()
    cust = next((c for c in customers if c["customer_id"] == customer_id), None)
    if cust:
        if compute_reward_balance(cust) > 0:
            cust["redeemed"] = int(cust.get("redeemed", 0)) + 1
            save_rewards(customers)
    return redirect(url_for("rewards"))

# ==================== CATALOG ROUTES ====================

@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    """Display and manage parts catalog with images"""
    catalog_items = load_catalog()
    search_query = request.args.get("search", "").strip().lower()
    category_filter = request.args.get("category", "").strip()
    
    if request.method == "POST":
        action = request.form.get("action", "").strip()
        
        # Add new part
        if action == "add_part":
            part_id = request.form.get("part_id", "").strip()
            name = request.form.get("name", "").strip()
            category = request.form.get("category", "").strip()
            price = request.form.get("price", "0").strip()
            stock = request.form.get("stock", "0").strip()
            description = request.form.get("description", "").strip()
            
            # Handle image upload
            image_path = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(f"{part_id}_{file.filename}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_path = f"/static/uploads/{filename}"
            
            # Validate required fields
            if part_id and name and category:
                try:
                    price_float = float(price)
                    stock_int = int(stock)
                except ValueError:
                    price_float = 0.0
                    stock_int = 0
                
                new_part = {
                    "part_id": part_id,
                    "name": name,
                    "category": category,
                    "price": price_float,
                    "stock": stock_int,
                    "description": description,
                    "image": image_path
                }
                
                # Check if part already exists
                existing = next((p for p in catalog_items if p["part_id"] == part_id), None)
                if not existing:
                    catalog_items.append(new_part)
                    save_catalog(catalog_items)
        
        # Update stock
        elif action == "update_stock":
            part_id = request.form.get("part_id", "").strip()
            stock = request.form.get("stock", "0").strip()
            
            try:
                stock_int = int(stock)
            except ValueError:
                stock_int = 0
            
            part = next((p for p in catalog_items if p["part_id"] == part_id), None)
            if part:
                part["stock"] = stock_int
                save_catalog(catalog_items)
        
        # Delete part
        elif action == "delete_part":
            part_id = request.form.get("part_id", "").strip()
            catalog_items = [p for p in catalog_items if p["part_id"] != part_id]
            save_catalog(catalog_items)
        
        # Add to cart from catalog
        elif action == "add_to_cart_from_catalog":
            part_id = request.form.get("part_id", "").strip()
            quantity = request.form.get("quantity", "1").strip()
            
            part = next((p for p in catalog_items if p["part_id"] == part_id), None)
            if part:
                try:
                    quantity_int = int(quantity)
                except ValueError:
                    quantity_int = 1
                
                cart = load_cart()
                existing = next((item for item in cart if item["item_name"] == part["name"]), None)
                if existing:
                    existing["quantity"] += quantity_int
                else:
                    cart.append({
                        "item_name": part["name"],
                        "price": part["price"],
                        "quantity": quantity_int
                    })
                save_cart(cart)
        
        return redirect(url_for("catalog", search=search_query, category=category_filter))
    
    # Get unique categories
    categories = sorted(set(p.get("category", "Other") for p in catalog_items if p.get("category")))
    
    # Filter catalog
    filtered_catalog = catalog_items
    
    if category_filter:
        filtered_catalog = [p for p in filtered_catalog if p.get("category") == category_filter]
    
    if search_query:
        filtered_catalog = [
            p for p in filtered_catalog
            if search_query in p.get("part_id", "").lower()
            or search_query in p.get("name", "").lower()
            or search_query in p.get("category", "").lower()
            or search_query in p.get("description", "").lower()
        ]
    
    return render_template(
        "catalog.html",
        catalog=filtered_catalog,
        categories=categories,
        search_query=search_query,
        category_filter=category_filter
    )

# ==================== ORDERS & CART ROUTES ====================

@app.route("/orders", methods=["GET", "POST"])
def orders():
    """Display orders and shopping cart"""
    orders_list = load_orders()
    cart = load_cart()
    search_query = request.args.get("search", "").strip().lower()

    if request.method == "POST":
        action = request.form.get("action", "").strip()

        # Add item to cart
        if action == "add_to_cart":
            item_name = request.form.get("item_name", "").strip()
            price = request.form.get("price", "0").strip()
            quantity = request.form.get("quantity", "1").strip()

            try:
                price_float = float(price)
                quantity_int = int(quantity)
            except ValueError:
                price_float = 0.0
                quantity_int = 1

            if item_name and price_float > 0:
                # Check if item already in cart
                existing = next((item for item in cart if item["item_name"] == item_name), None)
                if existing:
                    existing["quantity"] += quantity_int
                else:
                    cart.append({
                        "item_name": item_name,
                        "price": price_float,
                        "quantity": quantity_int
                    })
                save_cart(cart)

            return redirect(url_for("orders"))

        # Remove item from cart
        if action == "remove_from_cart":
            item_name = request.form.get("item_name", "").strip()
            cart = [item for item in cart if item["item_name"] != item_name]
            save_cart(cart)
            return redirect(url_for("orders"))

        # Update cart item quantity
        if action == "update_cart_quantity":
            item_name = request.form.get("item_name", "").strip()
            quantity = request.form.get("quantity", "1").strip()

            try:
                quantity_int = int(quantity)
            except ValueError:
                quantity_int = 1

            if quantity_int < 1:
                quantity_int = 1

            for item in cart:
                if item["item_name"] == item_name:
                    item["quantity"] = quantity_int
                    break

            save_cart(cart)
            return redirect(url_for("orders"))

        # Checkout - convert cart to order
        if action == "checkout":
            if cart:
                import datetime
                order_id = f"ORD{len(orders_list) + 1001}"
                
                total = sum(item["price"] * item["quantity"] for item in cart)
                
                # Get customer details
                customer_name = request.form.get("customer_name", "Guest").strip()
                customer_phone = request.form.get("customer_phone", "").strip()
                customer_email = request.form.get("customer_email", "").strip()
                order_notes = request.form.get("order_notes", "").strip()
                
                new_order = {
                    "order_id": order_id,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone,
                    "customer_email": customer_email,
                    "order_notes": order_notes,
                    "items": cart.copy(),
                    "total": round(total, 2),
                    "status": "Pending",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                orders_list.append(new_order)
                save_orders(orders_list)
                
                # Clear cart after checkout
                save_cart([])
                cart = []

            return redirect(url_for("orders"))

        # Update order status
        if action == "update_order_status":
            order_id = request.form.get("order_id", "").strip()
            new_status = request.form.get("status", "").strip()

            order = next((o for o in orders_list if o["order_id"] == order_id), None)
            if order and new_status:
                order["status"] = new_status
                save_orders(orders_list)

            return redirect(url_for("orders"))

    # Calculate cart totals
    cart_total = sum(item["price"] * item["quantity"] for item in cart)
    cart_item_count = sum(item["quantity"] for item in cart)

    # Filter orders by search
    filtered_orders = orders_list
    if search_query:
        filtered_orders = [
            o for o in orders_list
            if search_query in o.get("order_id", "").lower()
            or search_query in o.get("customer_name", "").lower()
            or search_query in o.get("status", "").lower()
        ]

    # Sort orders by most recent
    filtered_orders = sorted(filtered_orders, key=lambda x: x.get("date", ""), reverse=True)

    return render_template(
        "orders.html",
        orders=filtered_orders,
        cart=cart,
        cart_total=round(cart_total, 2),
        cart_item_count=cart_item_count,
        search_query=search_query
    )

@app.route("/orders/delete/<order_id>", methods=["POST"])
def delete_order(order_id):
    """Delete an order"""
    orders_list = load_orders()
    orders_list = [o for o in orders_list if o["order_id"] != order_id]
    save_orders(orders_list)
    return redirect(url_for("orders"))

@app.route("/orders/edit/<order_id>", methods=["GET", "POST"])
def edit_order(order_id):
    """Edit an existing order"""
    orders_list = load_orders()
    order = next((o for o in orders_list if o["order_id"] == order_id), None)
    
    if not order:
        return redirect(url_for("orders"))
    
    if request.method == "POST":
        # Update order details
        order["customer_name"] = request.form.get("customer_name", "").strip()
        order["customer_phone"] = request.form.get("customer_phone", "").strip()
        order["customer_email"] = request.form.get("customer_email", "").strip()
        order["order_notes"] = request.form.get("order_notes", "").strip()
        order["status"] = request.form.get("status", "Pending").strip()
        
        save_orders(orders_list)
        return redirect(url_for("orders"))
    
    return render_template("edit_order.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)
