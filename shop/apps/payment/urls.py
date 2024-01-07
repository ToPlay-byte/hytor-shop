from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('ajax/delete-order', views.AjaxDeleteOrderView.as_view()),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('failed/', views.FailedView.as_view(), name='failed'),
    path('execute/<int:pk>', views.execute_payment, name='execute'),
    path('pay_order/<int:pk>', views.create_order, name='create'),
    path('<int:pk>', views.OrderView.as_view(), name='order'),
    path('my-orders/', views.OrdersList.as_view(), name='orders-list'),
    path('payment/<int:pk>', views.PaymentView.as_view(), name='payment')
]