from datetime import datetime, timedelta
import unittest
from app import app, db, plots
from app.models import User, Streak, PostDB

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_streak_plotting(self):
        u1 = User(username="joe")
        u2 = User(username="billy")
        s1 = Streak(total_count=1, user=u1, old_user=u1.username)
        s2 = Streak(total_count=2, user=u2, old_user=u2.username)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        png_image = plots.create_streak_plt(Streak.query.all())
        self.assertEqual(str, type(png_image))

        n_s1 = Streak(total_count=1, user=u1, old_user=u1.username)
        n_s2 = Streak(total_count=2, user=u2, old_user=u2.username)
        n_png_image = plots.create_streak_plt([n_s1, n_s2])
        self.assertEqual(png_image, n_png_image)

    def test_password_hashing(self):
        u = User(username="roger")
        u.set_password('dog')
        self.assertTrue(u.check_password('dog'))
        self.assertFalse(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='roger')
        self.assertEqual(u.avatar(128),
                         'https://www.gravatar.com/avatar/b911af807c2df88d671bd7004c54c1c2?d=retro&s=128')


if __name__ == '__main__':
    unittest.main(verbosity=2)
