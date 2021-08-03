from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, UsernameForm, PasswordForm
from app.journal.forms import JournalForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB
from werkzeug.urls import url_parse
from datetime import datetime, date, timedelta

@bp.route('/settings/<username>', methods=['GET', 'POST'])
@login_required
def settings(username):

    if current_user.username != username:
        return redirect(url_for('main.home'))

    return render_template('auth/settings.html')

@bp.route('/settings/<username>/change_username', methods=['GET', 'POST'])
@login_required
def settings_username(username):

    if current_user.username != username:
        return redirect(url_for('main.home'))

    form = UsernameForm()

    if form.validate_on_submit():
        update_old_streaks(current_user, form.new_username.data)
        current_user.set_username(form.new_username.data)
        db.session.commit()
        flash('Username successfully changed...!')
        return redirect(url_for('auth.settings_username', username=current_user.username))

    return render_template('auth/settings_username.html', user=username, form=form)

def update_old_streaks(current_user, new_username):
    """Updates all the old streaks when a user changes their name"""
    streaks = Streak.query.all()
    for streak in streaks:
        if streak.old_user == current_user.username:
            streak.old_user = new_username
            db.session.commit()


@bp.route('/settings/<username>/change_password', methods=['GET', 'POST'])
@login_required
def settings_password(username):

    if current_user.username != username:
        return redirect(url_for('main.home'))

    form = PasswordForm()

    if form.validate_on_submit():

        if not current_user.check_password(form.old_password.data):
            flash('Invalid password confirmation')
            return redirect(url_for('auth.settings_password', username=username))

        if current_user.check_password(form.new_password.data):
            flash('Password unchanged')
            return redirect(url_for('auth.settings_password', username=username))

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password successfully changed...!')
        return redirect(url_for('auth.settings_password', username=username))

    return render_template('auth/settings_password.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered...!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
