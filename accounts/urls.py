from django.urls import re_path, include
from django.urls import re_path, include
from django.views.generic import TemplateView

from .views.rest_views import LoginView, RevokeTokenView, RegisterView

app_name = 'accounts'

urlpatterns = [

    # url(r'^$',TemplateView.as_view(template_name='base.html')),
    # url(r'^accounts/home/$',home,name='home'),
    re_path(r'^login/$', LoginView.as_view(), name='rest_login'),
    re_path(r'^register/$', RegisterView.as_view(), name='rest_register'),
    re_path(r'^logout/$', RevokeTokenView.as_view(), name='rest_logout'),
    # re_path(r'^forgot_password/$', TemplateView.as_view(template_name='roommate/password_reset.html'),
    #         name="forgot_password"),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]
