from django.conf.urls import include
from django.conf.urls import url
from whitelist.urls.api.v1 import urls as v1_urls


# versioned includes
urlpatterns = [
    url(r'^v1/', include((v1_urls, 'v1'), namespace='v1')),
]