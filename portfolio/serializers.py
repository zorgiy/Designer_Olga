from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from portfolio.models import Design, UserDesignRelation


class DesignsSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Design
        fields = ('id', 'Design_title', 'square', 'author_name', 'likes_count', 'annotated_likes', 'rating')

    def get_likes_count(self, instance):
        return UserDesignRelation.objects.filter(design=instance, like=True).count()


class UserDesignRelationSerializer(ModelSerializer):
    class Meta:
        model = UserDesignRelation
        fields = ('design', 'like', 'in_bookmarks', 'rate')
