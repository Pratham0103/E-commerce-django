from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from .utils import code_generator
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail


class Categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="slug-slug")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    salt = models.TextField(default="salts")
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    image = models.ImageField(upload_to='picture', null=True, blank=True)

    slug = models.SlugField(default="Hey-d")

    def __str__(self):
        return "Title : "+self.title+",\tPrice : "+str(self.price)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class Checkout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.fname

    def save(self, *args, **kwargs):
        self.fname = self.fname.capitalize()
        self.lname = self.lname.capitalize()
        self.town = self.town.capitalize()
        self.city = self.city.capitalize()
        super(Checkout, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    in_cart = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title


class ActivationProfile(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL)
    key     = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)
    for_password = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("created")
        try:
            y = User.objects.get(username=instance)
            print(y.id)
            print(y.email)
            print(instance.key)
            print('activation created')
            print("for:", instance.for_password)
            if instance.for_password == False:
                print("in false")
                ins = ("Hello http://127.0.0.1:8000/med/activate/%s" % instance.key)
            else:
                print("in true")
                ins = ("Hello http://127.0.0.1:8000/med/change_password/%s" % instance.key)
            send_mail(
                'Confirmation',
                ins,
                settings.EMAIL_HOST_USER,
                [y.email, 'ishugoyal05@gmail.com', settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except:
            print("not WORTH")
    else:
        pass


post_save.connect(post_save_activation_receiver, sender=ActivationProfile)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            ActivationProfile.objects.create(user=instance)
        except:
            print("ERREOE")

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)