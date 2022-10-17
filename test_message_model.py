import os
from unittest import TestCase
from models import db, Message, User, Likes
from app import app

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()

class MessageModelTestCase(TestCase):
    '''Test views for messages.'''

    def setup(self):
        '''create test client, add sample data.'''

        db.drop_all()
        db.create_all()

        user1 = User.signup("testUser1", "testEmail@test.com", "HASHED_PASSWORD", None)
        uid1 = 1
        user1.id = uid1

        message1 = Message(text='message1', user_id=user1.id)

        db.session.add_all(user1, message1)
        db.session.commit()

        self.user1 = user1
        self.uid1= uid1
        self.message1 = message1

        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        '''Does message model work?'''

        mess= Message(text='test message', user_id=1)

        db.session.add(mess)
        db.session.commit()

        self.assertEqual(mess.text, 'test message')
        self.assertEqual(mess.user_id, 1)

    def test_likes(self):
        m1 = Message(text= 'test message 1', user_id=self.uid1)

        m2 = Message(text='test message2', user_id=self.uid1)

        u = User.signup('testuser2', 'test2@gmail.com', 'HASHED_PW', None)
        uid=342
        u.id= uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()

        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)