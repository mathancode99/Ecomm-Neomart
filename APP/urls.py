
from django.contrib import admin
from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   path('', sign_up ,name='signup'),
   path('sign_in', sign_in ,name='signin'),
   path('user_panel', user_panel,name='user_panel' ),
   path('admin_panel', admin_panel ),
   path('seller_panel', seller_panel ),
   path('seller_account',seller_account,name='seller_form'),
   path('seller_product',add_product,name='seller_panel'),
   path('delete/<pk>', delete_product, name='delete_product'),   
   path('update/<pk>', update_product, name='update_product'),
   path('search/', search_product, name='search'),
   path('category/', search_category, name='category'),
   path('checkout', checkout, name='checkout'),
   path('place_order', place_order, name='place_order'),
   path('order_success', order_success, name='order_success'),
   path('order_show', show_order, name='order_show'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)