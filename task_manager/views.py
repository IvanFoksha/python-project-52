from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    login,
    update_session_auth_hash,
)
from django.views import View
from django.contrib import messages
from .forms import CustomUserCreationForm, UserChangeForm
from .models import Status


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


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
    success_url = reverse_lazy('index')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            f'Пользователь {user.username} успешно создан!'
        )
        login(self.request, user)
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
            'У вас нет прав для редактированя этого профиля.'
        )
        return redirect('user_list')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Профиль успешно обновлен!')
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


class CustomLoginView(View):
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вы успешно вошли как {user.username}!')
            return redirect('index')
        messages.error(request, 'Неверные данные или ошибка входа.')
        return render(request, 'index.html', {'form': form})


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('status_list')
    fields = ['name']

    def form_valid(self, form):
        status = form.save()
        messages.success(
            self.request,
            f'Статус "{status.name}" успешно создан!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка создания статуса. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('status_list')
    fields = ['name']

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object()
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            'У вас нет прав для редактированя этого статуса.'
        )
        return redirect('status_list')

    def form_valid(self, form):
        status = form.save()
        messages.success(
            self.request,
            f'Статус "{status.name}" успешно обновлен!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка обновления статуса. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')

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
        return redirect('status_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.has_related_tasks():
            messages.error(request, 'Нельзя удалить статус, связанный с задачами.')
            return self.render_to_response(self.get_context_data())
        self.object.delete()
        messages.success(request, f'Статус "{self.object.name}" успешно удален!')
        return redirect(self.get_success_url())
