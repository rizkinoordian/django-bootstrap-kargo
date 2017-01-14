from django.conf.urls import url
from orders import views as order_views

urlpatterns = [
    url(r'^$', order_views.index, name="index"),
    url(r'^management/$', order_views.management, name="management"),

    url(r'^create_order/$', order_views.create_order, name="create_order"),
    url(r'^edit_order/(?P<uuid>[0-9a-z-]+)/$',
        order_views.edit_order, name="edit_order"),
    url(r'^delete_order/(?P<uuid>[0-9a-z-]+)/$',
        order_views.delete_order, name="delete_order"),
]
