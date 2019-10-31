"""
    Invoice Exchange APIs
"""
from django.urls.conf import include, path


urlpatterns = [
    path('auth/', include(('apps.api.urls', 'login_api'), namespace='login_api')),
]