import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "voting-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

db = SQLAlchemy(app)

# ------------------ MODELS ------------------
class Poster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image_filename = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)


class VotingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean, default=False)

# ------------------ USER SIDE ------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    """Halaman voting tanpa token"""
    status = VotingStatus.query.first()
    if not status or not status.is_open:
        flash("Voting belum dibuka atau sudah ditutup.", "warning")
        return redirect(url_for('index'))

    posters = Poster.query.all()

    if request.method == 'POST':
        poster_id = request.form['poster_id']
        poster = Poster.query.get(poster_id)

        if poster:
            poster.votes += 1
            db.session.commit()
            return render_template('finish.html')  # popup selesai

    return render_template('vote.html', posters=posters)


# ------------------ ADMIN LOGIN ------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Username atau password salah!", "danger")

    return render_template('admin_login.html')


@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    flash("Anda telah logout.", "info")
    return redirect(url_for('admin_login'))


# ------------------ ADMIN DASHBOARD ------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')


# ------------------ KELOLA POSTER ------------------
@app.route('/admin/posters', methods=['GET', 'POST'])
def admin_posters():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    posters = Poster.query.all()

    if request.method == 'POST':
        # Tambah Poster
        if 'add' in request.form:
            title = request.form['title']
            file = request.files['image']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.session.add(Poster(title=title, image_filename=filename))
                db.session.commit()
                flash("Poster berhasil diunggah!", "success")

        # Edit Poster
        elif 'edit' in request.form:
            poster = Poster.query.get(request.form['poster_id'])
            poster.title = request.form['title']
            if 'image' in request.files and request.files['image'].filename != '':
                file = request.files['image']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                poster.image_filename = filename
            db.session.commit()
            flash("Poster berhasil diperbarui!", "info")

        # Hapus Poster
        elif 'delete' in request.form:
            poster = Poster.query.get(request.form['poster_id'])
            db.session.delete(poster)
            db.session.commit()
            flash("Poster dihapus!", "danger")

        return redirect(url_for('admin_posters'))

    return render_template('admin_posters.html', posters=posters)


# ------------------ STATUS VOTING ------------------
@app.route('/admin/voting', methods=['GET', 'POST'])
def admin_voting():
    # pastikan admin sudah login
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    # ambil atau buat status voting
    status = VotingStatus.query.first()
    if not status:
        status = VotingStatus(is_open=False)
        db.session.add(status)
        db.session.commit()

    if request.method == 'POST':
        action = request.form.get('action')  # expects 'open' or 'close' from template

        if action == 'open':
            status.is_open = True
            db.session.commit()
            flash("Voting dibuka.", "success")
            return redirect(url_for('admin_voting'))

        elif action == 'close':
            status.is_open = False
            db.session.commit()
            flash("Voting ditutup.", "info")
            return redirect(url_for('admin_voting'))

        # opsional: tombol untuk menuju countdown
        elif action == 'countdown':
            return redirect(url_for('countdown'))

        else:
            flash("Aksi tidak dikenal.", "warning")
            return redirect(url_for('admin_voting'))

    # GET: tampilkan halaman dengan status terbaru
    return render_template('admin_voting.html', status=status)




# ------------------ COUNTDOWN ------------------
@app.route('/countdown')
def countdown():
    return render_template('countdown.html')


# ------------------ HASIL AKHIR ------------------
@app.route('/results')
def results():
    posters = Poster.query.order_by(Poster.votes.desc()).all()
    poster_titles = [p.title for p in posters]
    poster_votes = [p.votes for p in posters]

    return render_template(
        'results.html',
        posters=posters,
        poster_titles=poster_titles,
        poster_votes=poster_votes
    )


# ------------------ MAIN ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
