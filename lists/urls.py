from django.conf.urls import patterns, include, url
from django.contrib import admin

from lists import views


urlpatterns = patterns(
    '',
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),

    url(
        r'^show_mine_ip_pls/$',
        'lists.views.show_self_ip',
        name='show_self_ip'
    ),
)
