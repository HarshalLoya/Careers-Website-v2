from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from database import get_user_by_email, add_user_to_db, load_jobs_from_db, load_job_with_id, add_application_to_db
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET_KEY', 'fallback-secret-key')


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template("home.html", jobs=jobs)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if get_user_by_email(email):
      flash('Email already exists. Please log in.')
      return redirect(url_for('login'))

    add_user_to_db(username, email, password)
    flash('Signup successful! Please log in.')
    return redirect(url_for('login'))

  return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = get_user_by_email(email)

    if user and check_password_hash(user['password_hash'], password):
      session['user_id'] = user['id']
      session['username'] = user['username']
      flash('Login successful!')
      return redirect(url_for('hello_world'))
    else:
      flash('Invalid email or password.')
      return redirect(url_for('login'))

  return render_template('login.html')


@app.route('/logout')
def logout():
  session.pop('user_id', None)
  session.pop('username', None)
  flash('Logged out successfully!')
  return redirect(url_for('login'))


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id):
  job = load_job_with_id(id)
  if not job:
    return "Not Found", 404
  else:
    return render_template('jobpage.html', job=job)


@app.route("/api/jobs/<id>")
def show_job_json(id):
  job = load_job_with_id(id)
  return jsonify(job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_with_id(id)
  add_application_to_db(id, data)
  return render_template('application_sbumitted.html',
                         application=data,
                         job=job)


@app.route('/faqs')
def faqs():
  return render_template('faqs.html')


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
