from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from portfolio.models import Design, UserDesignRelation
from portfolio.permissions import IsOwnerOrStaffOrReadOnly
from portfolio.serializers import DesignsSerializer, UserDesignRelationSerializer


class DesignViewSet(ModelViewSet):
    queryset = Design.objects.all().annotate(
            annotated_likes=Count(Case(When(userdesignrelation__like=True, then=1))),
        ).select_related('owner').prefetch_related('vieweds').order_by('id')
    serializer_class = DesignsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['square']
    search_fields = ['Design_title', 'author_name']
    ordering_fields = ['square', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserDesignsRelationsView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserDesignRelation.objects.all()
    serializer_class = UserDesignRelationSerializer
    lookup_field = 'design'

    def get_object(self):
        obj, _ = UserDesignRelation.objects.get_or_create(user=self.request.user, design_id=self.kwargs['design'])
        return obj


def auth(request):
    return render(request, 'oauth.html')
