from django.db import models
from django.utils.translation import gettext_lazy as _
from realestate.settings.base import AUTH_USER_MODEL
from apps.common.models import TimeStampedModel
from apps.profiles.models import Profile

# Create your models here.


class Range(models.IntegerChoices):
    RATING_1 = 1, _("Poor")
    RATING_2 = 2, _("Fair")
    RATING_3 = 3, _("Good")
    RATING_4 = 4, _("Very Good")
    RATING_5 = 5, _("Excellent")
class Rating(TimeStampedModel): 
    rater = models.ForeignKey(AUTH_USER_MODEL , verbose_name=_("User providing rating") , on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Profile , verbose_name=_("Agent being rated") , on_delete=models.SET_NULL, null=True, related_name="agent_review")
    rating = models.IntegerField(verbose_name=_("Rating"), choices=Range.choices, help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent", default=0)
    comment = models.TextField(verbose_name=_("Comment"), blank=True, null=True)

    class Meta: 
        unique_together = ['rater','agent']
    
    def __str__(self):
        return f"{self.rater} rated {self.agent} with {self.rating}"


    
    


