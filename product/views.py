from django.shortcuts import render
from django.views import View

'''
trzeba dodac forms do tworzenia produktu




'''
# Create your views here.
class MainView(View):
    def get(self,request):
        return render(request,'index.html')



class ProductView(View):
    def get(self,request):
        pass