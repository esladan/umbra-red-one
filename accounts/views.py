from decimal import Context
from django.shortcuts import render, redirect
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views import View   
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Account
from menu.models import Category, Food
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, password_reset_token
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from . import util
from django.conf import settings






# Create your views here.
def index(request):
    return render(request,'index/index.html')


@login_required(login_url='/signin')
def dashboard(request):
    return render(request,'index/dashboard.html')

class Signin(View):
    def get(self, request):
        # <view logic>
        return render(request,'index/signup.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        print(user)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse("not a user")
            

class Signup(View):
    def get(self, request):
        # <view logic>
        return render(request,'index/signup.html')

    def post(self, request):
        username = request.POST['username'] 
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']        
        user = Account.objects.create_user(username=username, password=password,first_name=first_name,last_name=last_name, phone_number=phone_number,  ) 
        user.save(); 
        
        current_site = get_current_site(request)
        mail_subject = 'Verify your email'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, ["alsenad390@gmail.com"])
        messages.info(request,'Please confirm your email address to complete the registration')
        return redirect('home')




class Password_reset(View):
    def get(self, request):
        return render(request,'index/password_reset_req.html')

    def post(self, request):
        # """User forgot password form view."""
        if request.POST.get('email') != None:
                email = request.POST.get('email')
                qs = Account.objects.get(email=email)
                           
                user = qs
                user.is_active = False  # User needs to be inactive for the reset password duration
                user.reset_password = True
                user.save()
                current_site = get_current_site(request)
                mail_subject= 'Password Reset Link'
                message = render_to_string('password_reset_mail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':password_reset_token.make_token(user),
                })
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, ["alsenad390@gmail.com"])
                messages.info(request,'A link has being sent to your email')
                return render(request, 'index/password_reset_req.html')
        else:
            messages.error(request,'This is not a registered email')
            return render(request, 'index/password_reset_req.html')

      
        
          
            
# to activate your emaiil Account///////////////////
class Activate_req(View):
    def get(self, request, mail):
        if Account.objects.filter(email=mail).exists():
            context = {
                'email':mail            }
            return render(request, 'index/activate_req.html' ,context)

    def post(self, request, mail):
        if Account.objects.filter(email=mail).exists():
            user = Account.objects.get(email=mail)
            current_site = get_current_site(request)
            mail_subject = 'Verify your email'
            message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, ["alsenad390@gmail.com"])
        messages.info(request,'Please confirm your email address to complete the registration')
        return render(request, 'index/activate_req.html' )
       

# verify token and activate account////////////////////////////////
def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
   
    if Account.objects.filter(pk=uid).exists():
        user = Account.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user)
        # return redirect('home')
  
            messages.info(request,'Your Email has being verified succesfuly')
            return redirect('dashboard')
    else:
        messages.error(request,'Activation link is invalid!')
        return redirect('dashboard')


# render the password Reset page
class Reset(View):

    def get(self,request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            context = {
               'uid': uidb64,
               'token': token
            }
            return render(request, 'index/password_reset_conf.html',context )
        else:
            messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
            messages.add_message(request, messages.WARNING, 'Please request a new password reset.')
            return redirect('home')

    def post(self,request,uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            
            if request.POST.get('password')!= None:
                new_password = request.POST.get('password')                
                user.set_password(new_password)
                user.is_active = True
                user.reset_password = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect('home')
            else:
                context = {
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Password could not be reset.')
                return render(request, 'index/password_reset_conf.html',context )
        else:
            messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
            messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

            return redirect('reset-password')



    



@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/')




@login_required(login_url='/signin')
def profile(request, username):
    profile= Food.objects.all()
    context = {'profile':profile}
    print(context)
    return render(request, 'index/dashboard.html', context)


