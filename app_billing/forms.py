from django.forms import ModelForm
from .models import Items, Purchase, Order, OrderLine
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class ItemCreateForm(ModelForm):
    class Meta:
        model = Items
        fields = '__all__'

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PurchaceCreateForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'items': forms.Select(attrs={'class': 'form-control'}),
            'purchase_qty': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'billnumber',
            'customer_name',
            'phone_number'
        ]
        widgets = {
            'billnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderLineCreateForm(forms.Form):
    bill_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_name = Purchase.objects.all().values_list('items__item_name')
    result = [(tp[0], tp[0] )for tp in product_name]
    product_name = forms.ChoiceField(choices=result)



class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','username','password1','password2',]


class LoginForm(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField()


class SearchForm(forms.Form):
    search = forms.CharField()