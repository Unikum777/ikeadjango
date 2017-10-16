from django.conf.urls import url
from . import views

app_name = 'ikealist'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<ikea_id>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^add/', views.add, name='add'),
]
