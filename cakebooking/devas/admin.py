from django.contrib import admin
from .models import*
from django import forms
# Register your models here.
admin.site.register(registration)
# admin.site.register(cake_details)
admin.site.register(cart)
admin.site.register(revieww)  
admin.site.register(cake_type)
admin.site.register(CartProduct)
admin.site.register(Orders)
# models ilulla page




class CakeDetailsAdminForm(forms.ModelForm):
    date = forms.DateField(widget=admin.widgets.AdminDateWidget())

    class Meta:
        model = cake_details
        fields = '__all__'


class CakeDetailsAdmin(admin.ModelAdmin):
    form = CakeDetailsAdminForm


admin.site.register(cake_details, CakeDetailsAdmin)
