from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.exercise import bp, plots
from app.auth.forms import LoginForm, RegistrationForm
from app.journal.forms import JournalForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB
from werkzeug.urls import url_parse
from datetime import datetime, date, timedelta
import random

@bp.route('/routine')
@login_required
def routine_entry():
    """Ephemeral url space that automatically redirects to the routine page and avoids a 404"""
    return redirect(url_for('exercise.routine', username=current_user.username))

@bp.route('/routine/<username>', methods=['GET', 'POST'])
@login_required
def routine(username):
    """Changes the database based on the current user that enters the page"""
    user = User.query.filter_by(username=username).first_or_404()

    try:
        user.streak.total_count

    except AttributeError:
        streak = Streak(total_count=0, streak_begin=date.today(), user=user, old_user=user.username)
        db.session.add(streak)
        user.streak = streak
        db.session.commit()

    today_date = date.today()
    date_difference = today_date - user.last_exercised
    days_passed = str(date_difference).split()[0]
    days_passed = 0 if days_passed[0] == '0' else days_passed

    # Streak over, missed a day
    if int(days_passed) > 1:
        reset_streak(user)
        shuffle_seed(user)
        db.session.commit()

    # The next day...
    elif int(days_passed) == 1:

        if user.daily_count < 5:
            reset_streak(user)
            shuffle_seed(user)
            db.session.commit()

        else:
            user.daily_count = 0
            user.last_exercised = date.today()
            shuffle_seed(user)
            db.session.commit()

    # Exercise, exercise, exercise
    if request.method == 'POST':
        if user.daily_count < 5:
            user.daily_count = user.daily_count + 1

            if user.daily_count == 5:
                user.streak.total_count = user.streak.total_count + 1

        db.session.commit()

    return render_template('exercise/routine.html', user=user, streak=user.streak)

def reset_streak(user):
    """Cleans up the old streak and creates a new one"""
    # Old Streak clean-up
    end_date = user.streak.streak_begin + timedelta(days=user.streak.total_count - 1)
    user.streak.streak_end = end_date

    # New Streak set-up
    streak = Streak(total_count=0, streak_begin=date.today(), user=user, old_user=user.username)
    db.session.add(streak)
    user.streak = streak
    user.daily_count = 0
    user.last_exercised = date.today()

def shuffle_seed(user):
    """Shuffles the exercise seed for the day"""
    user.daily_seed = '01234' if user.daily_seed is None else user.daily_seed
    new_seed = list(user.daily_seed)
    random.shuffle(new_seed)
    user.daily_seed = ''.join(new_seed)


@bp.route('/get_timer')
def get_timer():
    return "timer.gif"

@bp.route('/exercisetop')
def exercise_top():
    """Creates a plot of the best streaks using the streak data"""
    png_image = plots.create_streak_plt(Streak.query.all())
    return render_template('exercise/exercisetop.html', image=png_image)

@bp.route('/streak/<username>')
@login_required
def past_streak(username):
    """Gets all the past streak values of the current user"""
    streak_list = []
    all_streaks = Streak.query.all()

    for streak in all_streaks:
        if username == streak.old_user:

            if streak.streak_end is not None:
                streak_list.append(streak)

    return render_template('exercise/paststreak.html', streaks=streak_list)
