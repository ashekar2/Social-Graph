import unittest
from neo4j.v1 import GraphDatabase, basic_auth
from main import *

driver = GraphDatabase.driver("bolt://localhost:7687/", auth=basic_auth("neo4j", "asdf"))
session = driver.session()

class TestDatabase(unittest.TestCase):

    def test_username_present1(self):
        valid = validate_login("j", "j")
        self.assertEqual(valid, True)

    def test_username_present2(self):
        valid = validate_login("Test", "TestUser123$")
        self.assertEqual(valid, True)

    def test_username_not_present(self):
        valid = validate_login("jack", "james")
        self.assertEqual(valid, False)

    def test_username_not_present(self):
        valid = validate_login("j", "wrong_pass")
        self.assertEqual(valid, False)

    def test_get_user(self):
    	curr_user = get_user("j")
    	self.assertEqual(curr_user.first_name, 'j')
    	self.assertEqual(curr_user.last_name, 'j')

   	def test_insert_into_db(self):
		query = "CREATE (a:Person {user_name: '%s', first_name: '%s' , last_name: '%s' , email_id: '%s' , password: '%s' })" % ('user_name', 'first_name', 'last_name', 'email_id', 'password')
	   	insert_into_graphdb(query)
	   	valid = validate_login("user_name", "password")



if __name__ == "__main__":
    app.run(debug=True)
