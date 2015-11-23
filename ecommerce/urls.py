__author__ = 'rusdi'

from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin, name="signin"),
    url(r'^product$', views.product, name="product"),
    url(r'^detail/([0-9])$', views.detail, name="detail"),
    url(r'^cart$', views.cart, name="cart"),


]
