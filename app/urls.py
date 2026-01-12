from django.urls import path, include
from . import views



urlpatterns = [
    
    
    path('', views.landing_page, name='landing_page'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout, name='logout'),

    path('ajax/validate/', views.ajax_validate_field, name='ajax_validate_field'),
    
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]
 
