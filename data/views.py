from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

class UserLogin(LoginView):
    template_name = 'data/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasks')

class UserRegister(FormView):
    template_name = 'data/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserRegister, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'Task'
    print(Task)
    template_name = 'data/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Task'] = context['Task'].filter(user=self.request.user)
        context['count'] = context['Task'].filter(complite=False).count()

        search_area = self.request.GET.get('search-area') or ''
        if search_area:
            context['Task'] = context['Task'].filter(title__icontains = search_area)
        context['search_area'] = search_area
        return context


class TaskDetails(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'Task'
    # template_name = 'data/taskDetail'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complite']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complite']
    success_url = reverse_lazy('tasks')
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'Task'
    success_url = reverse_lazy('tasks')

