from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from lindshop.core.product.models import Product
# Create your views here.
def landing(request):
	products = Product.objects.all()
	return render(request, 'index.html', {'products': products})