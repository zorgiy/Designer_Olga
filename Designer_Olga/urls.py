from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from portfolio.views import DesignViewSet, auth, UserDesignsRelationsView

router = SimpleRouter()

router.register(r'design', DesignViewSet)
router.register(r'design_relation', UserDesignsRelationsView)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('__debug__/', include('debug_toolbar.urls'))
]

urlpatterns += router.urls
