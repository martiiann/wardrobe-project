"""
URL configuration for wardrobe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wardrobeapp import views
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wardrobeapp.urls')),
    path('shop/', include('products.urls')),
    path('shop/<str:gender>/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('orders/', include('orders.urls')),
    path('faq/', include(('faq.urls', 'faq'), namespace='faq')),
    path('stripe/webhook/', order_views.stripe_webhook, name='stripe_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # ✅ Custom 403 handler
handler403 = 'wardrobeapp.views.custom_permission_denied_view'

