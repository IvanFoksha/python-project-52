# import django_filters
# from django import forms
# from django.contrib.auth.models import User
# from task_manager.tasks.models import Task
# # from task_manager.statuses.models import Status
# # from task_manager.labels.models import Label
#
# class TaskFilter(django_filters.FilterSet):
#     status = django_filters.ModelChoiceFilter(
#         queryset=Status.objects.all(),
#         label='Статус',
#     )
#     assignee = django_filters.ModelChoiceFilter(
#         queryset=User.objects.all(),
#         label='Исполнитель',
#     )
#     labels = django_filters.ModelMultipleChoiceFilter(
#         queryset=Label.objects.all(),
#         label='Метка',
#         conjoined=False,
#     )

#     class Meta:
#         model = Task
#         fields = ['status', 'assignee', 'labels']


import django_filters
from django import forms
from task_manager.users.models import User
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
# from task_manager.statuses.models import Status
# from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        # queryset='statuses.Status'.objects.all(),
        queryset=None,
        label='Статус',
    )
    assignee = django_filters.ModelChoiceFilter(
        queryset=get_user_model(),
        label='Исполнитель',
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        # queryset='labels.Label'.objects.all(),
        queryset=None,
        label='Метка',
        conjoined=False,
    )
    own_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method='filter_own_tasks',
        widget=forms.CheckboxInput,
        field_name=None,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request', None)
        super().__init__(*args, **kwargs)
        self.filters['status'].field.queryset = Task._meta.get_field('status').remote_field.model.objects.all()
        self.filters['labels'].field.queryset = Task._meta.get_field('labels').remote_field.model.objects.all()

    def filter_own_tasks(self, queryset, name, value):
        if value and self.request:
            print("Applying own_tasks filter, user:", self.request.user, "value:", value)
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels']
