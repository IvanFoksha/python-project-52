import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task, Status, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
    )
    assignee = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
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

    def filter_own_tasks(self, queryset, name, value):
        if value and self.request:
            filtered_qs = queryset.filter(author=self.request.user)
            return filtered_qs
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels']
