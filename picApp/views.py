from django.shortcuts import render
from .models import ImageUpload
from django.views import View
from os import getcwd
from json import load,JSONDecodeError
# Create your views here.
class Home(View):
    def get(self, request,*args,**kwargs):
        configs= read_json(getcwd()+"/picApp/configs.json")
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
        configs= read_json(getcwd()+"/picApp/configs.json")
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
