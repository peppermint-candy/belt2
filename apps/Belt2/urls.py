from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "main"),
    url(r'^register$', views.register ),
    url(r'^login$', views.login ),
    url(r'^friends$', views.friends, name = "friends" ),
    url(r'^user/(?P<id>\d+$)', views.profile, name = "profile"),
    url(r'^addfriend/(?P<id>\d+$)', views.addFriend, name ="addfriend"),
    url(r'^remove/(?P<id>\d+$)', views.remove, name = "remove"),

]
