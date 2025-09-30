from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.urls import reverse_lazy
from .models import Status
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Необходима авторизация пользователя.'
        )
        return redirect('index')


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('status_list')
    fields = ['name']

    def form_valid(self, form):
        # status = form.save()
        messages.success(
            self.request,
            'Статус успешно создан'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка создания статуса. Проверьте данные.'
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


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('status_list')
    fields = ['name']

    def form_valid(self, form):
        # status = form.save()
        messages.success(
            self.request,
            'Статус успешно изменен'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка обновления статуса. Проверьте данные.'
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


class StatusDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')

    def test_func(self):
        status = self.get_object()
        return not status.has_related_tasks()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Необходима авторизация пользователя.'
            )
            return redirect('index')
        messages.error(
            self.request,
            'Нельзя удалить статус, связанный с задачами.'
        )
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.test_func():
            messages.error(
                request,
                'Нельзя удалить статус, связанный с задачами.'
            )
            return redirect(self.success_url)
        self.object.delete()
        messages.success(
            request,
            'Статус успешно удален'
        )
        return redirect(self.success_url)
