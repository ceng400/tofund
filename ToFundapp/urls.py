from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('', views.landingpage, name = 'landingpage'),
    path('signup', views.signup, name = 'signups'),
    path('signin', views.signin,name='signins'),
    path('donate', views.donate, name = 'donation'),
    path('pay', views.start_payment, name = 'start_payment'),
    path('startfund', views.start_fund, name = 'startfund'),
    path('livefunds', views.livefunds, name = 'livefunds'),
    path('<str:ref>/', views.verify_payment, name = 'verify_payment')
]
