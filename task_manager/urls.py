from django.urls import path
from django.contrib.auth import views as auth_views
from task_manager.views import (
    index,
    about,
    TestErrorView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CustomLoginView,
    StatusListView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    LabelListView,
    LabelCreateView,
    LabelUpdateView,
    LabelDeleteView,
)
from django.contrib import admin

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path(
        'users/<int:pk>/update/',
        UserUpdateView.as_view(),
        name='user_update'
    ),
    path(
        'users/<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete'
    ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='index',
            template_name='logout.html'
        ),
        name='logout'),
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/create', StatusCreateView.as_view(), name='status_create'),
    path(
        'statuses/<int:pk>/update/',
        StatusUpdateView.as_view(),
        name='status_update'
    ),
    path(
        'statuses/<int:pk>/delete/',
        StatusDeleteView.as_view(),
        name='status_delete'
    ),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create', TaskCreateView.as_view(), name='task_create'),
    path(
        'tasks/<int:pk>/update/',
        TaskUpdateView.as_view(),
        name='task_update'
    ),
    path(
        'tasks/<int:pk>/delete/',
        TaskDeleteView.as_view(),
        name='task_delete'
    ),
    path(
        'tasks/<int:pk>',
        TaskDetailView.as_view(),
        name='task_detail'
    ),
    path('labels/', LabelListView.as_view(), name='label_list'),
    path('labels/create', LabelCreateView.as_view(), name='label_create'),
    path(
        'labels/<int:pk>/update/',
        LabelUpdateView.as_view(),
        name='label_update'
    ),
    path(
        'labels/<int:pk>/delete/',
        LabelDeleteView.as_view(),
        name='label_delete'
    ),
    path('test-error/', TestErrorView.as_view(), name='test_error'),
]
