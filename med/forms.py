from .models import Product,Checkout,Cart, Categories
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q


class Product_form(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug']


class CheckoutForm(forms.ModelForm):
    user = forms.CharField(required=False)
#          fname = models.CharField(max_length=50)
#         # lname = models.CharField(max_length=50)
#         # email = models.EmailField(max_length=50)
#         # address = models.CharField(max_length=200)
#         # town = models.CharField(max_length=200)
#         # zip = models.CharField(max_length=10)
#         # phone = models.CharField(max_length=11)

    class Meta:
        model = Checkout
        fields = '__all__'


class UserLogin(forms.Form):
    query = forms.CharField(label='Username / Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError("Invalid credentials -- user not exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            # log auth tries
            raise forms.ValidationError("Invalid credentials -- password invalid")
        if not user_obj.is_active:
            raise forms.ValidationError("Inactive user. Please verify your email address.")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLogin, self).clean()


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter User Name'}
    ), required=True, max_length=20)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter Mail Id'}
    ), required=True, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=40)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match = User.objects.get(username=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError("User Name Already Exist")

    def clean_email(self):
        user = self.cleaned_data['email']
        try:
            User.objects.get(email=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError("Email Already Exist")

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["confirm_password"])
        user.is_active = False
        if commit:
            user.save()
        return user
