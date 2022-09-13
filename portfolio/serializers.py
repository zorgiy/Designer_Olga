from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from portfolio.models import Design, UserDesignRelation


class DesignViewedsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class DesignsSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    vieweds = DesignViewedsSerializer(many=True, read_only=True)

    class Meta:
        model = Design
        fields = ('id', 'Design_title', 'square', 'author_name', 'annotated_likes', 'rating', 'owner_name', 'vieweds')


class UserDesignRelationSerializer(ModelSerializer):
    class Meta:
        model = UserDesignRelation
        fields = ('design', 'like', 'in_bookmarks', 'rate')
