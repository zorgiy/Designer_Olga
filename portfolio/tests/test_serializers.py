from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from portfolio.models import Design, UserDesignRelation
from portfolio.serializers import DesignsSerializer


class DesignSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        design_1 = Design.objects.create(Design_title='Test Design 1',
                                         square=25,
                                         author_name='Author 1',
                                         owner=user1)
        design_2 = Design.objects.create(Design_title='Test Design 2',
                                         square=55,
                                         author_name='Author 2',
                                         owner=user2)
        UserDesignRelation.objects.create(user=user1, design=design_1, like=True, rate=5)
        UserDesignRelation.objects.create(user=user2, design=design_1, like=True, rate=5)
        UserDesignRelation.objects.create(user=user3, design=design_1, like=True, rate=4)

        UserDesignRelation.objects.create(user=user1, design=design_2, like=True, rate=3)
        UserDesignRelation.objects.create(user=user2, design=design_2, like=True, rate=4)
        UserDesignRelation.objects.create(user=user3, design=design_2, like=False)

        designs = Design.objects.all().annotate(
            annotated_likes=Count(Case(When(userdesignrelation__like=True, then=1))),
            rating=Avg('userdesignrelation__rate')
        ).order_by('id')
        data = DesignsSerializer(designs, many=True).data
        expected_data = [
            {
                'id': design_1.id,
                'Design_title': 'Test Design 1',
                'square':  '25',
                'author_name': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67'
            },
            {
                'id': design_2.id,
                'Design_title': 'Test Design 2',
                'square': '55',
                'author_name': 'Author 2',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50'
            },
        ]
        self.assertEqual(expected_data, data)