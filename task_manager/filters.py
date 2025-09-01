import django_filters
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
        widget=django_filters.widgets.BooleanWidget,
        field_name=None,
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'own_tasks']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def filter_own_tasks(self, queryset, name, value):
        # author = self.request.user.pk if self.request.user == self.task.author else None
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.task.author) # =author -- попытался даже сравнить с author в модели Task
        return queryset
