from multiprocessing import context
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
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
from .models import Task, UserProfileModel
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import UserProfileForm
import json
from django.shortcuts import render, HttpResponse


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
                if UserProfileModel.objects.filter(user=user_name_object).first():
                    user_profile_object= user_name_object.related_profile
                    print("is block or not -> login page::", user_profile_object.blocked)
                    if user_profile_object.blocked:
                        error_messsage = {
                            'messag':'You are blocked.Create one',
                        }
                        return render(request, 'data/login.html', {'form':form, 'error_messsage':error_messsage})
                    else:
                        print("user password is exist")
                        login(self.request,user_name_object)
                        return redirect('tasks')

              
                  
            else:
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


class UserRegister(FormView):
    template_name = 'data/register.html'
    form_class = UserRegistationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            print("user")
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
   
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class UserList(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            user_list = User.objects.all()
            pagnator = Paginator(user_list,4)
            page = request.GET.get('page')
            page_obj = pagnator.get_page(page)
            # print("request of ajax or not :::", page_obj.number())
            if is_ajax(request):
                result = {}
                for value in page_obj.object_list:
                    # print("user_value:::::",value.username)
                    # print("user_value:::::",value.email)
                    result[value.id]={}
                    result[value.id]['username']=value.username
                    result[value.id]['email']=value.email
                print("result",result)
                result['has_next']=page_obj.has_next()
                result['has_previous']=page_obj.has_previous()
        
                return JsonResponse({'data':result})

            return render(request,'data/users.html',{'page_obj':page_obj})
        else:
            return redirect('tasks')

        

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
class UserProfile(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print("primary key: ", pk)
        user_object= User.objects.filter(pk=pk).first()
        user_profile= UserProfileModel.objects.filter(user=user_object).first()
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        address = request.POST.get('address')
        image = request.FILES.get("image")
        status = request.POST.get('check', "false")

        if user_profile:
            user_profile.first_name = firstName
            user_profile.last_name = lastName
            user_profile.address = address
            user_profile.image = image
            if not user_profile.image:
                user_profile.image = user_object.related_profile.image
            if status == 'on':
                print("He is blcoked..")
                user_profile.blocked = True
            else:
                print("He is unblocked")
                user_profile.blocked  = False
            user_profile.save()  
        else:
            UserProfileModel.objects.create(user=user_object, first_name=firstName, last_name=lastName, address=address, image=image)
        user_profile= UserProfileModel.objects.filter(user=user_object).first()
        return render(request, 'data/userInfo.html',{'user':user_object,'profile':user_profile})
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk == request.user.pk or request.user.is_superuser:
            user_object= User.objects.filter(pk=pk).first()
            if UserProfileModel.objects.filter(user=user_object).first():
                user_profile_object= user_object.related_profile
            else:
                user_profile_object = ''
            return render(request, 'data/userInfo.html',{'user':user_object,'profile':user_profile_object})
        else:
            return redirect('profile',pk=request.user.pk)
