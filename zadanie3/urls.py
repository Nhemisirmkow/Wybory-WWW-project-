from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^kraj', views.kraj),
    url(r'^województwo/PL-(?P<skrót>\w+)', views.województwo),
    url(r'^okręg/(?P<numer>[0-9]+)', views.okręg),
    url(r'^gmina/(?P<id>[0-9]+)', views.gmina),
    url(r'^login', views.loginView),
    url(r'^logout', views.logoutView),
    url(r'^test2', views.test_list),
    # url(r'^test$', views.index, name='index'),
    url(r'^przekierujDoGminy', views.przekierujDoGminy),
]