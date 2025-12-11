from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store job data
DATA_FILE = "jobs_data.json"

def load_jobs():
    """Load jobs from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    # Default jobs if file doesn't exist
    return [
        {"job_id": "JC1234", "status": "Open",   "remarks": "Initial review", "assigned_to": "Alice"},
        {"job_id": "JC5678", "status": "Closed", "remarks": "Completed",      "assigned_to": "Bob"},
    ]

def save_jobs(jobs):
    """Save jobs to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)

# Load jobs from file
jobs = load_jobs()

@app.route("/", methods=["GET", "POST"])
def home():
    global jobs
    jobs = load_jobs()  # Reload jobs to ensure fresh data
    search_query = request.args.get("search", "").strip().lower()
    
    if request.method == "POST":
        # get form values
        job_id = request.form.get("job_id", "").strip()
        status = request.form.get("status", "").strip()
        remarks = request.form.get("remarks", "").strip()
        assigned_to = request.form.get("assigned_to", "").strip()

        # basic validation
        if job_id and status:
            jobs.append({
                "job_id": job_id,
                "status": status,
                "remarks": remarks,
                "assigned_to": assigned_to,
            })
            # Save to file after adding
            save_jobs(jobs)

        # redirect so refresh doesn't resubmit the form
        return redirect(url_for("home"))
    
    # Filter jobs based on search query
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
    jobs = load_jobs()  # Reload jobs to ensure fresh data
    # Find the job to update
    job = next((j for j in jobs if j["job_id"] == job_id), None)
    
    if not job:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        # Update job fields
        job["status"] = request.form.get("status", "").strip()
        job["remarks"] = request.form.get("remarks", "").strip()
        job["assigned_to"] = request.form.get("assigned_to", "").strip()
        
        # Save to file
        save_jobs(jobs)
        return redirect(url_for("home"))
    
    return render_template("update.html", job=job)

@app.route("/delete/<job_id>", methods=["POST"])
def delete(job_id):
    global jobs
    jobs = load_jobs()  # Reload jobs to ensure fresh data
    # Filter out the job to delete
    jobs = [j for j in jobs if j["job_id"] != job_id]
    
    # Save to file
    save_jobs(jobs)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
