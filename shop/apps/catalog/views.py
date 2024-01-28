from django.views.generic import DetailView, ListView, View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404

from .cart import Cart
from .models import (
    Product, Category, Review,
)


class CatalogListView(ListView):
    """Цей класс представлення відображає каталог для користувача"""
    template_name = 'catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):

        if self.kwargs.get('category'):
            return Product.objects.filter(category__category=self.kwargs['category']).order_by('id')

        return super(CatalogListView, self).get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class SearchView(ListView):
    """За допомогою цього класу можемо робити пошук певного товару"""

    template_name = 'catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):

        return list(set(Product.objects.filter(
            Q(name__icontains=self.request.GET['query']) |
            Q(description__icontains=self.request.GET['query']) |
            Q(brand__brand__icontains=self.request.GET['query']) |
            Q(category__category__icontains=self.request.GET['query'])
        )))

    def get_context_data(self, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

    def post(self, request):
        items = Product.objects.filter(name__icontains=request.POST['query']).values_list('name')
        return JsonResponse({'items': list(items)})



class ProductView(DetailView):

    template_name = 'catalog/toy_detail.html'
    context_object_name = 'toy'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['name'] = self.kwargs['name']

        return context

    def get_object(self):

        return get_object_or_404(Product, name=self.kwargs.get('name'))


class AjaxComment(View):

    template_name = 'catalog/toy_detail.html'

    @staticmethod
    def post(request, **kwargs):

        comment = request.POST['comment']

        toy = Product.objects.get(name=kwargs['name'])

        review = Review()
        review.comment = comment
        review.user = request.user
        review.review = toy
        review.save()

        return JsonResponse({'index': review.id})

    @staticmethod
    def put(request):

        data = QueryDict(request.body)
        comment = data['comment']
        index = data['index']
        Review.objects.filter(Q(pk=index) & Q(user=request.user)).update(comment=comment)

        return HttpResponse()

    @staticmethod
    def delete(request, **kwargs):

        data = QueryDict(request.body)
        index = data['index']
        Review.objects.filter(Q(pk=index) & Q(user=request.user)).delete()

        return HttpResponse()


class AjaxCart(View):
    """Цей класс представлення взаємодіє з кошиком за допомогою ajax запитів"""

    @staticmethod
    def post(request):
        return JsonResponse(Cart(request).add())

    @staticmethod
    def delete(request):
        Cart(request).delete()
        return JsonResponse({'cart_counter': len(Cart(request).display())})

    @staticmethod
    def put(request):
        return JsonResponse(Cart(request).put())
