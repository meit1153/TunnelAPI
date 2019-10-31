

from django.http import HttpResponseRedirect
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from whitelist.urls import urls


urlpatterns = list()

urlpatterns += [
        
        path('api/', include(('whitelist.urls.api', 'api'), namespace='api')),
]