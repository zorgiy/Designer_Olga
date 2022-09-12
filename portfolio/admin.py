from django.contrib import admin
from django.contrib.admin import ModelAdmin

from portfolio.models import Design, UserDesignRelation


@admin.register(Design)
class DesignAdmin(ModelAdmin):
    pass


@admin.register(UserDesignRelation)
class UserDesignRelationAdmin(ModelAdmin):
    pass
