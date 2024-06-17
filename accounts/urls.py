from django.urls import path

from .views import home_view, login_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
]

app_name = 'accounts'  # accounts:home
