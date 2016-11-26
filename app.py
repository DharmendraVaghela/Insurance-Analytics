#!/usr/bin/env python
# coding=utf-8



from json import loads, dumps
from urllib3 import HTTPSConnectionPool, disable_warnings
from urlparse import parse_qs

from calculate_rate import calculate_rate

import logging
import flask

app = flask.Flask(__name__)

FACEBOOK_APP_ID="<Your app ID>"
FACEBOOK_APP_SECRET="<Your app secret>"
GRAPH_API_VERSION="v2.8"
REDIRECT_URI="http://localhost:5000/callback"
FB_POSTS_LIMIT = 1000

TOKENS = {}

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


@app.route("/authorize")
def authorize_facebook():
    """
    Redirects the user to the Facebook login page to authorize the app:
    - response_type=code
    - Scope requests is to access user posts

    :return: Redirects to the Facebook login page
    """
    return flask.redirect("https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=user_posts"
                    % (FACEBOOK_APP_ID, REDIRECT_URI))

@app.route("/callback")
def handle_callback():
    """
    Handles callback after user authorization of app, calling back to exchange code for access token

    :return:
    """
    global TOKENS

    try:
        TOKENS["user_token"] = get_user_token(flask.request.args.get("code"))
        return flask.redirect("/")
    except NotAuthorizedException:
        return 'Access was not granted or authorization failed', 403
    except:
        raise

def post_action(post):
    """
    Do something with a user post
    """
    print(post)

@app.route("/getrate", methods=["GET"])
def get_rate():
    rate = calculate_rate('27606', 26)

    return flask.render_template("show_rate.html", my_rate=rate)

@app.route("/getfeed", methods=["GET"])
def get_posts():
    global TOKENS

    # Make sure there is a token
    try:
        token = TOKENS["user_token"]
    except KeyError:
        return 'Not authorized', 401

    # Get a place id to include in the post, search for coffee within 10000 metres and grab first returned
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

    #[post_action(post=post) for post in posts['data']]

    #Convert json to string & indent for pretty printing
    posts_prettified = dumps(posts, indent=4, separators=(',', ': '))
    #print (dumps(posts,sort_keys=True, indent=4, separators=(',', ': ')))

    return flask.render_template("posts.html", posts=posts_prettified)

if __name__ == '__main__':
    # Register an app token at start-up (purely as validation that configuration for Facebook is correct)
    TOKENS["app_token"] = get_app_token()
    app.run(debug=True)
