from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from task_manager.users.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django_filters.views import FilterView
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_queryset(self):
        queryset = Task.objects.all().select_related(
            'status', 'author', 'assignee'
        ).prefetch_related('labels')
        if self.request.GET.get('own_tasks') == 'on':
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['statuses'] = Task._meta.get_field(
            'status').remote_field.model.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Task._meta.get_field(
            'labels').remote_field.model.objects.all()
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Необходима авторизация пользователя.'
        )
        return redirect('index')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    fields = ['name', 'description', 'status', 'assignee', 'labels']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            'Задача успешно создана'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка создания задачи. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Необходима авторизация пользователя.'
        )
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Task._meta.get_field(
            'status'
        ).remote_field.model.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Task._meta.get_field(
            'labels'
        ).remote_field.model.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Необходима авторизация пользователя.'
        )
        return redirect('index')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_update.html'
    fields = ['name', 'description', 'status', 'assignee', 'labels']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно изменена'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка обновления задачи. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request,
            'У вас нет прав для изменения этой задачи.'
        )
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Task._meta.get_field(
            'status'
        ).remote_field.model.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Task._meta.get_field(
            'labels'
        ).remote_field.model.objects.all()
        return context


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Необходима авторизация пользователя.'
            )
            return redirect('index')
        else:
            messages.error(
                self.request,
                'Задачу может удалить только ее автор.'
            )
            return redirect('task_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно удалена'
        )
        return super().form_valid(form)
