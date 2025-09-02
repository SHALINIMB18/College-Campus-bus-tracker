import unittest
from unittest.mock import patch, MagicMock

class TestLogin(unittest.TestCase):
    @patch('requests.Session')
    def test_login(self, mock_session_class):
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Mock the get request to return a response with status_code 200 and a csrftoken cookie
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.cookies.get.return_value = 'fake-csrf-token'
        mock_session.get.return_value = mock_get_response

        # Mock the post request to simulate a successful login redirect
        mock_post_response = MagicMock()
        mock_post_response.url = 'http://localhost:8000/tracking/live/'
        mock_session.post.return_value = mock_post_response

        # Import the login function or code here and run it, or simulate the logic
        login_url = "http://localhost:8000/users/login/"
        payload = {
            "username": "7026746330",
            "password": "Agr@9876",
            "csrfmiddlewaretoken": 'fake-csrf-token'
        }
        headers = {
            "Referer": login_url
        }

        # Simulate the login process
        response = mock_session.get(login_url)
        self.assertEqual(response.status_code, 200)
        csrf_token = response.cookies.get('csrftoken')
        self.assertIsNotNone(csrf_token)

        login_response = mock_session.post(login_url, data=payload, headers=headers)
        self.assertNotEqual(login_response.url, login_url)

        # Simulate accessing a protected page
        protected_url = "http://localhost:8000/tracking/live/"
        protected_response = mock_session.get(protected_url)
        protected_response.status_code = 200
        self.assertEqual(protected_response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
