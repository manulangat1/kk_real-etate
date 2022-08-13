import random 
import string
from tabnanny import verbose 
from django.db import models
from autoslug import AutoSlugField 

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedModel

User = get_user_model()

# Create your models here.

class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return super(PropertyPublishedManager, self).get_queryset().filter(
            is_published=True
        )


class Property(TimeStampedModel):
    class AdvertType(models.TextChoices):
        FOR_SALE="For Sale", _("For Sale")
        FOR_RENT="For Rent", _("For Rent")
        # FOR_LEASE="For Lease", _("For Lease")
        FOR_AUCTION="Auction", _("Auction")
    class PropertyType(models.TextChoices):
        APARTMENT="Apartment", _("Apartment")
        HOUSE="House", _("House")
        OFFICE="Office", _("Office")
        LAND="Land", _("Land")
        WAREHOUSE="Warehouse", _("Warehouse")
        COMMERCIAL="Commercial", _("Commercial")
        OTHER="Other", _("Other")

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_("Agent/Seller or Buyer/Buyer"), related_name="agent_buyer")
    title = models.CharField(verbose_name=_("Property Title"), max_length=180, blank=False, null=False)
    slug = AutoSlugField(populate_from="title", unique=True, verbose_name=_("Slug"), always_update=True)
    ref_code = models.CharField(verbose_name=_("Property Reference Code"), max_length=255, blank=True, null=True, unique=True)
    description = models.TextField(verbose_name=_("Property Description"), max_length=500, blank=True, null=True,default="Default Description ... update me please")
    country = CountryField(verbose_name=_("Country"), default="KE", blank_label="Select Country")
    city = models.CharField(verbose_name=_("City"), max_length=180, blank=False, null=False,default="Nairobi")
    postal_code = models.CharField(verbose_name=_("Postal Code"), max_length=100,default="12345")
    street_address = models.CharField(verbose_name=_("Street Address"), max_length=180,default="123 Main St")
    property_number = models.IntegerField(verbose_name=_("Property Number"), default=112,validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00)])
    tax = models.DecimalField(verbose_name=_("Property Tax"), max_digits=6, decimal_places=2, default=0.15, help_text="15% of the price" )
    plot_area = models.DecimalField(verbose_name=_("Plot Area(m2)"), max_digits=8, decimal_places=2, default=0.00)
    total_floors = models.IntegerField(verbose_name=_("Total Floors"), default=1,validators=[MinValueValidator(1)])
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.DecimalField(
        verbose_name=_("Bathrooms"), max_digits=4, decimal_places=2, default=1.0
    )
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )

    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    photo1 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax


class PropertyViews(TimeStampedModel):
    ip = models.CharField(
        verbose_name=_("IP Address"), max_length=255, blank=True, null=True
    )
    property = models.ForeignKey( 
        Property, on_delete=models.CASCADE, related_name="property_views"
    )

    def __str__(self):
        return f"Total views on - {self.property.title} is - {self.property.views} view(s)"

    class Meta:
        verbose_name = "Total views on property"
        verbose_name_plural = "Total views on properties"