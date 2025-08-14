from django.urls import path
from task_manager.views import index, UserListView
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user_list')
]
