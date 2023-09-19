from django.shortcuts import render,redirect
from django.conf import settings
from .models import ImageUpload
from django.views import View
import os
from json import load,JSONDecodeError
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
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
        paginator = Paginator(image_data, 20)
        page_number = request.GET.get('page',1)
        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['image_data'] = image_data
        context['page'] = page
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
            image_data = ImageUpload.objects.all().values().order_by('-upload_date')
        paginator = Paginator(image_data, 20)
        page_number = request.POST.get('page')
        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context['image_data'] = image_data
        context['page'] = page
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
            'phone_no':phoneNo,
            'message':message,
            'template' : "customer_template.html"
        }
        
        try:
            if self.send_email_message(self,request,*args,**customer_mail_objects):
                admin_mail_objects= {}
                admin_mail_objects['template'] = "admin_template.html"
                admin_mail_objects['fullname'] = "Welcome to MyPicDocs! "
                admin_mail_objects['subject'] = f"Response from MyPicDocs {settings.EMAIL_HOST_USER}"
                admin_mail_objects['sender_mail'] = customer_mail_objects['reciever_mail']
                admin_mail_objects['reciever_mail'] = customer_mail_objects['sender_mail']
                admin_mail_objects['phone_no']=str(9304911556)
                admin_mail_objects['message'] ="Welcome to MyPicDocs! Our team has been connected with you as soon as possible with your enquiry.Thank you for choosing us. Enjoy your journey with us"
                if self.send_email_message(self,request,*args,**admin_mail_objects):
                    messages.success(request, 'Your message successfully send to site adminstration.')
                else:
                    messages.success(request, 'If you have not get any mail from MyPicDocs. Our member will be connect as soon as possible.')
            else:
                messages.error(request, 'Sometime internet issues or network issues try again.')
            return redirect('/')
        except:
            print("Mail sending errors")
            return redirect("/")
    def send_email_message(self,request,*args,**kwargs):
        template = get_template(kwargs['template'])
        context = kwargs
        email_content = template.render(context)
        email = EmailMessage(kwargs['subject'],email_content,kwargs['sender_mail'],[kwargs['reciever_mail']],reply_to=[kwargs['sender_mail']])
        email.content_subtype = 'html'
        return email.send()
