__author__ = 'rusdi'

from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin, name="signin"),
    url(r'^product$', views.product, name="product"),
    url(r'^detail/([0-9])$', views.detail, name="detail"),
    url(r'^cart$', views.cart, name="cart"),
    url(r'^add-cart$', views.tmpCart, name="addcart"),
    url(r'^cart-item', views.cartItem, name="cartitem"),
    url(r'^clear-cart', views.clearCart, name="clearcart"),
    url(r'^checkout', views.checkout, name="checkout"),
]
