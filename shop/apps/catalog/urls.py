from django.urls import path, re_path

from apps.catalog import views


app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogListView.as_view(), name='main'),
    path('detail/ajax-comment/<name>', views.AjaxComment.as_view(), name='comment'),
    path('category/<category>', views.SelectedCategoriesView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('detail/<name>', views.ProductView.as_view(), name='toy'),
    path('orders/', views.AjaxCart.as_view()),
]
