from django.shortcuts import render,redirect
from django.conf import settings
from .models import ImageUpload
from django.views import View
from os import getcwd
import os
from json import load,JSONDecodeError
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
# Create your views here.
class Home(View):
    def get(self, request,*args,**kwargs):
        configs= read_json(os.getenv('CONFIG_PATH'))
        context = {}
        if 'searchText' in request.session and (request.session['searchText'] !="" or request.session['searchText'] is None) :
            search_text = request.session.get('searchText')
            image_data  = ImageUpload.objects.filter(image_category__category=search_text).values().order_by('-upload_date')
        else:
            image_data = ImageUpload.objects.all().values().order_by('-upload_date')
        context['image_data'] = image_data
        context['configs'] = configs
        return render(request, 'index.html', context)
    def post(self,request,*args,**kwargs):
        context = {}
        configs= read_json(os.getenv('CONFIG_PATH'))
        search_text = request.POST.get('search')
        if request.POST.get('btncancel') == 'cancel':
            search_text = ""
            del request.session['searchText']
        if(search_text !="" and search_text is not None):
            request.session['searchText'] = search_text
            image_data  = ImageUpload.objects.filter(image_category__category=search_text).values().order_by('-upload_date')
        else:
            request.session['searchText'] = search_text
            image_data = ImageUpload.objects.all().values()
        context['image_data'] = image_data
        context['configs'] = configs
        return render(request,'index.html',context)
def read_json(path):
    try:
        with open(path) as json_obj:
            data = load(json_obj)
        return data
    except FileNotFoundError:
        return None
    except JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
class SendMail(View):
    def post(self,request,*args,**kwargs):
        fullName = request.POST.get('fullName')
        email = request.POST.get('email')
        phoneNo = request.POST.get('phoneNo')
        message = request.POST.get('messageBox')
        send_message = f"Hi {fullName} , \n\n {message} \n\n Thanks & regard \n {fullName} \n {email}\n {phoneNo}"
        # code for response for customer
        customer_mail_objects = {
            'subject':f"Mail from {email}",
            'fullname':fullName,
            'sender_mail':email,
            'reciever_mail':settings.EMAIL_HOST_USER,
            'message':message,
            'user_type':"customer"
        }
        
        try:
            if self.send_email_message(self,request,*args,**customer_mail_objects):
                admin_mail_objects= {}
                admin_mail_objects['subject'] = f"Response from MyPicDocs {settings.EMAIL_HOST_USER}"
                admin_mail_objects['user_type'] = "admin"
                admin_mail_objects['sender_mail'] = customer_mail_objects['reciever_mail']
                admin_mail_objects['reciever_mail'] = customer_mail_objects['sender_mail']
                admin_mail_objects['message'] ="Our team has been connected wit you as soon as possible with your concern and message..!"
                if self.send_email_message(self,request,*args,**admin_mail_objects):
                    pass
            return redirect('/')
        except:
            print("Mail sending errors")
            return redirect("/")
    def send_email_message(self,request,*args,**kwargs):
        template = get_template('sender_mail.html')
        context = kwargs
        email_content = template.render(context)
        email = EmailMessage(kwargs['subject'],email_content,kwargs['sender_mail'],[kwargs['reciever_mail']],reply_to=[kwargs['sender_mail']])
        email.content_subtype = 'html'
        return email.send()
