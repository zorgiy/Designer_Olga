from rest_framework.serializers import ModelSerializer

from portfolio.models import Design, UserDesignRelation


class DesignsSerializer(ModelSerializer):
    class Meta:
        model = Design
        fields = '__all__'


class UserDesignRelationSerializer(ModelSerializer):
    class Meta:
        model = UserDesignRelation
        fields = ('design', 'like', 'in_bookmarks', 'rate')
