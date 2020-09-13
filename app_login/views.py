from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.generic import CreateView, FormView, TemplateView, ListView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url

from .forms import RegisterForm, LoginForm
from .models import User

class HomeView(ListView):
    model         = User
    template_name = 'app_login/home.html'
    context_object_name = 'donors'

class RegisterView(SuccessMessageMixin, CreateView):
    form_class      = RegisterForm
    template_name   = 'app_login/register.html'
    success_message = 'Account Created Successfully'
    
    def get_success_url(self):
        return reverse('app_login:login')


class LoginView(FormView):
    form_class    = LoginForm
    template_name = 'app_login/login.html'
    success_url   = '/'
    

    def form_valid(self, form):
        request       = self.request
        next_         = request.GET.get('next')
        next_post     = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email         = form.cleaned_data.get("email")
        password      = form.cleaned_data.get("password")
        user          = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
