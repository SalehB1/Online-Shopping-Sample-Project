from django.shortcuts import render
from itertools import product
from django.contrib import messages
from django.db.models.aggregates import Count
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Shop, Product
from order.models import Order
from .forms import CreateShopForm, CreateProductForm
from django.urls import reverse_lazy
from user.apiView import sample
# Create your views here.


class ShopDetail(LoginRequiredMixin, DetailView):
    template_name = 'shop/shopDetail.html'
    login_url = ''
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        context['product_list'] = Product.objects.filter(shop=context['shop']).order_by('id')
        context['order_list'] = Order.objects.filter(orderitem__product__shop__slug=self.kwargs['slug']).annotate(
            Count('id')).order_by('created_at')
        return context


class CreateShop(LoginRequiredMixin, CreateView, ContextMixin):
    template_name = 'shop/createShop.html'
    login_url = ''
    form_class = CreateShopForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        return context

    def post(self, request):
        not_confirmed = Shop.UnDeleted.filter(is_confirmed=False, seller=request.user).first()
        if not_confirmed:
            messages.info(request, "شما فروشگاه تأیید نشده دارید")
            return redirect('shopDetail', slug=not_confirmed.slug)
        form = CreateShopForm(request.POST)
        if form.is_valid():
            form.instance.seller = request.user
            form.save()
            shop = Shop.UnDeleted.filter(seller=request.user).last()
            messages.info(request, "فروشگاه شما ایجاد شد")
            return redirect('shopDetail', shop.slug)


class EditShop(LoginRequiredMixin, UpdateView):
    template_name = 'shop/editShop.html'
    login_url = ''
    model = Shop
    form_class = CreateShopForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        return context

    def get_success_url(self):
        slug = self.kwargs["slug"]
        return reverse("shopDetail", kwargs={"slug": slug})

    def post(self, request, *args, **kwargs):
        shop = Shop.UnDeleted.filter(slug=self.kwargs['slug'])
        shop.update(is_confirmed=False)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


# python3 -m pip install virtualenv

class DeleteShop(LoginRequiredMixin, UpdateView):
    login_url = ''
    model = Shop

    def get(self, request, *args, **kwargs):
        shop = Shop.UnDeleted.filter(slug=self.kwargs['slug'])
        shop.update(is_deleted=True, is_confirmed=False)
        shop = Shop.UnDeleted.filter(seller=self.request.user).first()
        messages.info(request, "فروشگاه رو حذف کردید")
        if shop:
            return redirect('shopDetail', slug=shop.slug)
        return redirect('createShop')


class CreateProduct(LoginRequiredMixin, CreateView, ContextMixin):
    template_name = 'product/createProduct.html'
    login_url = ''
    form_class = CreateProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        return context

    def post(self, request, *args, **kwargs):
        form = CreateProductForm(request.POST, request.FILES)
        form.instance.shop = Shop.UnDeleted.get(slug=self.kwargs['slug'])
        if form.is_valid():
            form.save()

            messages.success(request, "محصول شما ساخته شد")
            return redirect("shopDetail", self.kwargs["slug"])

        messages.info(request, "لطفا همه فیلد ها رو پر کنید")
        return redirect("createProduct", self.kwargs["slug"])

    # def get_success_url(self):
    #     return reverse('shopDetail', kwargs={'slug': self.UnDeleted.slug})


class EditProduct(LoginRequiredMixin, UpdateView):
    """
        editiing the product
    """
    model = Product
    form_class = CreateProductForm
    template_name = "product/editProduct.html"
    success_url = reverse_lazy('sellerLogin')

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=self.kwargs['slug'])
        product.update(is_confirmed=False)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
