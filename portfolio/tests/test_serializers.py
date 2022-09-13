from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from portfolio.models import Design, UserDesignRelation
from portfolio.serializers import DesignsSerializer


class DesignSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Petr', last_name='Ivanov')
        user2 = User.objects.create(username='user2', first_name='Inna', last_name='Volkova')
        user3 = User.objects.create(username='user3', first_name='Pavel', last_name='Gagarin')
        design_1 = Design.objects.create(Design_title='Test Design 1',
                                         square=25,
                                         author_name='Author 1',
                                         owner=user1)
        design_2 = Design.objects.create(Design_title='Test Design 2',
                                         square=55,
                                         author_name='Author 2')
        UserDesignRelation.objects.create(user=user1, design=design_1, like=True, rate=5)
        UserDesignRelation.objects.create(user=user2, design=design_1, like=True, rate=5)
        user_design_3 = UserDesignRelation.objects.create(user=user3, design=design_1, like=True)
        user_design_3.rate = 4
        user_design_3.save()

        UserDesignRelation.objects.create(user=user1, design=design_2, like=True, rate=3)
        UserDesignRelation.objects.create(user=user2, design=design_2, like=True, rate=4)
        UserDesignRelation.objects.create(user=user3, design=design_2, like=False)

        designs = Design.objects.all().annotate(
            annotated_likes=Count(Case(When(userdesignrelation__like=True, then=1)))
        ).order_by('id')
        data = DesignsSerializer(designs, many=True).data
        expected_data = [
            {
                'id': design_1.id,
                'Design_title': 'Test Design 1',
                'square': '25',
                'author_name': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user1',
                'vieweds': [
                    {
                        'first_name': 'Petr',
                        'last_name': 'Ivanov'
                    },
                    {
                        'first_name': 'Inna',
                        'last_name': 'Volkova'
                    },
                    {
                        'first_name': 'Pavel',
                        'last_name': 'Gagarin'
                    }
                ]
            },
            {
                'id': design_2.id,
                'Design_title': 'Test Design 2',
                'square': '55',
                'author_name': 'Author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'vieweds': [
                    {
                        'first_name': 'Petr',
                        'last_name': 'Ivanov'
                    },
                    {
                        'first_name': 'Inna',
                        'last_name': 'Volkova'
                    },
                    {
                        'first_name': 'Pavel',
                        'last_name': 'Gagarin'
                    }
                ]
            },
        ]
        print('expected_data:', expected_data)
        print('data:', data)
        self.assertEqual(expected_data, data)
