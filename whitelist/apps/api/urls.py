from django.conf.urls import url
from .views import LoginView, AssignedPort


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name="user_login"),
    url(r'^assigned-port', AssignedPort.as_view(), name="user_assigned_port"),
]

