from django.views.generic import DetailView, ListView, View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.http import QueryDict

from rest_framework import generics

from .cart import Cart
from .serializers import *


class CatalogListView(ListView):
    template_name = 'catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return super(CatalogListView, self).get_queryset().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class AjaxCart(View):
    @staticmethod
    def post(request):
        return JsonResponse(Cart(request).post())

    @staticmethod
    def delete(request):
        Cart(request).delete()
        return JsonResponse({'cart_counter': len(Cart(request).display())})

    @staticmethod
    def put(request):
        return JsonResponse(Cart(request).put())


class SelectedCategoriesView(ListView):
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(category__category=self.kwargs['category']).order_by('id')

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        context = super(SelectedCategoriesView, self).get_context_data(**kwargs)
        context['categories'] = categories
        return context


class SearchView(ListView):
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
        return Product.objects.filter(name=self.kwargs['name'])


class AjaxComment(View):
    template_name = 'catalog/toy_detail.html'

    def post(self, request, **kwargs):
        review = Review()
        comment = request.POST['comment']
        toy = Product.objects.get(name=kwargs['name'])
        review.comment = comment
        review.user = request.user
        review.review = toy
        review.save()
        return JsonResponse({'index': review.id})

    def put(self, request):
        data = QueryDict(request.body)
        comment = data['comment']
        index = data['index']
        Review.objects.filter(Q(pk=index) & Q(user=request.user)).update(comment=comment)
        return HttpResponse()

    def delete(self, request):
        data = QueryDict(request.body)
        index = data['index']
        Review.objects.filter(Q(pk=index) & Q(user=request.user)).delete()
        return HttpResponse()


class ProductAPIList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'


class CategoryAPIList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandAPIList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class MaterialAPIList(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
