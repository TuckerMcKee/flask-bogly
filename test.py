from unittest import TestCase
from app import app
from flask import session
from sqlalchemy import text
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True

# db.drop_all()
# db.create_all()

class FlaskTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        """create test user"""
        self.app_context = app.app_context() 
        self.app_context.push()
        User.query.delete()
        db.session.execute(text('ALTER SEQUENCE users_id_seq RESTART WITH 1'))
        user = User(first_name='James', last_name='Madison',
                    image_url='https://science.nasa.gov/wp-content/uploads/2023/05/sun-cartoon-crop.png?w=4096&format=png&crop=1')
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

    def test_update_user_data(self):
        """testing post route for editing user data"""
        with app.test_client() as client:
            edit_user = {'first_name': 'test_edit_first_name',
                         'last_name': '',
                         'image_url': ''}
            res = client.post('/users/1/edit',data=edit_user,follow_redirects=True)
            user = db.session.get(User, 1)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(user.first_name,'test_edit_first_name')                 
   