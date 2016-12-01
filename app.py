#!/usr/bin/env python
# coding=utf-8

from json import loads, dumps
from urllib3 import HTTPSConnectionPool, disable_warnings
from urlparse import parse_qs
from signal import signal, SIGPIPE, SIG_DFL

from helper import calculate_rate, calculate_age, get_plan_name, get_income_addition
from preprocessing import process_fb_json
from data_analysis import get_deltas
from get_tweets import get_all_tweets

import logging
import flask
from flask import Flask, session, render_template, url_for, request, redirect

app = flask.Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

FACEBOOK_APP_ID="273803779683669"
FACEBOOK_APP_SECRET="5824e17970319800be2ef29206348b01"
GRAPH_API_VERSION="v2.8"
REDIRECT_URI="http://localhost:5000/callback"
FB_POSTS_LIMIT = 1000

TOKENS = {}
signal(SIGPIPE,SIG_DFL)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
disable_warnings()

class NotAuthorizedException(Exception):
    pass


class FacebookConnection(HTTPSConnectionPool):
    """
    Convenience class to that wraps connection and call to Graph API
    """
    def __init__(self):
        super(FacebookConnection, self).__init__('graph.facebook.com')

    def __call__(self, method, url, token, http_headers, request_body):
        if http_headers is None:
            http_headers = {}

        if token is not None:
            http_headers["Authorization"] = "Bearer %s" % token

        return self.urlopen(method, url, headers=http_headers, body=request_body)

FACEBOOK_CONNECTION=FacebookConnection()



# OAuth functions


def get_app_token():
    """
    Get an app token based on app ID and secret
    """

    try:
        response = FACEBOOK_CONNECTION(
            'GET',
            '/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials'
            % (FACEBOOK_APP_ID, FACEBOOK_APP_SECRET),
            None, None, None)

        return parse_qs(response.data.decode("utf-8"))["access_token"]
    except KeyError:
        logging.log(logging.ERROR, response.data)
        raise NotAuthorizedException("Authorization error", "App access token not found")
    except:
        raise


def get_user_token(code):
    try:
        response = FACEBOOK_CONNECTION(
            'GET',
            '/%s/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s'
            % (GRAPH_API_VERSION, FACEBOOK_APP_ID, REDIRECT_URI, FACEBOOK_APP_SECRET, code),
            None, None, None)

        return loads(response.data.decode("utf-8"))["access_token"]
    except KeyError:
        logging.log(logging.ERROR, response.data)
        raise NotAuthorizedException("Authorization error", "User access token not found")
    except:
        raise

# App routes
@app.route("/")
def home_page():
    """
    Renders home page
    """

    # Check whether the user has authorized the app. If authorized, login button will not be displayed
    user_authorized = True if "user_token" in TOKENS else False

    return flask.render_template("index.html", authorized=user_authorized)

@app.route("/viewplans", methods=['POST'])
def view_plans():
    """
    Redirects the user to the Facebook login page to authorize the app:
    - response_type=code
    - Scope requests is to access user posts

    :return: Redirects to the Facebook login page
    """

    if request.form['date'] != '':
        session['age'] = calculate_age(request.form['date'])

    session['income'] = request.form['income']
    print(session['income'])
    session['zipcode'] = request.form['zipcode']
    base_rate = calculate_rate(session['zipcode'], session['age'])
    session['base_rate'] = base_rate

    if request.form['twitter'] != '' :
        session['analyse_twitter'] = True
        session['twitter_handle'] = request.form['twitter']
    else:
        session['analyse_twitter'] = False
    if 'with_fb' in request.form:
        session['analyse_fb'] = True
    else:
        session['analyse_fb'] = False
    if 'with_fb' in request.form:
        print("Logging in with FB")
        return flask.redirect("https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=user_posts"
                % (FACEBOOK_APP_ID, REDIRECT_URI))
    elif 'without_fb' in request.form:
        print("Logging in without FB")
        user_authorized = True if "user_token" in TOKENS else False
        return flask.render_template("insurance_plans.html", \
                rate = session['base_rate'], age = session['age'])


@app.route("/callback")
def handle_callback():
    """
    Handles callback after user authorization of app, calling back to exchange code for access token

    :return:
    """
    global TOKENS

    try:
        TOKENS["user_token"] = get_user_token(flask.request.args.get("code"))
        return flask.redirect("/showplans")
    except NotAuthorizedException:
        return 'Access was not granted or authorization failed', 403
    except:
        raise

@app.route("/showplans")
def show_plans():
    user_authorized = True if "user_token" in TOKENS else False
    return flask.render_template("insurance_plans.html", \
            rate = session['base_rate'], age = session['age'])

@app.route("/calculaterate", methods=["GET"])
def get_rate():
    #Default premium add is
    total_premium_add = 15
    posts = ''

    plan_code = request.args.get('plancode')
    plan_details = get_plan_name(plan_code)
    plan_name = plan_details[0]

    income_addition_rate = get_income_addition(session['income'])

    _base_rate = session['base_rate'] + plan_details[1] + income_addition_rate

    if (session['analyse_fb'] == True):
        fb_text = get_fb_posts()
        posts = fb_text

    if (session['analyse_twitter'] == True):
        twitter_posts = get_all_tweets(session['twitter_handle'])
        twitter_text = u". ".join(twitter_posts)
        posts = posts + '. ' + twitter_text

    if(session['analyse_twitter'] == True or session['analyse_fb'] == True):
        total_premium_add = get_deltas(posts)
    else:
        result_list = []
        result_list.append({'attribute' : 'Alcohol', 'sentiment' : 'Neutral', 'relevance' : 0, 'delta' : 0, 'factor' : 0.5})
        result_list.append({'attribute' : 'Drugs', 'sentiment' : 'Neutral', 'relevance' : 0, 'delta' : 0, 'factor' : 0.62} )
        result_list.append({'attribute' : 'Smoking', 'sentiment' : 'Neutral', 'relevance' : 0, 'delta' : 0, 'factor' : 0.7} )
        result_list.append({'attribute' : 'Lifestyle', 'sentiment' : 'Neutral', 'relevance' : 0, 'delta' : 0, 'factor' : 0.34})
        result_list.append({'attribute' : 'Healthy', 'sentiment' : 'Neutral', 'relevance' : 0, 'delta' : 0, 'factor' : 1.0})
        session['result_list'] = result_list

    #Base rate should not be lowered
    if(total_premium_add < 0):
        total_premium_add = 0

    #final_rate = session['base_rate'] + total_premium_add + income_addition_rate

    return flask.render_template("viewPlanDetails.html", \
            base_rate = _base_rate, delta = total_premium_add, \
            result = session['result_list'], \
            code = plan_code, name = plan_name)


def get_fb_posts():
    global TOKENS

    # Make sure there is a token
    try:
        token = TOKENS["user_token"]
    except KeyError:
        return 'Not authorized', 401

    # Get FB posts upto FB_POSTS_LIMIT
    try:
        response = FACEBOOK_CONNECTION(
            'GET',
            '/%s/me/posts?limit=%s' % (GRAPH_API_VERSION, FB_POSTS_LIMIT),
            token,
            None,
            None)

        if response.status != 200:
            logging.log(logging.ERROR, response.data)
            return 'Unexpected HTTP return code from Facebook: %s' % response.status, response.status

    except Exception as e:
        logging.log(logging.ERROR, str(e))
        return 'Unknown error calling Graph API', 502

    """
    Response format:
    {
        "paging" : {
            "next" : "https://graph.facebook.com/v2.8/12......."
            "previous" : "https://graph.facebook.com/v2.8/..."
        }
        "data" : [
                    {"created_time" : "...", "message" : "Chilling...", "story" : "Patrick Doyle at Carowinds.", "id" : "..."},
                    {....},
                    {....}
                ]
    }
    """

    #Get user posts from response which fetches posts upto specified limit
    posts = loads(response.data.decode("utf-8"))["data"]

    message_list, story_list = process_fb_json(posts)
    msg_concat = u". ".join(message_list)

    return msg_concat
    #Convert json to string & indent for pretty printing
    #osts_prettified = dumps(posts, indent=4, separators=(',', ': '))
    #print (dumps(posts,sort_keys=True, indent=4, separators=(',', ': ')))

    #return flask.render_template("posts.html", posts=posts_prettified, zipcode1 = session['zipcode'])
    #return flask.render_template("messages.html", posts=msg_concat, zipcode1 = session['zipcode'])

if __name__ == '__main__':
    # Register an app token at start-up (purely as validation that configuration for Facebook is correct)
    TOKENS["app_token"] = get_app_token()
    app.run(debug=True, threaded=True)
