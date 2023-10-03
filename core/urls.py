from django.urls import path
from .views import (
    login_view,
    home,
    logout_view,
    change_pass
)

urlpatterns = [
    path('accounts/login/', login_view, name='login_view'),
    path('accounts/logout/', logout_view, name='logout_view'),
    path('', home, name='home'),
    path('change_pass', change_pass, name='change_pass'),
]