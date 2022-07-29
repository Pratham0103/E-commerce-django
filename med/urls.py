from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$', views.index),
    url(r'^account/$', views.account),
    url(r'^add_product/$', views.add_product),
    url(r'^edit_product/([\w-]+)$', views.edit_product),
    url(r'^shop/$', views.shop),
    url(r'^search/$', views.search),
    url(r'^product-details/([\w-]+)$', views.product_details),
    url(r'^cart/$', views.cart),
    url(r'^checkout/$', views.checkout),
    url(r'^edit_checkout/$', views.edit_checkout),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout_user),
    url(r'^contact-us/$', views.contact_us),
    url(r'^404/$', views.a),
    url(r'^add_cart/(\d+)$', views.add_cart),
    url(r'^sub_cart/(\d+)$', views.sub_cart),
    url(r'^del_cart/(\d+)$', views.del_cart),
    url(r'^index/([\w-]+)$', views.index2),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', views.activate_user_view),
    url(r'^change_password/(?P<code>[a-z0-9].*)/$', views.change_password),
    url(r'^update_cart/$', views.update_cart),
    url(r'^reset_password/$', views.reset_password),
]
