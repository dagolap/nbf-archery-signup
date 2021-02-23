import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

class ArcherClass(models.Model):
    code = models.CharField(_('Klassekode'), max_length=10)
    description = models.CharField(_('Klassenavn'), max_length=50)

    def __str__(self):
        return "%s - %s" % (self.code, self.description)

    class Meta:
        verbose_name = "Konkurranseklasse"
        verbose_name_plural = "Konkurranseklasser"

# Create your models here.
class Competition(models.Model):
    name = models.CharField(_('Navn'), null=False, max_length=100)
    host = models.CharField(_('Arrangør'), default=_('Norges Bueskytterforbund'), max_length=100)
    start_date = models.DateTimeField(_('Konkurransestart'), null=False)
    end_date = models.DateTimeField(_('Konkurranseslutt'), null=False)
    signup_deadline = models.DateTimeField(_('Påmeldingsfrist'), null=False)
    allowed_classes = models.ManyToManyField(to=ArcherClass, verbose_name=_('Tillate klasser'))

    def signup_count(self):
        return Signup.objects.filter(competition=self).count()
    signup_count.short_description = "Påmeldte"

    def __str__(self):
        return "%s" % self.name

    def get_absolute_url(self):
        return reverse("signups:competition", kwargs={"competition_id": self.pk})

    class Meta:
        verbose_name = "Konkurranse"
        verbose_name_plural = "Konkurranser"

class Signup(models.Model):
    id = models.UUIDField(_('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    archer_id = models.CharField(_('IANSEO-nummer'), max_length=10)
    competition = models.ForeignKey("signups.Competition", verbose_name=_("Konkurranse"), on_delete=models.CASCADE)
    name = models.CharField(_('Navn'), max_length=100)
    email = models.EmailField(_('E-post'), max_length=254)
    archer_class = models.ForeignKey("signups.ArcherClass", verbose_name=_("Konkurranseklasse"), on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (self.competition, self.archer_class, self.name)
    
    def get_score_submission_url(self):
        return reverse("signups:result_delivery", kwargs={"signup_id": self.id})

    class Meta:
        verbose_name = "Påmelding"
        verbose_name_plural = "Påmeldinger"

class ResultDelivery(models.Model):
    signup = models.ForeignKey("signups.Signup", verbose_name=_("Påmelding"), on_delete=models.CASCADE)
    scorecard = models.ImageField(_('Scorekort'), upload_to='uploads/scorecards/', null=False, blank=False)
    proof_image1 = models.ImageField(_('Bildebevis 1'), upload_to='uploads/proof_images/', null=False, blank=False)
    proof_image2 = models.ImageField(_('Bildebevis 2'), upload_to='uploads/proof_images/', null=True, blank=True)
    proof_image3 = models.ImageField(_('Bildebevis 3'), upload_to='uploads/proof_images/', null=True, blank=True)
    proof_image4 = models.ImageField(_('Bildebevis 4'), upload_to='uploads/proof_images/', null=True, blank=True)

    def __str__(self):
        return "%s - %s - %s" % (self.signup.competition.name, self.signup.name, self.result)

    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resultater"
