from django.shortcuts import render
from .models import ImageUpload
from django.views import View
# Create your views here.

class Home(View):
    def get(self, request,*args,**kwargs):
        context = {}
        if 'searchText' in request.session and (request.session['searchText'] !="" or request.session['searchText'] is None) :
            search_text = request.session.get('searchText')
            image_data  = ImageUpload.objects.filter(image_category__category=search_text).values()
        else:
            image_data = ImageUpload.objects.all().values()
        context['image_data'] = image_data
        return render(request, 'index.html', context)
    def post(self,request,*args,**kwargs):
        context = {}
        search_text = request.POST.get('search')
        if request.POST.get('btncancel') == 'cancel':
            search_text = ""
            del request.session['searchText']
        if(search_text !="" and search_text is not None):
            request.session['searchText'] = search_text
            image_data  = ImageUpload.objects.filter(image_category__category=search_text).values()
        else:
            request.session['searchText'] = search_text
            image_data = ImageUpload.objects.all().values()
        context['image_data'] = image_data
        return render(request,'index.html',context)
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def contact(request):
    return render(request,'contact.html')
