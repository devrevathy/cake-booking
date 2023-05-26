from django.db import models
import datetime
from datetime import *
from django.utils import timezone
# Create your models here.
class registration(models.Model):
    user_id = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    pin = models.IntegerField()
    email = models.CharField(max_length=40)
    passwd = models.CharField(max_length=40)
    confirmpasswd= models.CharField(max_length=40)
    
    
    def __str__(self):
        return self.fname

    
class cake_details(models.Model):
    
    
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=10000)
    caption = models.TextField(max_length=10000,null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    pic = models.ImageField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50) # cake by type, flavour,etc
    
    def __str__(self):
        return self.name


class revieww(models.Model):
    review_decp=models.CharField(max_length=50)
    # cake=models.ForeignKey(cake_details,on_delete=models.CASCADE)
    cake=models.CharField(max_length=50)
    user_id= models.ForeignKey(registration,on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    

    
class cake_type(models.Model):
    cake_id = models.ForeignKey(cake_details,on_delete=models.CASCADE)
    by_flavour = models.CharField(max_length=100)
    by_type = models.CharField(max_length=100)
    by_ocassion =  models.CharField(max_length=100)
    
class cart(models.Model):
    customer = models.ForeignKey(registration, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)

class CartProduct(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    cake = models.ForeignKey(cake_details, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "cart:" + str(self.cart.id) + "cartproduct:" + str(self.id)
    
   
ORDER_STATUS = (
    ("order processing", "order processing"),
    ("order on the way", "order confirm"),
    ("order completed", "order on the way"),
    ("order recived", "order recived"),
    ("order cancelled", "order cancelled")
)
class Orders(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(registration, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, default="ssss")
    mobile  = models.CharField(max_length=50, default="45678")



class cake_payment(models.Model):
    user_id = models.ForeignKey(registration,on_delete=models.CASCADE)
    cake_id = models.ForeignKey(cake_type,on_delete=models.CASCADE)
    amt = models.CharField(max_length=50)
    card_no = models.CharField(max_length=50)
    cvv  = models.IntegerField()
    status = models.CharField(max_length=50)
    
class cakeimages(models.Model):
    photo = models.ImageField(upload_to='photo', blank=True,null=True)
    description = models.CharField(max_length=300)
    


# class MyModelAdmin(admin.ModelAdmin):
#     def clean(self):
#         cleaned_data = super().clean()
#         time_field = cleaned_data.get('time_field')
#         if time_field:
#             # Validate that the time is between 9:00 AM and 5:00 PM
#             start_time = timezone.make_aware(timezone.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
#             end_time = timezone.make_aware(timezone.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0))
#             if not start_time <= time_field <= end_time:
#                 raise ValidationError('Time should be between 9:00 AM and 5:00 PM.')

# admin.site.register(MyModel, MyModelAdmin)

# class Contact(models.Models):
#     name=models
    
    
    
    
    