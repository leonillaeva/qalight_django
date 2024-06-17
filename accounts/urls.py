from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path(
        "activate/<str:username>/<str:token>/",
        views.ActivateAccountView.as_view(),
        name="activate",
    ),
]

app_name = 'accounts'  # accounts:home
