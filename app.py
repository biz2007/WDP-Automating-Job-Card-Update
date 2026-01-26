from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
