

from django.conf.urls import url
from school import views as music_views


app_name = "school"

urlpatterns = [

    url(r'^$', music_views.dashboard, name='dashboard'),
    url(r'^login/$', music_views.login_user, name='login'),
    url(r'^register/$', music_views.register, name='register'),
    url(r'^logout/$', music_views.logout_user, name='logout'),
    url(r'^teachers/$', music_views.teachers, name='teachers'),
    url(r'^students/$', music_views.students, name='students'),
    url(r'^books/$', music_views.books, name='books'),
    url(r'^profile/$', music_views.profile, name='profile'),
]
