from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from lindshop.core.product.models import Product
from lindshop.core.category.views import category
from lindshop.core.breadcrumbs.breadcrumbs import Breadcrumbs

def product(request, id_product, slug):
	product = get_object_or_404(Product, pk=id_product)

	breadcrumbs = Breadcrumbs()
	breadcrumbs.add_product(product, False)
	
	return render(request, "product/product-page.html", {'product': product, 'breadcrumbs': breadcrumbs.crumbs})