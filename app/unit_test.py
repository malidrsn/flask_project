import unittest
from .views.home import make_a_request


class TestUnit(unittest.TestCase):
    def test_request(self) -> None:
        """Test for app.

        this function written for the testing. it calls make_request methods
        to check is the answer is right or not. after the testing if the result is 1 it means
        passed the test as successfully

        """
        self.assertEqual(make_a_request("example"),
                         "Something Gone Wrong, Try Again")
        self.assertEqual(make_a_request(123456),
                         "Something Gone Wrong, Try Again")
        self.assertEqual(make_a_request(
            [123456]), "Something Gone Wrong, Try Again")
        self.assertEqual(make_a_request(
            "  "), "Something Gone Wrong, Try Again")
        self.assertEqual(make_a_request("abcde"),
                         "Something Gone Wrong, Try Again")
        self.assertEqual(make_a_request("Mосква"),
                         "The Address that you entered is in MKAD-area")
        self.assertEqual(make_a_request(
            "istanbul"), "The Address that you entered is 1500.524km away from MKAD")


if __name__ == "__main__":
    unittest.main()
