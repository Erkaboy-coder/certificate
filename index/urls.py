from django.urls import path, include, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.Home, name='home_page'),
    re_path(r'^search/$', views.search, name="search"),
    re_path(r'^search_big/$', views.search_big, name="search_big"),
    re_path(r'^worker_home_page/$', views.worker_home_page, name="worker_home_page"),

    re_path(r'^create_certificate/$', views.create_certificate, name="create_certificate"),
    re_path(r'^delete/(?P<id>\d+)/$', views.delete, name="delete"),
    re_path(r'^show/(?P<id>\d+)/$', views.show, name="show"),
    re_path(r'^edit/(?P<id>\d+)/$', views.edit, name="edit"),
    re_path(r'^edit_certificate/(?P<id>\d+)/$', views.edit_certificate, name="edit_certificate"),

    re_path(r'^give_permission/(?P<id>\d+)/$', views.give_permission, name="give_permission"),

    re_path(r'^login_page/$', views.login_page, name="login_page"),
    re_path(r'^sign_in/$', views.sign_in, name="sign_in"),
    re_path(r'^logout/$', views.logout, name="logout"),
]