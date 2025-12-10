from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# “database”
jobs = [
    {"job_id": "JC1234", "status": "Open",   "remarks": "Initial review", "assigned_to": "Alice"},
    {"job_id": "JC5678", "status": "Closed", "remarks": "Completed",      "assigned_to": "Bob"},
]

@app.route("/", methods=["GET", "POST"])
def home():
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

        # redirect so refresh doesn’t resubmit the form
        return redirect(url_for("home"))
    
    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)
