from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.menu, name='index'),
    path('order-view/<int:id>', views.order_view, name='view_order'),
    path('order-view/', views.order_view, name='order'),

    path('stream/<int:order_id>/', views.sse_stream, name='sse_stream'),

    path('tracking-order-location/<int:order_id>', views.track_location, name='sse_stream'),
    path('send-driver-location/<int:order_id>', views.send_driver_location, name='sse_stream'),

]