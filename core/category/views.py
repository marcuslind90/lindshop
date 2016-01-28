from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from lindshop.core.category.models import Category
from lindshop.core.breadcrumbs.breadcrumbs import Breadcrumbs

# Create your views here.
def category(request, category_slug):
	category = get_object_or_404(Category, slug=category_slug)

	breadcrumbs = Breadcrumbs()
	breadcrumbs.add_category(category, False)

	return render(request, "category/category-page.html", {'category': category, 'breadcrumbs': breadcrumbs.crumbs})