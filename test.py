from unittest import TestCase
from app import app
from flask import session
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True

db.drop_all()
db. create_all()

class FlaskTests(TestCase):
    
    def setUp(self):
        """create test user"""
        User.query.delete()
        user = {'first_name': 'James',
                        'last_name':'Madison',
                        'image_url':'https://science.nasa.gov/wp-content/uploads/2023/05/sun-cartoon-crop.png?w=4096&format=png&crop=1'}
        db.session.add(user)
        db.session.commit()

    def tearDown(self):

        db.session.rollback()   

    def test_home(self):
        """testing home route redirect"""
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 302)
           
    def test_show_users(self):
        """testing html for show_users"""
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Users</h1>',html)

    def test_create_new_user(self):
        """testing post route for creating new user"""
        with app.test_client() as client:
            new_user = {'first_name': 'test_first_name',
                        'last_name':'test_last_name',
                        'image_url':'https://science.nasa.gov/wp-content/uploads/2023/05/sun-cartoon-crop.png?w=4096&format=png&crop=1'}
            res = client.post('/users/new',data=new_user,follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('test_first_name test_last_name',html)        
   