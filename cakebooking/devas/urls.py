"""cakebooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
       path('',views.index, name="index"),
       path('index.html',views.index, name="index"),

       path('about.html',views.about, name="about"),
       path('cakedetails.html',views.cakedetails, name="cakedetails"),
       path('login',views.login, name="login"),
       path('Registration',views.Registration, name="Registration"),
       path('wedding',views.wedding),
       path('rating.html',views.review, name="rating"),
       path('userhome',views.userhome, name="userhome"),
       path('cake_detail_page', views.cake_detail_page, name="cake_detail_page"),
       path('addtocart', views.addtocart,name="addtocart"),
       path('mycart', views.mycart, name="mycart"),
       path('managecart/<int:id>/', views.managecart, name="managecart"),
       
       path('checkout', views.checkout),
       path('confirm_payment', views.confirm_payment),
       
       
    #    path('user_cake_details.html', views.user_cake_details, name="user_cake_details"),
       path('user_cake_detail_page',views.user_cake_detail_page, name="user_cake_detail_page"),
       path('user_cake_details', views.user_cake_details, name="user_details_page"), 
       path('logout',views.logout, name="logout"),
       path("checkout_session", views.checkout_session, name="checkout_session"),
       path('pay_success', views.pay_success, name="pay_success"),
       path('pay_cancel', views.pay_cancel, name="pay_cancel"),
       path('user_order_status', views.user_order_status),
       path('contact', views.contact, name="contact"),
       path('usercontact',views.usercontact, name="usercontact"),
]    

urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
