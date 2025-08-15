from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django import forms


def index(request):
    return render(request, 'index.html')


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(CreateView):
    model = User
    template_name = 'user_create.html'
    success_url = reverse_lazy('index')
    form_class = forms.ModelForm
    fields = ['username', 'first_name', 'last_name', 'password']

    def get_form_class(self):
        class CustomUserCreationForm(forms.ModelForm):
            password = forms.CharField(
                widget=forms.PasswordInput,
                label="Пароль"
            )
            password_confirm = forms.CharField(
                widget=forms.PasswordInput,
                label="Подтверждение пароля"
            )

            class Meta:
                model = User
                fields = ['username', 'first_name', 'last_name', 'password']

            def clean(self):
                cleaned_data = super().clean()
                password = cleaned_data.get("password")
                password_confirm = cleaned_data.get("password_confirm")
                if password != password_confirm:
                    raise forms.ValidationError("Пароли не совпадают.")
                if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
                    raise forms.ValidationError(
                        "Пароль должен содержать минимум 8 символов, включая заглавную букву и цифру."
                    )
                return cleaned_data

            def save(self, commit=True):
                user = super().save(commit=False)
                user.set_password(self.cleaned_data["password"])
                if commit:
                    user.save()
                return user

        return CustomUserCreationForm

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
            'Ошибка создания пользователя. Проверьте данные.'
        )
        return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object()
        )

    def handle_no_permission(self):
        return redirect('user_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object()
        )

    def handle_no_permission(self):
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
        return JsonResponse(
            {'success': False, 'message': 'Неверные данные'},
            status=400
        )
