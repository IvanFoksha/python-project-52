from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    login,
    authenticate,
    update_session_auth_hash,
)
from django.views import View
from django.contrib import messages
from .forms import CustomUserCreationForm, UserChangeForm
from .models import Status, Task, Label


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


'''Работа с моделью - User'''


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


'''Работа с моделью - Status'''


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
        else:
            # status = self.get_object()
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
            f'Статус "{self.object.name}" успешно удален!'
        )
        return redirect(self.get_success_url())


'''Работа с моделью - Task'''


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all()

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


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    fields = ['name', 'description', 'status', 'assignee', 'labels']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        task = form.save()
        messages.success(
            self.request,
            f'Задача "{task.name}" успешно создана!'
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
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
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
        task = form.save()
        messages.success(
            self.request,
            f'Задача "{task.name}" успешно обновлена!'
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
            'Необходима авторизация пользователя.'
        )
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
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
                'Удаление задачи может выполнить только автор.'
            )
            return redirect('task_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(
            request,
            f'Задача "{self.object.name}" успешно удалена!'
        )
        return redirect(self.get_success_url())


'''Работа с моделью - Status'''


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
#
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['statuses'] = Status.objects.all()
    #     context['users'] = User.objects.all()
    #     return context


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
