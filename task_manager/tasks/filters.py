# import django_filters
# from django import forms
# from django.contrib.auth.models import User
# from task_manager.tasks.models import Task
# # from task_manager.statuses.models import Status
# # from task_manager.labels.models import Label


# class TaskFilter(django_filters.FilterSet):
#     status = django_filters.ModelChoiceFilter(
#         # queryset=Status.objects.all(),
#         # queryset=Task._meta.get_field('status').related_model.objects.all(),
#         queryset=None,
#         label='Статус',
#     )
#     assignee = django_filters.ModelChoiceFilter(
#         # queryset=User.objects.all(),
#         # queryset=User.objects.all(),
#         queryset=None,
#         label='Исполнитель',
#     )
#     labels = django_filters.ModelMultipleChoiceFilter(
#         # queryset=Label.objects.all(),
#         # queryset=Task._meta.get_field('labels').related_model.objects.all(),
#         queryset=None,
#         label='Метка',
#         conjoined=False,
#     )
#     own_tasks = django_filters.BooleanFilter(
#         label='Только свои задачи',
#         method='filter_own_tasks',
#         widget=forms.CheckboxInput,
#         field_name=None,
#     )

#     # def __init__(self, *args, **kwargs):
#     #     self.request = kwargs.get('request', None)
#     #     super().__init__(*args, **kwargs)

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.get('request', None)
#         super().__init__(*args, **kwargs)
#         self.filters['status'].extra.update(
#             queryset=Task._meta.get_field('status').remote_field.model.objects.all()
#         )
#         self.filters['assignee'].extra.update(
#             queryset=User.objects.all()
#         )
#         self.filters['labels'].extra.update(
#             queryset=Task._meta.get_field('labels').remote_field.model.objects.all()
#         )

#     def filter_own_tasks(self, queryset, name, value):
#         if value and self.request:
#             filtered_qs = queryset.filter(author=self.request.user)
#             return filtered_qs
#         return queryset

#     class Meta:
#         model = Task
#         fields = ['status', 'assignee', 'labels']


import django_filters
from django import forms
from django.contrib.auth.models import User
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
        queryset=User.objects.all(),
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
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels']
