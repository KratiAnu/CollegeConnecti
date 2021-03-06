from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
#from app.forms import EditProfileForm
from .models import Note
from .models import User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

#

@views.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def getUser(email):
    return render_template("user.html", user=current_user, email=email)


@views.route('/follow/<email>')
def follow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User ' + email + ' not found.')
        return redirect(url_for('home'))
    u = current_user.follow(user)
    if u is None:
        flash('Cannot follow ' + email + '.')
        return redirect(url_for('user', email=email))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + email + '!')
    return redirect(url_for('user', email=email))


@views.route('/unfollow/<email>')
def unfollow(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User ' + email + ' not found.')
        return redirect(url_for('home'))
    u = current_user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + email + '.')
        return redirect(url_for('user', email=email))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + email + '.')
    return redirect(url_for('user', email=email))


@views.route('/faq')
@login_required
def faq():
    return render_template("faq.html", user=current_user)
