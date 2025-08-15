from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View
from django.contrib import messages


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
    form_class = UserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)


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
    form_class = AuthenticationForm
    template_name = 'login.html'

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

    def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
            else:
                return JsonResponse({'success': True, 'message': 'Неверные данные'}, status=400)
        return render(request, 'login.html')
