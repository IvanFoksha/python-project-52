from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
