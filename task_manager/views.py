import rollbar
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views import View
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


class TestErrorView(View):
    def get(self, request):
        a = None
        a.hello()  # Искусственная ошибка
        return HttpResponse("Hello, world")


def handler500(request):
    rollbar.report_exc_info(request=request)
    return HttpResponseServerError("Произошла ошибка на сервере.")


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
