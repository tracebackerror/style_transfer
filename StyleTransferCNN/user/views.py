from django.views.generic import TemplateView, CreateView, View
from django.shortcuts import redirect,render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from tensorflow.python.eager.context import context
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import run_style_transfer, to_image
from django.conf import settings
import os
import random

class ForgotPassword(TemplateView):
    template_name = 'user/forgot_pass.html'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context["verified"] = False
        self.extra_context["setpass"] = False

        if request.user.is_authenticated:
            return redirect("dashboard")
        username = request.GET.get('username',False)
        if username:
            user_obj = User.objects.filter(username=username)
            setup_obj = SetupForgotPassword.objects.filter(user = user_obj.first())
            if user_obj and setup_obj:
                setup_obj = setup_obj.first()
                transformed_list = [setup_obj.transformed1,setup_obj.transformed2,setup_obj.transformed3]
                transformed_list = list(filter(None,transformed_list))
                transformed_url_list = [i.url for i in transformed_list]
                if len(transformed_list)==3:
                    self.extra_context["verified"] = True
                    random_image_url = []
                    media_dirs = os.path.join(settings.MEDIA_ROOT,'transformed_images')
                    for file in os.listdir(media_dirs):
                        if file.endswith(".jpg") or file.endswith(".jpeg"):
                            img_url = "/media/transformed_images/"+file
                            if img_url not in transformed_url_list:
                                random_image_url.append(img_url)
                    
                    random.shuffle(random_image_url)
                    imgset1 = random_image_url[:8]
                    imgset1.append(setup_obj.transformed1.url)
                    random.shuffle(imgset1)

                    random.shuffle(random_image_url)
                    imgset2 = random_image_url[:8]
                    imgset2.append(setup_obj.transformed2.url)
                    random.shuffle(imgset2)

                    random.shuffle(random_image_url)
                    imgset3 = random_image_url[:8]
                    imgset3.append(setup_obj.transformed3.url)
                    random.shuffle(imgset3)

                    self.extra_context["imgset1"] = imgset1
                    self.extra_context["imgset2"] = imgset2
                    self.extra_context["imgset3"] = imgset3

                else:
                    messages.error(request,"You haven't setup forgot password")
            else:
                messages.error(request,"User doesn't exist")
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        new_password1 = request.POST.get("new_password1",None)
        username = request.POST['username']
        user_obj = User.objects.get(username=username)

        if new_password1:
            form = CustomSetPasswordForm(user_obj,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password reset successful")
                return redirect('login')
            else:
                context = {}
                context["verified"] = False
                context["setpass"] = True
                context["username"] = username
                context["form"] = form
                return self.render_to_response(context)

        imgsrclist = request.POST['imgsrclist'].split(",")
        setup_obj = SetupForgotPassword.objects.get(user = user_obj)
        transformed_list = [setup_obj.transformed1.url,setup_obj.transformed2.url,setup_obj.transformed3.url]
        correct_img = 0
        for src in imgsrclist:
            if src in transformed_list:
                correct_img += 1
        if correct_img>=2:
            context = {}
            context["verified"] = False
            context["setpass"] = True
            context["username"] = username
            context["form"] = CustomSetPasswordForm(user=user_obj)
            return self.render_to_response(context)
        
        messages.error(request,"Unauthorized : You have selected incorrect image")
        return redirect('forgot_pass')

class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = 'user/dashboard.html'
    login_url = reverse_lazy('login')

class UserLogin(LoginView):
    template_name = 'user/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().get(request, *args, **kwargs)

class UserSignUp(CreateView):
    template_name = 'user/sign_up.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class SetUpForgotPassword(TemplateView):
    template_name = 'user/setup_forgot_pass.html'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        self.extra_context["transformed1"] = None
        self.extra_context["transformed2"] = None
        self.extra_context["transformed3"] = None

        self.extra_context["range_list"] = [i for i in range(1,4)]
        obj = SetupForgotPassword.objects.filter(user=request.user)
        if obj:
            obj = obj.first()
            self.extra_context["transformed1"] = obj.transformed1
            self.extra_context["transformed2"] = obj.transformed2
            self.extra_context["transformed3"] = obj.transformed3
        return super().get(request, *args, **kwargs)

    def saveObj(self,row,numpy_img,obj=None):
        if obj is None:
            obj = SetupForgotPassword()
            obj.user = self.request.user
        if row == 1:
            obj.transformed1 = to_image(numpy_img)
        elif row == 2:
            obj.transformed2 = to_image(numpy_img)
        else:
            obj.transformed3 = to_image(numpy_img)        
        obj.save()

    def post(self, request, *args, **kwargs):
        content_file = request.FILES['content_file']
        style_file = request.FILES['style_file']
        num_iterations = int(request.POST.get("num_iteration",10))
        row = int(request.POST["row"])

        # Style Transformation 
        best, best_loss = run_style_transfer(content_file, style_file, num_iterations=num_iterations)

        obj = SetupForgotPassword.objects.filter(user=request.user)
        if obj:
            obj = obj.first()
            self.saveObj(row,best,obj)
        else:
            self.saveObj(row,best)
        return redirect("setup_forgot_pass")