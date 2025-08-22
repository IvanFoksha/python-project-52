import django_filters
from django.contrib.auth.models import User
from .models import Task, Status, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label='Все статусы'
    )
    assignee = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        empty_label='Все исполнители'
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        empty_label='Все метки'
    )
    own_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method='filter_own_tasks',
        widget=django_filters.widgets.BooleanWidget
    )

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'label', 'own_tasks']

    def filter_own_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(authors=self.request.user)
        return queryset

    @property
    def qs(self):
        parent = super().qs
        self.request = self.request
        return parent
