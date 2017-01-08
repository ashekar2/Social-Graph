import unittest
from create_query import *

class TestPassword(unittest.TestCase):
    def test_create_personal_poke(self):
        query = create_personal_poke('j', 'test')
        answer = "MATCH (ee:Person) WHERE ee.user_name = 'j' CREATE (c:Comment {comment: 'test', owner: 'j'}) CREATE (ee)-[:OWNS_COMMENT]->(c)"
        self.assertEqual(query, answer)

    def test_create_global_poke(self):
        query = create_global_poke('j', 'test')
        answer = "MATCH (ee:Person) WHERE ee.user_name = 'j' MATCH (global_node:GlobalComment) WHERE global_node.user_name = 'global_comment' CREATE (c:Comment {comment: 'test', owner: 'j'}) CREATE (ee)-[:OWNS_COMMENT]->(c) CREATE (global_node)-[:GLOBAL_POST]->(c)"
        self.assertEqual(query, answer)

    def test_create_friends_poke(self):
        query = create_friends_poke('j', ['user1', 'user2'], 'test')
        answer = "MATCH (ee:Person) WHERE ee.user_name = 'j' MATCH (f0:Person) WHERE f0.user_name = 'user1'  MATCH (f1:Person) WHERE f1.user_name = 'user2'  CREATE (c:Comment {comment: 'test', owner: 'j'}) CREATE (ee)-[:OWNS_COMMENT]->(c) CREATE (f0)-[:SHARED_COMMENT]->(c)  CREATE (f1)-[:SHARED_COMMENT]->(c) "
        self.assertEqual(query, answer)

    def test_create_combo_poke(self):
        query = create_combo_poke('j', ['user1', 'user2'], 'test')
        answer = "MATCH (ee:Person) WHERE ee.user_name = 'j' MATCH (global_node:GlobalComment) WHERE global_node.user_name = 'global_comment'  MATCH (f0:Person) WHERE f0.user_name = 'user1'  MATCH (f1:Person) WHERE f1.user_name = 'user2'  CREATE (c:Comment {comment: 'test', owner: 'j'}) CREATE (ee)-[:OWNS_COMMENT]->(c) CREATE (global_node)-[:GLOBAL_POST]->(c) CREATE (f0)-[:SHARED_COMMENT]->(c)  CREATE (f1)-[:SHARED_COMMENT]->(c) "
        self.assertEqual(query, answer)

    def test_get_create_user_account(self):
        query = get_create_user_account('u1', 'f1', 'l1', 'e1', 'p1')
        answer = "CREATE (a:Person {user_name: 'u1', first_name: 'f1' , last_name: 'l1' , email_id: 'e1' , password: 'p1' })"
        self.assertEqual(query, answer)

    def test_create_get_friendspokes(self):
        query = create_get_friendspokes('j')
        answer = "MATCH (ee:Person)-[:SHARED_COMMENT]-(comments) WHERE ee.user_name='j' RETURN comments"
        self.assertEqual(query, answer)

    def test_create_add_follow(self):
        query = create_add_follow('j', 'k')
        answer = "MATCH (u:Person) WHERE u.user_name='j' MATCH (f:Person) WHERE f.user_name='k' CREATE (u)-[:FOLLOWS]->(f) "
        self.assertEqual(query, answer)

    def test_create_global_pokes_by_username(self):
        query = create_global_pokes_by_username('j')
        answer = "MATCH (ee:GlobalComment)-[:GLOBAL_POST]-(comments) WHERE comments.owner ='j' RETURN comments LIMIT 2"
        self.assertEqual(query, answer)

    def test_create_handle_create_group(self):
        query = create_handle_create_group('j', 'a', 'as')
        answer = "MATCH (e:Person) WHERE e.user_name = 'j' CREATE (g:Group {group_name: 'a', group_password: 'as'}) CREATE (e)-[:IN_GROUP]->(g)"
        self.assertEqual(query, answer)

    def test_create_get_all_group_names(self):
        query = create_get_all_group_names('j')
        answer = "MATCH (e:Person)-[:IN_GROUP]->(g:Group) WHERE e.user_name = 'j' RETURN g"
        self.assertEqual(query, answer)

    def test_create_get_per_group_info(self):
        query = create_get_per_group_info('j')
        answer = "MATCH (g:Group)-[:GROUP_COMMENT]->(c:Comment) WHERE g.group_name = 'j' RETURN c"
        self.assertEqual(query, answer)

    def test_create_handle_join_group(self):
        query = create_handle_join_group('j', 'ajay')
        answer = "MATCH (g:Group) WHERE g.group_name = 'j' MATCH (e:Person) WHERE e.user_name = 'ajay' CREATE (e)-[:IN_GROUP]->(g)"
        self.assertEqual(query, answer)

    def test_create_handle_insert_group_comment(self):
        query = create_handle_insert_group_comment('j', 'ajay', 'paj')
        answer = "MATCH (e:Person) WHERE e.user_name = 'j' MATCH (g:Group) WHERE g.group_name = 'ajay' CREATE (c:Comment {comment: 'paj', owner: 'j'}) CREATE (g)-[:GROUP_COMMENT]->(c)"
        self.assertEqual(query, answer)



if __name__ == '__main__':
    unittest.main()