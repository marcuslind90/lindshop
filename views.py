from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from lindshop.core.product.models import Product
from lindshop.core.category.models import Category
from lindshop.core.cart.models import CartItem
from lindshop.core.customer.models import Country
from lindshop.core.shipping.models import Carrier
from lindshop.core.order.models import Order
from lindshop.core.breadcrumbs.breadcrumbs import Breadcrumbs
from lindshop.core.payment.utils import payments

import mixins as mixins
from lindshop.core.checkout import process

# Class Based Views
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
# End Class Based Views

class HomeView(TemplateView):

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['products'] = Product.objects.all()
		return context

class CategoryList(mixins.BreadcrumbsMixin, ListView):
	context_object_name = "products"

	def get_queryset(self):
		# We call it self.object to keep things consistant with DetailView.
		# This means that we can use self.object in Mixins to refer to the main
		# instance of the page.
		self.object = get_object_or_404(Category, slug=self.kwargs['category_slug'])
		return Product.objects.filter(categories__in=[self.object])

	def get_context_data(self, **kwargs):
		context = super(CategoryList, self).get_context_data(**kwargs)
		context['category'] = self.object
		context['subcategories'] = Category.objects.filter(parent=self.object)
		return context

class ProductDetail(mixins.BreadcrumbsMixin, DetailView):
	model = Product
	context_object_name = "product"

	def get_context_data(self, **kwargs):
		return super(ProductDetail, self).get_context_data(**kwargs)

class CartSummary(TemplateView):
	"""Display a summary of the current user's cart items. The Cart context 
	is already added by our context_processor and therefore this can be a TemplateView.
	"""
	pass

class Checkout(TemplateView):

	def get_context_data(self, **kwargs):
		context = super(Checkout, self).get_context_data(**kwargs)
		default_country = Country.objects.get(default=True)
		context['carriers'] = Carrier.objects.filter(countries=default_country)
		context['countries'] = Country.objects.all()
		context['payments'] = payments
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data()

		# Put in any process of the checkout here...
		validate = process.validate_checkout(request)
		if validate is not True:
			context['errors'] = validate
			return super(Checkout, self).render_to_response(context)

		cart = process.get_cart(request)
		user = process.add_customer(request)
		address = process.add_address(request)

		order = Order(
			cart=cart, 
			user=user, 
			payment_option=request.POST.get("payment-option", None)
		)

		order.save()

		del request.session['id_cart']
		return HttpResponseRedirect(reverse('shop:thank_you'))


class ThankYou(TemplateView):
	pass