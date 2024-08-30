from django.db import models
from django.utils.translation import gettext_lazy as _

class Clinic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PaymentType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Revenue(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, default=1)  # использование значения по умолчанию

    class Meta:
        unique_together = ('clinic', 'date', 'payment_type')

    def __str__(self):
        return f'{self.clinic.name} - {self.date} - {self.revenue} - {self.payment_type.type}'


class KnowledgeBaseSection(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.title

class KnowledgeBaseArticle(models.Model):
    section = models.ForeignKey(KnowledgeBaseSection, on_delete=models.CASCADE, related_name='articles', verbose_name=_("Section"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))

    def __str__(self):
        return self.title