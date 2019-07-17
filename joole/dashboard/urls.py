__author__ = 'xavier'
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),

    url(r'^$', views.client_log, name='client-form'),

    url(r'^results/(?P<client_id>.+)$', views.results, name='results')
]
