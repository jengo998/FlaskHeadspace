from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.journal import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.journal.forms import JournalForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB
from werkzeug.urls import url_parse
from datetime import datetime, date, timedelta

@bp.route('/journal', methods=['GET', 'POST'])
def journal():

    form = JournalForm()
    if form.delete.data:
        post_list = PostDB.query.all()

        if post_list:
            db.session.delete(post_list[-1])
            db.session.commit()

        return redirect(url_for("journal.journal"))

    if form.validate_on_submit():
        post_obj = PostDB(post=form.post.data, post_date=form.post_date.data)
        db.session.add(post_obj)
        db.session.commit()
        return redirect(url_for("journal.journal"))

    if current_user.is_anonymous:
        name_used = "anonymous"
    else:
        name_used = current_user.username

    post_pagination, next_url, prev_url = handle_journal_pagination()
    return render_template('journal/journal.html', post_list=reversed(post_pagination.items), username=name_used,
                           form=form, next_url=next_url, prev_url=prev_url)

def handle_journal_pagination():
    """Handles the pagination of journal entries"""
    page = request.args.get('page', 1, type=int)
    reverse_query = PostDB.query.order_by(PostDB.id.desc())
    post_list = reverse_query.paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = None
    if post_list.has_next:
        next_url = url_for('journal.journal', page=post_list.next_num)

    prev_url = None
    if post_list.has_prev:
        prev_url = url_for('journal.journal', page=post_list.prev_num)

    return post_list, next_url, prev_url