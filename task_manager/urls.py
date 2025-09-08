from django.urls import path, include
from django.contrib.auth import views as auth_views
from task_manager.views import (
    index,
    about,
    TestErrorView,
    CustomLoginView,
    CustomLogoutView,
)
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('test-error/', TestErrorView.as_view(), name='test_error'),
]
