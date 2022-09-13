from django.db.models import Avg

from portfolio.models import UserDesignRelation


def set_rating(design):
    rating = UserDesignRelation.objects.filter(design=design).aggregate(rating=Avg('rate')).get('rating')
    design.rating = rating
    design.save()
