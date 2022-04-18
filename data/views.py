from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages

from .models import UserRegistationForm
from .models import Task
from django.urls import reverse_lazy
from django.core.paginator import Paginator



class UserLogin(LoginView):
    template_name = 'data/login.html'   
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
            
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_name_object= User.objects.filter(username=username).first()
        user_email_object = User.objects.filter(email=username).first()
        if user_name_object:
            if check_password(password,user_name_object.password):
                print("user password is exist")
                login(self.request,user_name_object)
                return redirect('tasks')
                  
            else:
                print("password doesn't mach1")
                messages.error(request, "Comment Invalid!") 
                return render(request, 'data/login.html', {'form':form})
        elif user_email_object:
            if check_password(password,user_email_object.password):
                login(self.request,user_email_object)
                return redirect('tasks')
            else:
                print("password doesn't mach")
                return render(request, 'data/login.html', {'form':form})
        else:
            # form.add_error("user_error","Username or password not correct")
            return render(request, 'data/login.html', {'form':form})

    # def get(self, request, *args, **kwargs):
    #     if not request.user:
    #        return redirect('login')
    #     else:
    #         return redirect('tasks')




class UserRegister(FormView):
    template_name = 'data/register.html'
    form_class = UserRegistationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    # pass_error = ""
    # username_error =""

    # def post(self,request):
    #     print()
    #     return render(request, template_name=self.template_name)
    
    def form_invalid(self, form):
        print("Registation_info:",form.cleaned_data)
        flag = 0
        user_name = ""
        for key, value in form.cleaned_data.items():
            if key == "username":
                user_name = value
            elif  key == "password1":
                flag+=1
            elif key == "password2":
                flag+=1;
        # if not user_name:
        #     # form.add_error("username","username already exist.")
        
        #     # form['username_error'] = "username already exist."
        # if int(flag) !=2:
        #     form.add_error("password2","Passowrd miss mass")
        return super(UserRegister, self).form_invalid(form)
        


    def get(self, *args, **kwargs):
        # print("dfffffffffffffffffffffffffffffffff")
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserRegister, self).get(*args, **kwargs)
   


class UserList(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        pagnator = Paginator(user_list,10)
        page = request.GET.get('page')
        page_obj = pagnator.get_page(page)
        return render(request, 'data/users.html', {'page_obj':page_obj})
        

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
