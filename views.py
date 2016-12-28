from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from lindshop.core.product.models import Product
from lindshop.core.category.models import Category
from lindshop.core.cart.models import CartItem
from lindshop.core.breadcrumbs.breadcrumbs import Breadcrumbs

# Class Based Views
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
# End Class Based Views

class HomeView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['products'] = Product.objects.all()
		return context

class CategoryList(ListView):
	context_object_name = "products"
	template_name = "category/category-single.html"

	def get_queryset(self):
		self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
		return Product.objects.filter(categories__in=[self.category])

	def get_context_data(self, **kwargs):
		context = super(CategoryList, self).get_context_data(**kwargs)

		breadcrumbs = Breadcrumbs()
		breadcrumbs.add_category(self.category, False)

		context['breadcrumbs'] = breadcrumbs.crumbs
		context['category'] = self.category
		context['subcategories'] = Category.objects.filter(parent=self.category)

		return context

class ProductDetail(DetailView):
	model = Product
	context_object_name = "product"
	template_name = "product/product-single.html"

	def get_context_data(self, **kwargs):
		context = super(ProductDetail, self).get_context_data(**kwargs)

		breadcrumbs = Breadcrumbs()
		breadcrumbs.add_product(self.object, False)

		context['breadcrumbs'] = breadcrumbs.crumbs

		return context

class CartSummary(TemplateView):
	"""Display a summary of the current user's cart items. The Cart context 
	is already added by our context_processor and therefore this can be a TemplateView.
	"""
	template_name = "cart/summary.html"