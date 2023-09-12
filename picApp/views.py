from django.shortcuts import render
from .models import ImageUpload
# Create your views here.

def home(request):
    context = {}
    if request.method == "POST":
        search_text = request.POST.get('search')
        if search_text is not None and search_text != "" :
            request.session['searchText'] = search_text
            context['image_data']   = ImageUpload.objects.filter(image_category__category=search_text).values()
        else:
            context['image_data'] = ImageUpload.objects.all().values()
    else:
        if(request.session.get('searchText')):
            context['image_data'] = ImageUpload.objects.filter(image_category__category=request.session.get('searchText')).values()
        else:
            context['image_data'] = ImageUpload.objects.all().values()
    return render(request,'index.html',context)
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def contact(request):
    return render(request,'contact.html')
