from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
    url(r'^new$', 'lists.views.new_list', name='new_list'),

    url(
        r'^show_mine_ip_pls/$',
        'lists.views.show_self_ip',
        name='show_self_ip'
    ),
)
