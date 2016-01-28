from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from lindshop.core.product.models import Product
# Create your views here.
def landing(request):
	products = Product.objects.all()
	return render(request, 'index.html', {'products': products})

def terms(request):
	return render(request, 'lindshop/terms.html')

def contact(request):
	return render(request, 'lindshop/contact.html')

def faq(request):
	return render(request, 'lindshop/faq.html')