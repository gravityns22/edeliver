# accounts.models.py
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, username, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            date_of_birth=date_of_birth,

        )
        #user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, validators=[
        RegexValidator(regex= USERNAME_REGEX,
                       message = 'Username must be Alphanumeric or any of the following: ". @ + -"')],
                                unique=True

                                )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    date_of_birth = models.DateField()
    date_joined = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'date_of_birth'] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin


class APIService(models.Model):
    APIPROVIDER_CHOICES = (
        ('wordpress', 'Wordpress'),
        ('wocommerce', 'Woocommerce'),
        ('auspost', 'Australia Post'),
        ('fedex', 'FedEx'),
    )

    API_SERVICES_CHOICES = (
        ('wordpress_rest_api', 'Wordpress REST API'),
        ('wocommerce_rest_api', 'Woocommerce REST API'),
        ('auspost_pac', 'Australia Post - PAC API'),
        ('fedex', 'FedEx'),
    )

    api_provider = models.TextField(default='auspost', choices=APIPROVIDER_CHOICES)
    api_name = models.TextField(default='auspost_pac', choices=API_SERVICES_CHOICES)

    api_key = models.TextField(max_length=150)
    api_secret = models.TextField(max_length=150, default=None, help_text='Required for Wordpress & Woocommerce')

    api_is_publc = models.BooleanField(default=False)
    api_category = models.TextField(max_length=150)

    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return '{}\'s {} API Key {}'.format(self.user.username, self.api_provider.strip(), self.api_key.strip())
    def __unicode__(self):
        return '{}\'s {} API Key {}'.format(self.user.username, self.api_provider.strip(), self.api_key.strip())



    def round_currency(dec):
        """
        Correctly rounds the decimal value as per usual currency rules.
        e.g.: Decimal('12.9699999999') becomes Decimal('12.97')
        """
        return dec.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

class WareHouse(models.Model):
    warehouse_code = models.CharField(blank=False, max_length=50)
    default_warehouse_base = models.BooleanField(default=False)
    warehouse_slug = models.TextField(blank=False, max_length=250)
    address_line_1 = models.TextField(blank=False, max_length=250)
    #address_line_2 = models.TextField(blank=True)
    city = models.CharField(blank=False, max_length=250)

    state = models.CharField(blank=False, max_length=250)
    post_code = models.CharField(blank=False, max_length=250)
    country = models.CharField(blank=False, max_length=250)


    def __str__(self):
        return self.warehouse_code

    def formatted_address(self):
        return '{}, {}, {} {}, {}'.format(self.address_line_1, self.city, self.state, self.post_code, self.country)


class Product(models.Model):
    pid = models.TextField(blank=False)
    name = models.TextField()
    slug = models.TextField()
    permalink = models.TextField()
    date_created = models.TextField()
    date_created_gmt = models.TextField()
    date_modified = models.TextField()
    date_modified_gmt = models.TextField()
    type = models.TextField()
    status = models.TextField()
    featured = models.TextField()
    catalog_visibility = models.TextField()
    description = models.TextField()
    short_description = models.TextField()
    sku = models.TextField()
    price = models.TextField()
    regular_price = models.TextField()
    sale_price = models.TextField()
    date_on_sale_from = models.TextField()
    date_on_sale_from_gmt = models.TextField()
    date_on_sale_to = models.TextField()
    date_on_sale_to_gmt = models.TextField()
    price_html = models.TextField()
    on_sale = models.TextField()
    purchasable = models.TextField()
    total_sales = models.TextField()
    virtual = models.TextField()
    downloadable = models.TextField()
    downloads = models.TextField()
    download_limit = models.TextField()
    download_expiry = models.TextField()
    external_url = models.TextField()
    button_text = models.TextField()
    tax_status = models.TextField()
    tax_class = models.TextField()
    manage_stock = models.TextField()
    stock_quantity = models.TextField()
    stock_status = models.TextField()
    backorders = models.TextField()
    backorders_allowed = models.TextField()
    backordered = models.TextField()
    sold_individually = models.TextField()
    weight = models.TextField()
    dimensions = models.TextField()
    shipping_required = models.TextField()
    shipping_taxable = models.TextField()
    shipping_class = models.TextField()
    shipping_class_id = models.TextField()
    reviews_allowed = models.TextField()
    average_rating = models.TextField()
    rating_count = models.TextField()
    related_ids = models.TextField()
    upsell_ids = models.TextField()
    cross_sell_ids = models.TextField()
    parent_id = models.TextField()
    purchase_note = models.TextField()
    categories = models.TextField()
    tags = models.TextField()
    images = models.TextField()
    attributes = models.TextField()
    default_attributes = models.TextField()
    variations = models.TextField()
    grouped_products = models.TextField()
    menu_order = models.TextField()
    meta_data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    warehouse_id = models.ForeignKey(WareHouse, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{}:{}:{}:{}:{}'.format(self.id,self.name, self.price, self.stock_quantity,self.user)
