from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main import bp
from app.exercise import plots
from app.auth.forms import LoginForm, RegistrationForm
from app.journal.forms import JournalForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB
from werkzeug.urls import url_parse
from datetime import datetime, date, timedelta

@bp.route('/')
def home():
    return render_template('HTML Project 1.html')

@bp.route('/music')
def music():
    return render_template('music.html')

@bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

@bp.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')

@bp.route('/games')
@login_required
def games():
    return render_template('games.html')

@bp.route('/othello', methods=['POST'])
def play_othello():
    return redirect(url_for('games'))


# Secret url used exclusively for testing purposes
@bp.route('/test', methods=['GET', 'POST'])
def test():
    test_string = "<p><b>This is</b> a test</p>"
    return render_template('test.html', test_string=test_string)
