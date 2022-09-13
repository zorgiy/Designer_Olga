from django.contrib.auth.models import User
from django.test import TestCase

from portfolio.logic import set_rating
from portfolio.models import Design, UserDesignRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='Petr', last_name='Ivanov')
        user2 = User.objects.create(username='user2', first_name='Inna', last_name='Volkova')
        user3 = User.objects.create(username='user3', first_name='Pavel', last_name='Gagarin')
        self.design_1 = Design.objects.create(Design_title='Test Design 1',
                                              square=25,
                                              author_name='Author 1',
                                              owner=user1)
        UserDesignRelation.objects.create(user=user1, design=self.design_1, like=True, rate=5)
        UserDesignRelation.objects.create(user=user2, design=self.design_1, like=True, rate=5)
        UserDesignRelation.objects.create(user=user3, design=self.design_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.design_1)
        self.design_1.refresh_from_db()
        self.assertEqual('4.67', str(self.design_1.rating))
