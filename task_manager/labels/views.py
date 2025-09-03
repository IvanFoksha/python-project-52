from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Label.objects.all()

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


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    template_name = 'labels/label_create.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        form.instance.created_at = timezone.now()
        label = form.save()
        messages.success(
            self.request,
            f'Метка "{label.name}" успешно создана!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка создания метки. Проверьте данные.'
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
        return super().get_context_data(**kwargs)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'labels/label_update.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        label = form.save()
        messages.success(
            self.request,
            f'Метка "{label.name}" успешно обновлена!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка обновления метки. Проверьте данные.'
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


class LabelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')

    def test_func(self):
        label = self.get_object()
        return not label.has_related_tasks()

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
                'Нельзя удалить метку, связанную с задачами.'
            )
            return redirect('label_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(
            request,
            f'Метка "{self.object.name}" успешно удалена!'
        )
        return redirect(self.get_success_url())
