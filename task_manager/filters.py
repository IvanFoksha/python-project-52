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
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'own_tasks']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def filter_own_tasks(self, queryset, name, value):
        if value and self.request and hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    def filter_labels(self, queryset, name, value):
        if value:
            if not isinstance(value, (list, tuple)):
                value = [value]
            return queryset.filter(labels__in=value).distinct()
        return queryset

    # @property
    # def qs(self):
    #     parent = super().qs
    #     request = getattr(self, 'request', None)
    #     if request:
    #         self.request = request
    #     return parent
