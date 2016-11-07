from flask import Flask, abort
from flask import render_template
from flask import request, url_for

from person import *
from post import *
from password_checker import *

from neo4j.v1 import GraphDatabase, basic_auth

"""
Driver and session to interact with graph db
"""
driver = GraphDatabase.driver("bolt://localhost:7687/", auth=basic_auth("neo4j", "asdf"))
session = driver.session()

app = Flask(__name__)

def validate_login(username, password):
    """
    Function to check for valid username and password combo
    :param username: Username
    :param password: Password
    :return: True if valid login
    """
    query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username, a.password AS retr_password" % username
    result = session.run(query)
    i = 0
    for item in result:
        if item['retr_password'] != password:
            return False
        else:
            return True
    return False


def validate_unique_username(username):
    """
    Function that checks for unique username
    :param username: Username
    :return: True if valid username
    """
    if username_check(username) == False:
        return False
    query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username" % username
    result = session.run(query)
    i = 0
    for item in result:
        i += 1
    if result == [] or result == None or i == 0:
        return True
    return False

def validate_password_characteristics(password):
    """
    Function to check password format
    :param password: Password
    :return: True if valid Password
    """
    valid = password_check(password)
    if valid == True:
        return True
    else:
        return False

def get_user(username):
    """
    Function that checks for unique username
    :param username: Username
    :return: True if valid username
    """
    query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username, a.password AS retr_password, a.first_name AS retr_first_name, a.last_name AS retr_last_name, a.email_id AS retr_email_id" % username
    result = session.run(query)
    for item in result:
        return Person(item['retr_first_name'], item['retr_last_name'], item['retr_username'], item['retr_email_id'])

def insert_into_graphdb(query):
    """
    Function that checks for unique username
    :param username: Username
    :return: True if valid username
    """
    session.run(query)

def get_all_mypokes(username):
    query = "MATCH (ee:Person)-[:OWNS_COMMENT]-(comments) WHERE ee.user_name='%s' RETURN comments" % (username)
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        final.append(item[0]['comment'])
    return final


@app.route("/")
def login():
    """
    Handles Login Page
    :return: Renders Template
    """
    return render_template('login_signup.html')

@app.route("/", methods=['POST'])
def login_post():
    """
    Handles POST Login
    :return: Renders Template
    """
    username = request.form['username']
    password = request.form['password']

    valid_login = validate_login(username, password)

    if valid_login == True:
        curr_user = get_user(username)
        return render_template('user_home.html', user=curr_user)
    else:
        return render_template('invalid_login_signup.html')


@app.route("/<path:login_url>")
def my_pokes(login_url):
    """
    Handles myPokes Rendering
    :return: Renders Template
    """
    split = login_url.split('/')
    username = split[0]
    curr_user = get_user(username)
    comments = get_all_mypokes(username)

    if len(split) == 1:
        return render_template('user_home.html', user=curr_user)
    else:
        if split[1] == 'my_pokes':
            return render_template('my_pokes.html', user=curr_user, comments=comments)
        elif split[1] == username:
            return render_template('user_home.html', user=curr_user)
        elif split[1] == '':
            pass

@app.route("/signup", methods=['POST'])
def sign_up_post():
    """
    Handles POST sign up
    :return: Renders Template
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_name = request.form['user_name']
    email_id = request.form['email_id']
    password = request.form['password']

    valid_user_name = validate_unique_username(user_name)
    valid_password = validate_password_characteristics(password)
    if valid_user_name == True and valid_password == True:
        query = "CREATE (a:Person {user_name: '%s', first_name: '%s' , last_name: '%s' , email_id: '%s' , password: '%s' })" % (user_name, first_name, last_name, email_id, password)
        insert_into_graphdb(query)
        curr_user = Person(first_name, last_name, user_name, email_id)
        return render_template('user_home.html', user=curr_user)
    else:
        return render_template('invalid_login_signup.html')

@app.route("/<path:comment_owner>/my_pokes", methods=['POST'])
def add_comment_mypoke(comment_owner):
    """
    Handles POST sign up
    :return: Renders Template
    """
    to_user = request.form['names']
    comment = request.form['comment']
    curr_user = get_user(comment_owner)
    #assume only self comments for now. So to_user is currently blank
    query = "MATCH (ee:Person) WHERE ee.user_name = '%s' CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (ee)-[:OWNS_COMMENT]->(c)" % (comment_owner, comment, comment_owner)
    insert_into_graphdb(query)

    comments = get_all_mypokes(comment_owner)

    return render_template('my_pokes.html', user=curr_user, comments=comments)


if __name__ == "__main__":
    app.run(debug=True)
