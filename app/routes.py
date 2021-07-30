from flask import render_template, flash, redirect, url_for, request
from app import app, db, plots
from app.forms import LoginForm, RegistrationForm, JournalForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB
from werkzeug.urls import url_parse
# from .othello import project_4_user_interface as ui
from datetime import datetime, date, timedelta

@app.route('/')
@app.route('/HTML Project 1')
def home():
    return render_template('HTML Project 1.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    post_list = PostDB.query.all()

    form = JournalForm()
    if form.delete.data:

        if post_list:
            db.session.delete(post_list[-1])
            db.session.commit()

        return redirect(url_for("journal"))

    if form.validate_on_submit():
        post_obj = PostDB(post=form.post.data, post_date=form.post_date.data)
        db.session.add(post_obj)
        db.session.commit()
        return redirect(url_for("journal"))

    if current_user.is_anonymous:
        name_used = "anonymous"
    else:
        name_used = current_user.username

    return render_template('journal.html', post_list=post_list, username=name_used, form=form)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')

#####################################################
# Everything tied to exercise portion enclosed here #
#####################################################
@app.route('/routine')
@login_required
def routine_entry():
    """Ephemeral url space that automatically redirects to the routine page and avoids a 404"""
    return redirect(url_for('routine', username=current_user.username))

@app.route('/routine/<username>', methods=['GET', 'POST'])
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

    if int(days_passed) > 1:
        # Old Streak clean-up
        user.streak.streak_end = date.today()

        # New Streak set-up
        streak = Streak(total_count=0, streak_begin=date.today(), user=user, old_user=user.username)
        db.session.add(streak)
        user.last_exercised = date.today()
        user.streak = streak
        user.daily_count = 0
        db.session.commit()

    elif int(days_passed) == 1:
        user.daily_count = 0
        user.last_exercised = date.today()
        db.session.commit()

    if request.method == 'POST':
        user.daily_count = user.daily_count + 1

        if user.daily_count >= 5:
            user.streak.total_count = user.streak.total_count + 1

        db.session.commit()

    return render_template('routine.html', user=user, streak=user.streak)

@app.route('/exercisetop')
def exercise_top():
    """Creates a plot of the best streaks using the streak data"""
    png_image = plots.create_streak_plt(Streak.query.all())
    return render_template('exercisetop.html', image=png_image)

@app.route('/streak/<username>')
@login_required
def past_streak(username):
    """Gets all the past streak values of the current user"""
    streak_list = []
    all_streaks = Streak.query.all()

    for streak in all_streaks:
        if username == streak.old_user:

            if streak.streak_end is not None:
                streak_list.append(streak)

    return render_template('paststreak.html', streaks=streak_list)
##################################################################
#    ^^^^^^^^^         Exercise portion end     ^^^^^^^^         #
##################################################################


@app.route('/games')
@login_required
def games():
    return render_template('games.html')

@app.route('/othello', methods=['POST'])
def play_othello():
    # ui.run_user_interface()
    return redirect(url_for('games'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered...!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Secret url used exclusively for testing purposes
@app.route('/test', methods=['GET', 'POST'])
def test():
    test_string = "<p><b>This is</b> a test</p>"
    return render_template('test.html', test_string=test_string)
