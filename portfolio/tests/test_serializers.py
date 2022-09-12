from django.contrib.auth.models import User
from django.test import TestCase

from portfolio.models import Design
from portfolio.serializers import DesignsSerializer


class DesignSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username='test_username')
        design_1 = Design.objects.create(Design_title='Test Design 1',
                                         square=25,
                                         author_name='Author 1',
                                         owner=self.user)
        design_2 = Design.objects.create(Design_title='Test Design 2',
                                         square=55,
                                         author_name='Author 2',
                                         owner=self.user)
        data = DesignsSerializer([design_1, design_2], many=True).data
        expected_data = [
            {
                'id': design_1.id,
                'Design_title': 'Test Design 1',
                'square':  '25',
                'author_name': 'Author 1',
                'owner': design_1.owner.id
            },
            {
                'id': design_2.id,
                'Design_title': 'Test Design 2',
                'square': '55',
                'author_name': 'Author 2',
                'owner': design_2.owner.id
            },
        ]
        self.assertEqual(expected_data, data)