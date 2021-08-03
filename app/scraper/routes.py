from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.scraper import bp, plots_scraper
from app.auth.forms import LoginForm, RegistrationForm
from app.scraper.forms import ItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Streak, PostDB, EbayItem
from werkzeug.urls import url_parse
from datetime import datetime, date, timedelta
from app.scraper import webscraper
import statistics

@bp.route('/prices', methods=['GET', 'POST'])
def prices():

    form = ItemForm()
    
    if form.validate_on_submit():

        # If there is no Ebay item in the database already
        if not EbayItem.query.all():
            price_list = get_item_prices(form.item.data)
            mean_val, median_val = get_mean_median(price_list)
            png_image = plots_scraper.create_item_plt(price_list, form.item.data)

            item = EbayItem(item_name=form.item.data, png_image=png_image, mean=mean_val, median=median_val)
            db.session.add(item)
            db.session.commit()

        # Updates the existing Ebay item
        else:
            price_list = get_item_prices(form.item.data)
            mean_val, median_val = get_mean_median(price_list)
            new_png_image = plots_scraper.create_item_plt(price_list, form.item.data)

            existing_item = EbayItem.query.all()[0]
            existing_item.item_name = form.item.data
            existing_item.png_image = new_png_image
            existing_item.last_updated = date.today()
            existing_item.mean = mean_val
            existing_item.median = median_val
            db.session.commit()

    try:
        item_obj = EbayItem.query.all()[0]
        check_week_passed(item_obj)
        graph_image = item_obj.png_image
        mean = item_obj.mean
        median = item_obj.median

    except IndexError:
        graph_image = "data:image/png;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
        mean = 0
        median = 0

    return render_template('scraper/prices.html', image=graph_image, form=form, mean=mean, median=median)


def get_item_prices(item_name):
    """Using the name of an item, gets price listings of it on Ebay"""
    
    payload = dict()
    payload.update({'_nkw': item_name})
    payload.update({'LH_Sold': '1'})
    payload.update({'LH_Complete': '1'})
    payload.update({'_fosrp': '1'})
    payload.update({'_ipg': '50'})
    
    return webscraper.produce_ebay_prices(payload)


def check_week_passed(item):
    """Checks if a week has passed since the Ebay db was last updates and makes changes"""

    today_date = date.today()
    date_difference = today_date - item.last_updated
    days_passed = str(date_difference).split()[0]
    days_passed = 0 if days_passed[0] == '0' else int(days_passed)

    if days_passed >= 7:
        price_list = get_item_prices(item.item_name)
        mean_val, median_val = get_mean_median(price_list)
        new_png_image = plots_scraper.create_item_plt(price_list, item.item_name)
        item.png_image = new_png_image
        item.last_updated = date.today()
        item.mean = mean_val
        item.median = median_val
        db.session.commit()

    return

def get_mean_median(price_list) -> tuple:
    """Gets a list of prices, converts it into floats and does statistics"""

    try:
        mean_val = statistics.fmean(price_list)
        median_val = statistics.median(price_list)

    except statistics.StatisticsError:
        mean_val = 0
        median_val = 0

    mean_val = str(round(mean_val, 2))
    return mean_val, median_val
