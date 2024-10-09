from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

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
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title

class KnowledgeBaseArticle(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    section = models.ForeignKey(KnowledgeBaseSection, on_delete=models.CASCADE, related_name='articles')
    attached_file = models.FileField(upload_to='knowledge_base/files/', blank=True, null=True)
    attached_image = models.ImageField(upload_to='knowledge_base/images/', blank=True, null=True)

    def __str__(self):
        return self.title