from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^process$', views.process),
    url(r'^dashboard$', views.success),
    url(r'^addprocess$', views.addprocess),
    url(r'^add$', views.addwish),
    url(r'^wish_items/(?P<item_id>\d+)$', views.item),
    url(r'^add/(?P<item_id>\d+)$', views.addtowishlist),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),


]
