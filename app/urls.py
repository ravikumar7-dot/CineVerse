from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<uuid:uu_id>/', views.movie_detail, name='movie'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-to-list/<uuid:uu_id>/', views.add_to_list, name='add_to_list'),
    path('remove-from-list/<uuid:uu_id>/', views.remove_from_list, name='remove_from_list'),
    path('my-list/', views.my_list, name='my_list'),
]