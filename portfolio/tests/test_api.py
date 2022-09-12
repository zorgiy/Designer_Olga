import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from portfolio.models import Design, UserDesignRelation
from portfolio.serializers import DesignsSerializer


class DesignsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.design_1 = Design.objects.create(Design_title='Design_1',
                                              square=25,
                                              author_name='Author_1',
                                              owner=self.user)
        self.design_2 = Design.objects.create(Design_title='Design_1',
                                              square=55,
                                              author_name='Author_2',
                                              owner=self.user)
        self.design_3 = Design.objects.create(Design_title='Design_3 Author_1',
                                              square=55,
                                              author_name='Author_3',
                                              owner=self.user)

    def test_get(self):
        url = reverse('design-list')
        response = self.client.get(url)
        serializer_data = DesignsSerializer([self.design_1, self.design_2, self.design_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('design-list')
        response = self.client.get(url, data={'square': 55})
        serializer_data = DesignsSerializer([self.design_2, self.design_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('design-list')
        response = self.client.get(url, data={'search': 'Author_1'})
        serializer_data = DesignsSerializer([self.design_1, self.design_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Design.objects.all().count())
        url = reverse('design-list')
        data = {
            "Design_title": "Design_6",
            "square": 55,
            "author_name": "Author_6"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Design.objects.all().count())
        self.assertEqual(self.user, Design.objects.last().owner)

    def test_update(self):
        url = reverse('design-detail', args=(self.design_1.id,))
        data = {
            "Design_title": self.design_1.Design_title,
            "square": 105,
            "author_name": self.design_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.design_1.refresh_from_db()
        self.assertEqual(105, self.design_1.square)

    def test_delete(self):
        self.assertEqual(3, Design.objects.all().count())
        url = reverse('design-detail', args=(self.design_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Design.objects.all().count())

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('design-detail', args=(self.design_1.id,))
        data = {
            "Design_title": self.design_1.Design_title,
            "square": 105,
            "author_name": self.design_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.design_1.refresh_from_db()
        self.assertEqual(25, self.design_1.square)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2',
                                         is_staff=True)
        url = reverse('design-detail', args=(self.design_1.id,))
        data = {
            "Design_title": self.design_1.Design_title,
            "square": 105,
            "author_name": self.design_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.design_1.refresh_from_db()
        self.assertEqual(105, self.design_1.square)


class DesignsRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.design_1 = Design.objects.create(Design_title='Design_1',
                                              square=25,
                                              author_name='Author_1',
                                              owner=self.user)
        self.design_2 = Design.objects.create(Design_title='Design_1',
                                              square=55,
                                              author_name='Author_2',
                                              owner=self.user)

    def test_like(self):
        url = reverse('userdesignrelation-detail', args=(self.design_1.id,))
        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserDesignRelation.objects.get(user=self.user, design=self.design_1)
        self.assertTrue(relation.like)
        data = {
            "in_bookmarks": True
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserDesignRelation.objects.get(user=self.user, design=self.design_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userdesignrelation-detail', args=(self.design_1.id,))
        data = {
            "rate": 3
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserDesignRelation.objects.get(user=self.user, design=self.design_1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse('userdesignrelation-detail', args=(self.design_1.id,))
        data = {
            "rate": 6
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
