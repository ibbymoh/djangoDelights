from django.urls import path

from .views import  *


urlpatterns = [

    path('register/',CreateUser.as_view(),name="create-user"),
    path('login/',MyLoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(next_page='login'),name="logout"),

]