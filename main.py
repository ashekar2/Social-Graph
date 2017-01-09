from flask import Flask, abort
from flask import render_template
from flask import request, url_for

import Queue
from person import *
from post import *
from password_checker import *
from create_query import *
from prefix_tree import *

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
    query = create_validate_login(username)
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
    :param username: Username for user
    :return: True if valid given username
    """
    if username_check(username) == False:
        return False
    query = create_check_unique_username(username)
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
    query = get_create_user(username)
    result = session.run(query)
    for item in result:
        return Person(item['retr_first_name'], item['retr_last_name'], item['retr_username'], item['retr_email_id'])

def insert_into_graphdb(query):
    """
    Function executes query
    :param username: Username
    :return: True if valid username
    """
    session.run(query)

def get_all_mypokes(username):
    """
    Function that retrives pokes for a given username
    :param username: Username
    :return: list of comments
    """
    query = create_get_mypokes(username)
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        final.append(tuple((item[0]['comment'],item[0]['owner'])))
    return final

def get_all_response(comment_id):
    responses = []
    query = create_get_responses(comment_id)
    result = session.run(query)
    for c in result:
        responses.append(tuple((c[0]['comment'],c[0]['owner'])))
    return responses

def get_all_globalpokes():
    """
    Function to get all global pokes
    :return: List of comments
    """
    query = create_get_global_pokes()
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        comment_id = item[0]['id']
        responses = get_all_response(comment_id)
        global_comment = Post(comment_id, item[0]['comment_data']['owner'], item[0]['comment_data']['comment'], responses)
        final.append(global_comment)
    return final

def insert_personal_poke(comment_owner, comment):
    """
    Function inset personal pokes
    :param comment_owner: Owner of comment
    :param comment: Actual comment
    """
    query = create_personal_poke(comment_owner, comment)
    insert_into_graphdb(query)

def insert_global_poke(comment_owner, comment):
    """
    Function insert global pokes
    :param comment_owner: Owner of comment
    :param comment: Actual comment
    """
    query = create_global_poke(comment_owner, comment)
    insert_into_graphdb(query)

def insert_friends_poke(comment_owner, user_list, comment):
    """
    Function insert friends pokes
    :param comment_owner: Owner of comment
    :param comment: Actual comment
    :param user_list: list of users to share comment with
    """
    query = create_friends_poke(comment_owner, user_list, comment)
    insert_into_graphdb(query)

def insert_combo_poke(comment_owner, user_list, comment):
    """
    Function insert combo pokes
    :param comment_owner: Owner of comment
    :param comment: Actual comment
    :param user_list: list of users to share comment with
    """
    query = create_combo_poke(comment_owner, user_list, comment)
    insert_into_graphdb(query)

def validate_valid_usernames(user_list):
    """
    Function that checks for unique username
    :param username: Username
    :return: True if valid username
    """
    for u in user_list:
        if validate_unique_username(u) == True:
            return False
    return True

def handle_comment(users, comment, curr_username):
    """
    Function that classifies and inserts a comments
    :param users: List of Users
    :param comment: Actual Comment
    :param curr_username: Username
    """
    result = classify_post(users)
    if result == 0: #personal post
        insert_personal_poke(curr_username, comment)
    elif result == 1: #global post
        insert_global_poke(curr_username, comment)
    elif result[0] == 2: #friends post
        user_list = result[1]
        if validate_valid_usernames(user_list) == False:
            return -1
        insert_friends_poke(curr_username, user_list, comment)
    elif result[0] == 3: #global post
        user_list = result[1]
        if validate_valid_usernames(user_list) == False:
            return -1
        insert_combo_poke(curr_username, user_list, comment)

def get_all_friendspokes(username):
    """
    Function that retrives all friends pokes for a username
    :param username: Username
    :return: List of comments
    """
    query = create_get_friendspokes(username)
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        final.append(tuple((item[0]['comment'],item[0]['owner'])))
    return final

def create_follows_relation(username, f_username):
    """
    Function to create follow relations
    :return: Renders Template
    """
    if username == f_username:
        return None
    if f_username in get_all_follows(username):
        return None
    query = create_add_follow(username, f_username)
    session.run(query)

def get_all_follows(username):
    """
    Function to get all follow relations by username
    :param username: Username
    :return: List of comments
    """
    query = create_get_follows(username)
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        if item[0]['user_name'] in final:
            continue
        final.append(item[0]['user_name'])
    return final

def get_follow_recomendations(username):
    """
    Gets follow recomendations based on username
    :param username: Username
    :return: List of follow recos
    """
    curr_follows = get_all_follows(username)
    f_count = {}
    for f in curr_follows:
        f_follows = get_all_follows(f)
        for f_t in f_follows:
            if not(f_t in curr_follows) and not(f_t == username): #curr does not follow f_t
                if f_t in f_count:
                    f_count[f_t] += 1
                else:
                    f_count[f_t] = 1
    zip_f_count = []
    for k,v in f_count.iteritems():
        zip_f_count.append(tuple((k,v)))
    s_f_count = sorted(zip_f_count, key=lambda x: x[1], reverse=True)
    result = []
    result = s_f_count[:5]
    return result

def shortest_path(user_1, user_2):
    """
    Return shortest path if exists between two users
    :return: Renders Template
    """
    #use BFS in order to navigate from user_1 to user_2
    if(not(validate_valid_usernames([user_2]))):
        return []
    q = Queue.Queue()
    curr_user = user_1
    path = []
    coming_from = {}
    coming_from[user_1] = None
    q.put(user_1)
    i = 0
    while(not(curr_user == user_2)):
        if q.qsize() == 0:
            return []
        curr_user = q.get()
        all_follows = get_all_follows(curr_user)
        for u in all_follows:
            if not(u in coming_from) and u != user_1: #u has not been visited
                q.put(u)
                coming_from[u] = curr_user
        i += 1
        if i == 20:
            return []
    curr_user = user_2
    path.append(user_2)
    while(curr_user != None):
        if coming_from[curr_user] != None:
            path.append(coming_from[curr_user])
        curr_user = coming_from[curr_user]
    path.reverse()
    return path

def global_pokes_by_username(username):
    """
    Get global pokes by username
    :param username: Username
    :return: List of comments
    """
    query = create_global_pokes_by_username(username)
    result = session.run(query)
    final = []
    for item in result: #each item is a Comment Object
        final.append(item[0]['comment'])
    return final

def get_follows_posts(all_follows):
    """
    Gets posts based on who you follow
    :param all_follows: List of usernames
    :return: Dict mapping uname to posts
    """
    result = {}
    for user in all_follows:
        #get global pokes made by user
        curr_user_posts = global_pokes_by_username(user)
        result[user] = curr_user_posts
    return result

def insert_response(parent_id, response_owner, response_text):
    query = create_insert_respone(parent_id, response_owner, response_text)
    result = session.run(query)

def get_all_usernames():
    query = create_get_all_usernames()
    result = session.run(query)
    final = []
    for r in result:
        final.append(r[0]['user_name'])
    return final

def autocomplete_username(prefix):
    usernames = get_all_usernames()
    pre_tree = PrefixTree()
    pre_tree.build_prefix_tree(usernames)
    result = pre_tree.get_all_possible_words(prefix)
    return result

def get_all_group_names(username):
    query = create_get_all_group_names(username)
    result = session.run(query)
    final = {}
    for g in result:
        g_name = g[0]['group_name']
        final[g_name] = []
    return final

def get_per_group_info(group_name):
    query = create_get_per_group_info(group_name)
    result = session.run(query)
    final = []
    for c in result:
        final.append(tuple((c[0]['owner'], c[0]['comment'])))
    return final

def get_all_groups_information(username):
    group_data = get_all_group_names(username)
    for k,v in group_data.iteritems():
        group_data[k] = get_per_group_info(k)
    return group_data

def handle_create_group(username, group_name):
    query = create_handle_create_group(username, group_name)
    session.run(query)

def handle_join_group(username, group_name):
    query = create_handle_join_group(group_name, username)
    session.run(query)

def handle_insert_group_comment(username, group_name, comment):
    query = create_handle_insert_group_comment(username, group_name, comment)
    session.run(query)

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
        all_follows = get_all_follows(username)
        follows_posts = get_follows_posts(all_follows)
        follow_recos = get_follow_recomendations(username)
        return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=None)
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
        get_follow_recomendations(username)
        all_follows = get_all_follows(username)
        follow_recos = get_follow_recomendations(username)
        follows_posts = get_follows_posts(all_follows)
        return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=None)
    else:
        if split[len(split) - 1] == 'my_pokes':
            return render_template('my_pokes.html', user=curr_user, comments=comments)
        elif split[len(split) - 1] == 'global_pokes':
            comments = get_all_globalpokes()
            return render_template('global_pokes.html', user=curr_user, comments=comments)
        elif split[len(split) - 1] == username or split[len(split) - 1] == 'home':
            all_follows = get_all_follows(username)
            follow_recos = get_follow_recomendations(username)
            follows_posts = get_follows_posts(all_follows)
            return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=None)
        elif split[len(split) - 1] == 'groups':
            group_info = get_all_groups_information(username)
            return render_template('groups.html', user=curr_user, group_info=group_info)
        elif split[len(split) - 1] == 'friends_pokes':
            comments = get_all_friendspokes(username)
            return render_template('friends_pokes.html', user=curr_user, comments=comments)
        elif split[len(split) - 1] == '':
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
        query = get_create_user_account(user_name, first_name, last_name, email_id, password)
        insert_into_graphdb(query)
        curr_user = Person(first_name, last_name, user_name, email_id)
        all_follows = get_all_follows(user_name)
        follow_recos = get_follow_recomendations(user_name)
        follows_posts = get_follows_posts(all_follows)
        return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=None)
    else:
        return render_template('invalid_login_signup.html')

@app.route("/<path:comment_owner>/my_pokes", methods=['POST'])
def add_comment_mypoke(comment_owner):
    """
    Handles POST sign up
    :return: Renders Template
    """
    users = request.form['names']
    comment = request.form['comment']
    handle_comment(users, comment, comment_owner)
    comments = get_all_mypokes(comment_owner)
    curr_user = get_user(comment_owner)
    all_follows = get_all_follows(comment_owner)
    return render_template('my_pokes.html', user=curr_user, comments=comments, follows=all_follows)

@app.route("/<path:comment_owner>/global_pokes", methods=['POST'])
def add_comment_globalpoke(comment_owner):
    """
    Handles POST sign up
    :return: Renders Template
    """
    users = request.form['names']
    comment = request.form['comment']
    handle_comment(users, comment, comment_owner)
    comments = get_all_globalpokes()
    curr_user = get_user(comment_owner)
    return render_template('global_pokes.html', user=curr_user, comments=comments)

@app.route("/<path:comment_owner>/friends_pokes", methods=['POST'])
def add_comment_friendspoke(comment_owner):
    """
    Handles POST sign up
    :return: Renders Template
    """
    users = request.form['names']
    comment = request.form['comment']
    handle_comment(users, comment, comment_owner)
    comments = get_all_friendspokes(comment_owner)
    curr_user = get_user(comment_owner)
    return render_template('friends_pokes.html', user=curr_user, comments=comments)

@app.route("/<path:comment_owner>/home", methods=['POST'])
def add_comment_homepoke(comment_owner):
    """
    Handles POST sign up
    :return: Renders Template
    """
    print("BADD")
    users = request.form['names']
    comment = request.form['comment']
    handle_comment(users, comment, comment_owner)
    comments = get_all_mypokes(comment_owner)
    curr_user = get_user(comment_owner)
    all_follows = get_all_follows(comment_owner)
    follow_recos = get_follow_recomendations(comment_owner)
    follows_posts = get_follows_posts(all_follows)
    return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path =[], possible_words=None)

@app.route("/add_follows", methods=['POST'])
def add_follows_homepoke():
    """
    Handles POST sign up
    :return: Renders Template
    """
    friend_name = request.form['f_name']
    curr_user_name = request.form['username']
    create_follows_relation(curr_user_name, friend_name)
    curr_user = get_user(curr_user_name)
    all_follows = get_all_follows(curr_user_name)
    follow_recos = get_follow_recomendations(curr_user_name)
    follows_posts = get_follows_posts(all_follows)
    return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=None)


@app.route("/shortest_path", methods=['POST'])
def handle_shortest_path():
    """
    Handles POST sign up
    :return: Renders Template
    """
    friend_name = request.form['f_name']
    curr_user_name = request.form['username']
    path = shortest_path(curr_user_name, friend_name)
    curr_user = get_user(curr_user_name)
    all_follows = get_all_follows(curr_user_name)
    follow_recos = get_follow_recomendations(curr_user_name)
    follows_posts = get_follows_posts(all_follows)
    return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=path, possible_words=None)

@app.route("/add_response", methods=['POST'])
def add_comment_globalresponse():
    """
    Handles POST sign up
    :return: Renders Template
    """
    parent_id = int(request.form['parent_id'])
    comment_owner = request.form['comment_owner']
    response_owner = request.form['response_owner']
    response_text = request.form['response']
    insert_response(parent_id, response_owner, response_text)
    comments = get_all_globalpokes()
    curr_user = get_user(response_owner)
    return render_template('global_pokes.html', user=curr_user, comments=comments)

@app.route("/search_username", methods=['POST'])
def handle_search_username():
    """
    Handles POST sign up
    :return: Renders Template
    """
    prefix = request.form['prefix']
    curr_user_name = request.form['username']
    curr_user = get_user(curr_user_name)
    all_follows = get_all_follows(curr_user_name)
    follow_recos = get_follow_recomendations(curr_user_name)
    follows_posts = get_follows_posts(all_follows)
    possible_words = autocomplete_username(prefix)
    return render_template('user_home.html', user=curr_user, follows=follows_posts, follow_recos=follow_recos, path=[], possible_words=possible_words)

@app.route("/create_group", methods=['POST'])
def create_group():
    username = request.form['username']
    group_name = request.form['group_name']
    handle_create_group(username, group_name)
    curr_user = get_user(username)
    group_info = get_all_groups_information(username)
    return render_template('groups.html', user=curr_user, group_info=group_info) 

@app.route("/join_group", methods=['POST'])
def join_group():
    username = request.form['username']
    group_name = request.form['group_name']
    handle_join_group(username, group_name)
    curr_user = get_user(username)
    group_info = get_all_groups_information(username)
    return render_template('groups.html', user=curr_user, group_info=group_info) 

@app.route("/create_group_comment", methods=['POST'])
def create_group_comment():
    username = request.form['username']
    group_name = request.form['group_name']
    comment = request.form['group_message']
    handle_insert_group_comment(username, group_name, comment)
    curr_user = get_user(username)
    group_info = get_all_groups_information(username)
    return render_template('groups.html', user=curr_user, group_info=group_info)

if __name__ == "__main__":
    app.run(debug=True)
