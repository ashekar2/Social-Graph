"""
Class that deals with creating all queries to interact with the graphDB
"""

def create_personal_poke(comment_owner, comment):
	"""
    Function to create query for personal poke insertion
    :param comment_owner: Comment Owner
    :param comment: Actual Comment
    :return: Query
    """
	query = "MATCH (ee:Person) WHERE ee.user_name = '%s' CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (ee)-[:OWNS_COMMENT]->(c)" % (comment_owner, comment, comment_owner)
	return query

def create_global_poke(comment_owner, comment):
	"""
    Function to create query for global poke insertion
    :param comment_owner: Comment Owner
    :param comment: Actual Comment
    :return: Query
    """
	query = "MATCH (ee:Person) WHERE ee.user_name = '%s' MATCH (global_node:GlobalComment) WHERE global_node.user_name = 'global_comment' CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (ee)-[:OWNS_COMMENT]->(c) CREATE (global_node)-[:GLOBAL_POST]->(c)" % (comment_owner, comment, comment_owner)
	return query

def create_friends_poke(comment_owner, user_list, comment):
	"""
    Function to create query for friends poke insertion
    :param comment_owner: Comment Owner
    :param comment: Actual Comment
    :param user_list: List of users
    :return: Query
    """
	query = "MATCH (ee:Person) WHERE ee.user_name = '%s'" % comment_owner
	for i in range(len(user_list)):
		curr_user_q = "MATCH (f%d:Person) WHERE f%d.user_name = '%s' " %(i, i, user_list[i])
		query += ' ' + curr_user_q
	query += ' ' +  "CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (ee)-[:OWNS_COMMENT]->(c)" % (comment, comment_owner)
	for i in range(len(user_list)):
		curr_user_q = "CREATE (f%d)-[:SHARED_COMMENT]->(c) " %(i)
		query += ' ' + curr_user_q
	return query


def create_combo_poke(comment_owner, user_list, comment):
	"""
    Function to create query for friends+global poke insertion
    :param comment_owner: Comment Owner
    :param comment: Actual Comment
    :param user_list: List of users
    :return: Query
    """
	query = "MATCH (ee:Person) WHERE ee.user_name = '%s' MATCH (global_node:GlobalComment) WHERE global_node.user_name = 'global_comment' " % comment_owner
	for i in range(len(user_list)):
		curr_user_q = "MATCH (f%d:Person) WHERE f%d.user_name = '%s' " %(i, i, user_list[i])
		query += ' ' + curr_user_q

	query += ' ' +  "CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (ee)-[:OWNS_COMMENT]->(c) CREATE (global_node)-[:GLOBAL_POST]->(c)" % (comment, comment_owner)
	for i in range(len(user_list)):
		curr_user_q = "CREATE (f%d)-[:SHARED_COMMENT]->(c) " %(i)
		query += ' ' + curr_user_q
	print(query)
	return query

def create_get_global_pokes():
	"""
    Function to get all global pokes query
    :return: Query
    """
    # MATCH (n:Person) RETURN { id: ID(n), name: n.name } as user
	query = "MATCH (ee:GlobalComment)-[:GLOBAL_POST]-(comments) RETURN { id: ID(comments), comment_data: comments } as c"
	return query

def create_get_responses(parent_id):
    query = "MATCH (parent:Comment)-[:REPLY]-(r:Comment) WHERE ID(parent) = %d RETURN r" % parent_id
    return query

def create_insert_respone(parent_id, reply_owner, reply_text):
    query = "MATCH (parent:Comment) WHERE ID(parent) = %d CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (parent)-[:REPLY]->(c)" % (parent_id, reply_text, reply_owner)
    return query

def create_get_mypokes(username):
    """
    Function to get persol pokes for user
    :param username: User name
    :return: Query
    """
    query = "MATCH (ee:Person)-[:OWNS_COMMENT]-(comments) WHERE ee.user_name='%s' RETURN comments" % (username)
    return query

def create_validate_login(username):
	"""
    Function to validate user login query
    :param username: User name
    :return: Query
    """
	query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username, a.password AS retr_password" % username
	return query

def create_check_unique_username(username):
	"""
    Function to check unique username query
    :param username: User name
    :return: Query
    """
	query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username" % username
	return query

def get_create_user(username):
	"""
    Function to create user username
    :param username: User name
    :return: Query
    """
	query = "MATCH (a:Person) WHERE a.user_name = '%s' RETURN a.user_name AS retr_username, a.password AS retr_password, a.first_name AS retr_first_name, a.last_name AS retr_last_name, a.email_id AS retr_email_id" % username
	return query

def get_create_user_account(user_name, first_name, last_name, email_id, password):
	"""
    Function to create sign up user
    :param user_name: Username
    :param first_name: First name
    :param last_name: Last name
    :param email_id: Email ID
    :param password: Password
    :return: Query
    """
	query = "CREATE (a:Person {user_name: '%s', first_name: '%s' , last_name: '%s' , email_id: '%s' , password: '%s' })" % (user_name, first_name, last_name, email_id, password)
	return query

def create_get_friendspokes(username):
    """
    Function to create query for getting friends pokes
    :param username: Username
    :return: Query
    """
    query = "MATCH (ee:Person)-[:SHARED_COMMENT]-(comments) WHERE ee.user_name='%s' RETURN comments" % (username)
    return query

def create_add_follow(username, f_username):
    """
    Function to create query for getting friends pokes
    :param username: Username
    :return: Query
    """
    query = "MATCH (u:Person) WHERE u.user_name='%s' MATCH (f:Person) WHERE f.user_name='%s' CREATE (u)-[:FOLLOWS]->(f) " % (username, f_username)
    return query

def create_get_follows(username):
    """
    Function to create query for following a person
    :param username: Username
    :return: Query
    """
    query = "MATCH (ee:Person)-[:FOLLOWS]-(f) WHERE ee.user_name='%s' RETURN f" % (username)
    return query

def create_global_pokes_by_username(username):
    """
    Create query for global posts by username
    :return: Renders Template
    """
    query = "MATCH (ee:GlobalComment)-[:GLOBAL_POST]-(comments) WHERE comments.owner ='%s' RETURN comments LIMIT 2" % (username)
    return query

def create_get_all_usernames():
    """
    Create query for global posts by username
    :return: Renders Template
    """
    query = "MATCH (e:Person) WHERE EXISTS(e.user_name) RETURN e"
    return query

def create_handle_create_group(username, group_name):
    """
    Create query for creating group
    :return: query
    """
    query = "MATCH (e:Person) WHERE e.user_name = '%s' CREATE (g:Group {group_name: '%s'}) CREATE (e)-[:IN_GROUP]->(g)" % (username, group_name)
    return query

def create_get_all_group_names(username):
    """
    Create query for group names
    :return: query
    """
    query = "MATCH (e:Person)-[:IN_GROUP]->(g:Group) WHERE e.user_name = '%s' RETURN g" % username
    return query

def create_get_per_group_info(group_name):
    """
    Create query for group info
    :return: query
    """
    query = "MATCH (g:Group)-[:GROUP_COMMENT]->(c:Comment) WHERE g.group_name = '%s' RETURN c" % group_name
    return query

def create_handle_join_group(group_name, username):
    """
    Create query for joining group
    :return: query
    """
    query = "MATCH (g:Group) WHERE g.group_name = '%s' MATCH (e:Person) WHERE e.user_name = '%s' CREATE (e)-[:IN_GROUP]->(g)" % (group_name, username)
    return query

def create_handle_insert_group_comment(username, group_name, comment):
    """
    Create query for creating group comment
    :return: query
    """
    query = "MATCH (e:Person) WHERE e.user_name = '%s' MATCH (g:Group) WHERE g.group_name = '%s' CREATE (c:Comment {comment: '%s', owner: '%s'}) CREATE (g)-[:GROUP_COMMENT]->(c)" % (username, group_name, comment, username)
    return query

