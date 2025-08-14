from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
