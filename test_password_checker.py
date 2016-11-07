import unittest
from password_checker import *

class TestPassword(unittest.TestCase):

    def test_invalid_pass_1(self):
        valid = password_check("abcd")
        self.assertEqual(valid, False)

    def test_invalid_pass2(self):
        valid = password_check("Hello Abcd $123")
        self.assertEqual(valid, False)

    def test_invalid_pass3(self):
        valid = password_check("12345678")
        self.assertEqual(valid, False)

    def test_invalid_pass4(self):
        valid = password_check("notavalidpass123#")
        self.assertEqual(valid, False)

    def test_valid_pass1(self):
        valid = password_check("ValidPass123$")
        self.assertEqual(valid, True)

    def test_valid_pass2(self):
        valid = password_check("1234$Valid")
        self.assertEqual(valid, True)

    def test_valid_pass3(self):
        valid = password_check("validpass12W#")
        self.assertEqual(valid, True)

    def test_invalid_username(self):
        valid = username_check("Not a Valid")
        self.assertEqual(valid, False)

    def test_valid_username(self):
        valid = username_check("thisisvalid")
        self.assertEqual(valid, True)

if __name__ == '__main__':
    unittest.main()