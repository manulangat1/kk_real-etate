from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _ 
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedModel



# Create your models here.

class Enquiry(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("Name")) 
    phone_number = PhoneNumberField(_("Phone Number") , max_length=30, default="+23456789089")
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))

    def __str__(self):
        return self.email 

    class Meta:
        verbose_name_plural = "Enquiries"

