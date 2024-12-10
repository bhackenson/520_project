import unittest
import json
import os
import secrets
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # test client
        self.client = app.test_client()
        
        # ensure test database is clean
        if os.path.exists('db.json'):
            os.remove('db.json')
        
        # initialize test database
        with open('db.json', 'w') as file:
            json.dump({}, file)

        # initialize feedback database
        if os.path.exists('feedback.json'):
            os.remove('feedback.json')
        
        with open('feedback.json', 'w') as file:
            json.dump({"feedback": []}, file)

    # helper method to create a test user
    def _create_test_user(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/api/create_user', json=user_data)
        response_data = json.loads(response.data)
        return response_data


    # helper method to login test user
    def _login_test_user(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/api/login', json=login_data)
        return json.loads(response.data)

    # test user registration
    def test_user_registration(self):
        response = self.client.post('/api/create_user', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('userid', data)
        self.assertEqual(data['username'], 'testuser')

    # test user registration with duplicate fields (should throw an error)
    def test_user_reg_missing_fields(self):
        response1 = self.client.post('/api/create_user', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.post('/api/create_user', json={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response2.status_code, 404)
        self.assertIn('error', json.loads(response2.data))
        self.assertEqual(json.loads(response2.data)['error'], 'username already exists.')

    # test login
    def test_user_login(self):
        self._create_test_user()

        response = self.client.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('userid', data)

    # test project creation
    def test_create_project(self):
        user_data = self._create_test_user()
        userid = user_data['userid']

        response = self.client.post('/api/create_project', json={
            'userid': userid,
            'name': 'Test Project',
            'date': '2024-12-09'
        })
        
        print("Create Project Response:", response.data)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('project', data)
        self.assertEqual(data['project']['name'], 'Test Project')
        #project_id = data['project']['id']

    # test progression generation
    def test_generate_progression(self):
        user_data = self._create_test_user()
        userid = user_data['userid']

        project_response = self.client.post('/api/create_project', json={
            'userid': userid,
            'name': 'Test Project',
            'date': '2024-01-01'
        })
        project_data = json.loads(project_response.data)
        projid = project_data['project']['id']

        response = self.client.post('/api/create_progression', json={
            'userid': userid,
            'projid': projid,
            'name': 'Test Progression',
            'key_signature': 'C',
            'mode': 'major',
            'time_signature': '4/4',
            'tempo': 120
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('progression', data)
        self.assertEqual(data['progression']['name'], 'Test Progression')

    # test progression update
    def test_update_progression(self):
        user_data = self._create_test_user()
        userid = user_data['userid']

        project_response = self.client.post('/api/create_project', json={
            'userid': userid,
            'name': 'Test Project',
            'date': '2024-01-01'
        })
        project_data = json.loads(project_response.data)
        projid = project_data['project']['id']

        prog_response = self.client.post('/api/create_progression', json={
            'userid': userid,
            'projid': projid,
            'name': 'Test Progression',
            'key_signature': 'C',
            'mode': 'major',
            'time_signature': '4/4',
            'tempo': 120
        })
        prog_data = json.loads(prog_response.data)
        progid = prog_data['progression']['id']

        update_response = self.client.put('/api/update_progression', json={
            'userid': userid,
            'projid': projid,
            'progid': progid,
            'name': 'Updated Progression',
            'key_signature': 'G',
            'mode': 'major',
            'time_signature': '3/4',
            'tempo': 100,
            'chords': [
                {"chord": "G major triad", "notes": ["G", "B", "D"]},
                {"chord": "C major triad", "notes": ["C", "E", "G"]}
            ],
            'melody': [
                ["G3", "B3", "D4"],
                ["C3", "E3", "G3"]
            ]
        })
        
        self.assertEqual(update_response.status_code, 200)
        update_data = json.loads(update_response.data)
        self.assertEqual(update_data['new_progression']['name'], 'Updated Progression')

    # test project deletion
    def test_delete_project(self):
        user_data = self._create_test_user()
        userid = user_data['userid']

        project_response = self.client.post('/api/create_project', json={
            'userid': userid,
            'name': 'Test Project',
            'date': '2024-01-01'
        })
        project_data = json.loads(project_response.data)
        projid = project_data['project']['id']

        response = self.client.put('/api/delete_project', json={
            'userid': userid,
            'projid': projid
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['projid'], projid)

    # test feedback submission
    def test_feedback_submission(self):
        response = self.client.post('/api/feedback', json={
            'progression1': {
                'chords': [
                    {"chord": "C major triad", "notes": ["C", "E", "G"]}
                ],
                'melody': [["C3", "E3", "G3"]]
            },
            'progression2': {
                'chords': [
                    {"chord": "A minor triad", "notes": ["A", "C", "E"]}
                ],
                'melody': [["A3", "C4", "E4"]]
            },
            'naturalness': 5,
            'accuracy': 5,
            'inspiration': 5,
            'comment': 'Test comment'
        })
        
        self.assertEqual(response.status_code, 200)
        with open('feedback.json', 'r') as file:
            feedback_data = json.load(file)
            self.assertTrue(len(feedback_data['feedback']) > 0)

if __name__ == '__main__':
    unittest.main()