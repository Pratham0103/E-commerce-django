from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import auth#login, get_user_model, logout
from .models import ActivationProfile
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='/med/login/')
def cart(request):
    carts = Cart.objects.filter(user=request.user, in_cart=True)
    list = []
    for i in carts:
        list.append(i.total_price)
        print(i.total_price)
    context = {
        "cart": carts,
        "sum": sum(list),
    }
    return render(request,'cart.html', context)


@login_required(login_url='/med/login/')
def add_cart(request, id):
    print(id, "\n\n\n")
    product = Product.objects.get(id=id)
    try:
        s = Cart.objects.get(product=product, user=request.user, in_cart=True)
        if s:
            s.quantity += 1
            s.total_price = float(product.price*s.quantity)
            s.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1, total_price=product.price)
    except:
        Cart.objects.create(user=request.user, product=product, quantity=1, total_price=product.price)
    return HttpResponseRedirect("/med/cart")


@login_required(login_url='/med/login/')
def del_cart(request, id):
    print(id, "\n\n\n")
    product = Product.objects.get(id=id)
    try:
        s = Cart.objects.get(product=product, user=request.user, in_cart=True)
        s.delete()
    except:
        return HttpResponseRedirect('/med/cart')
    return HttpResponseRedirect("/med/cart")


@login_required(login_url='/med/login/')
def sub_cart(request, id):
    print(id, "sub\n\n\n")
    product = Product.objects.get(id=id)
    try:
        s = Cart.objects.get(product=product, user=request.user, in_cart=True)
        if s:
            s.quantity -= 1
            s.total_price = float(product.price*s.quantity)
            s.save()
            if s.quantity == 0:
                s.delete()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1, total_price=product.price)
    except:
        Cart.objects.create(user=request.user, product=product, quantity=1, total_price=product.price)
    return HttpResponseRedirect("/med/cart")


def update_cart(request):
    carts = Cart.objects.filter(user=request.user, in_cart=True)
    for i in carts:
        i.in_cart = False
        i.save()
    return HttpResponseRedirect('/med/home/')


@login_required(login_url='/med/login/')
def add_product(request):
    user = request.user
    cat = Categories.objects.all()
    if user.id == 1:
        if request.method == 'POST':
            form = Product_form(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product Add Successfully")
                return HttpResponseRedirect('/med/add_product/')
            else:
                messages.error(request, "Invalid form")
        else:
            form = Product_form()

        return render(request, 'form.html', {"form": form, "cat": cat})
    else:
        return HttpResponseRedirect('/med/home/')


@login_required(login_url='/med/login/')
def edit_product(request, slug):
    user = request.user
    cat = Categories.objects.all()
    product = Product.objects.get(slug=slug)
    if user.id == 1:
        if request.method == 'POST':
            form = Product_form(request.POST, request.FILES)
            product.category.id = request.POST['category']
            product.title = request.POST['title']
            product.salt = request.POST['salt']
            product.description = request.POST['description']
            product.price = request.POST['price']
            try:
                product.image = request.FILES['image']
            except:
                pass
            try:
                product.save()
                messages.success(request, "Product Saved Successfully")
            except:
                messages.error(request, "Invalid")
            return HttpResponseRedirect('/med/add_product/')
        else:
            form = Product_form()

        return render(request, 'product_edit_form.html', {"form": form, "cat": cat, "product": product})
    else:
        return HttpResponseRedirect('/med/home/')


def search(request):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    if request.user.id == 1:
        boolean2 = 1
        print(boolean2)
    else:
        boolean2 = 2
    if request.method == 'POST':
        s = request.POST['sr']
        if s:

            match = Product.objects.filter(Q(title__icontains=s) |
                                           Q(description__icontains=s)|
                                           Q(salt__icontains=s))
            if match:
                categories = Categories.objects.all()
                return render(request, 'search.html', {"match": match,
                                                       'categories': categories,
                                                       "bool": boolean,
                                                       "bool2": boolean2})
            else:
                messages.error(request, "No Result Found")

        else:
            return HttpResponseRedirect('/med/home/')
    return render(request, 'search.html')


@login_required(login_url='/med/login/')
def account(request):
    user = request.user
    user = User.objects.get(username=user.username)
    order = Cart.objects.filter(user=request.user, in_cart=False)
    if request.method == 'POST':
        p1 = request.POST['password']
        p2 = request.POST['password2']
        if p1 == p2:
            # user.password = p1
            user.set_password(p1)
            user.save()
            messages.success(request, "Password Changed")
        else:
            messages.error(request, "Password doesnt match")
    context = {
        "user": user,
        "order": order,
    }

    return render(request, 'account.html', context)


def index(request):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    if request.user.id == 1:
        boolean2 = 1
    else:
        boolean2 = 2
    categories = Categories.objects.all()
    data = Product.objects.filter(category__name='Medicine')
    context = {
        'Data': data,
        'categories': categories,
        "bool": boolean,
        "bool2": boolean2
    }
    return render(request, 'index.html', context)


def index2(request, cat_name):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    if request.user.id == 1:
        boolean2 = 1
    else:
        boolean2 = 2
    cat = Categories.objects.all()
    all_items = Product.objects.filter(category__slug=cat_name)
    return render(request, 'index.html', {
        "categories": cat,
        "Data": all_items,
        "bool": boolean,
        "bool2": boolean2
    })


def shop(request):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    return render(request,'shop.html',{"bool": boolean})


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/med/home/')
    else:
        if request.method == 'POST':
            form = UserForm(request.POST or None)
            form_login = UserLogin(request.POST or None)
            if form.is_valid():
                print("asasasasdasas")
                form.save()
                print("asasasa")
                return HttpResponseRedirect("/")
            else:
                print("form invalid")
            if form_login.is_valid():
                user_obj = form_login.cleaned_data.get('user_obj')
                auth.login(request, user_obj)
                return HttpResponseRedirect("/med/home/")
        else:
            form = UserForm()
            form_login = UserLogin()
        return render(request, "login.html", {"form": form, "form2": form_login})


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/med/login/')


def product_details(request, name):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    item = Product.objects.get(slug=name)
    s = item.salt
    match = Product.objects.filter(Q(salt__contains=s))
    return render(request, 'product-details.html', {
        "Data": item,
        "match": match,
        "bool": boolean,
    })

def contact_us(request):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    return render(request,'contact-us.html',{"bool": boolean,})


@login_required(login_url='/med/login/')
def checkout(request):
    carts = Cart.objects.filter(user=request.user, in_cart=True)
    if carts:
        try:
            check = Checkout.objects.get(user=request.user)
            boolean = 1
        except:
            boolean = 0
            check = None
        if request.method == 'POST':
            form = CheckoutForm(request.POST or None)
            if form.is_valid():
                x = form.save(commit=False)
                x.user = User.objects.get(id=request.user.id)
                x.save()
                return HttpResponseRedirect('/med/checkout/')
        else:
            form = CheckoutForm()
        list = []
        for i in carts:
            list.append(i.total_price)
        context = {
            "sum": sum(list),
            "form": form,
            "cart": carts,
            "bool": boolean,
            "check": check
        }
        return render(request, 'checkout.html', context)
    else:
        return HttpResponseRedirect('/med/cart/')


@login_required(login_url='/med/login/')
def edit_checkout(request):
    try:
        check = Checkout.objects.get(user=request.user)
        if check:
            if request.method == 'POST':
                form = CheckoutForm(request.POST or None)
                if form.is_valid():
                    check.delete()
                    x = form.save(commit=False)
                    x.user = User.objects.get(id=request.user.id)
                    x.save()
                    return HttpResponseRedirect('/med/checkout/')
            else:
                form = CheckoutForm()
            context = {
                "form": form,
                "check": check
            }
            return render(request, 'edit_checkout.html', context)
    except:
        return HttpResponseRedirect('/med/checkout/')



def a(request):
    return render(request, '404.html')


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        act_profile_qs = ActivationProfile.objects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user_obj = act_obj.user
                user_obj.is_active = True
                user_obj.save()
                act_obj.expired = True
                act_obj.delete()
                return HttpResponseRedirect("/login")
    # invalid code
    return HttpResponseRedirect("/login")


def change_password(request, code=None):
    if code:
        act_profile_qs = ActivationProfile.objects.filter(key=code, for_password=True)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user = act_obj.user
                print("user:", user.username)
                if request.method == 'POST':
                    p1 = request.POST['password']
                    p2 = request.POST['password2']
                    if p1 == p2:
                        user.set_password(p1)
                        user.save()
                        act_obj.delete()
                        return HttpResponseRedirect("/med/login/")
                    else:
                        messages.error(request, "Password doesnt match")
                    return render(request, "reset_password.html", {"user": user})
                return render(request, "reset_password.html", {"user": user})
        else:
            return HttpResponseRedirect('/med/404/')
    return render(request, "reset_password.html")


def reset_password(request):
    if request.user.is_authenticated():
        boolean = 1
    else:
        boolean = 0
    if request.method == "POST":
        query = request.POST["query"]
        user_qs_final = User.objects.filter(
            Q(email__iexact=query)
        ).distinct()
        if user_qs_final.exists() and user_qs_final.count() == 1:
            user_obj = user_qs_final.first()
            ActivationProfile.objects.create(user=user_obj, for_password=True)
            messages.success(request, "Link to Reset sent")
        else:
            messages.error(request, "Wrong Email")
    return render(request, "get_email.html", {"bool": boolean})
