from venv import logger
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import (
    login,
    authenticate,
    update_session_auth_hash,
    logout
)
from django.contrib import messages
from task_manager.users.forms import CustomUserCreationForm, UserChangeForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            'Пользователь успешно зарегистрирован'
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка регистрации. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object()
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            'У вас нет прав для редактирования этого профиля.'
        )
        return redirect('user_list')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Исправьте ошибки в форме.'
        )
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object()
        )

    def handle_no_permission(self):
        messages.error(
            self. request,
            'У вас нет прав для удаления этого профиля.'
        )
        return redirect('user_list')

    def form_valid(self, form):
        form.delete()
        messages.success(self.request, 'Пользователь успешно удалён')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context
