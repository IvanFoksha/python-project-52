from django.urls import path
from django.contrib.auth import views as auth_views
from task_manager.views import (
    index,
    about,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CustomLoginView,
)
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='index',
            template_name='logout.html'
        ),
        name='logout'),
]
