import json
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core import serializers
from django.db import models
from django.urls import reverse


class AbstractHistory(models.Model):
    title = models.CharField(max_length=256, unique=True)
    text = models.TextField(blank=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    edited_on = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)
    history = GenericRelation('History')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        History.create_history(self) 


class History(models.Model):
    json_data = models.JSONField()
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = 'histories'
    
    def __str__(self):
       return self.json_data['fields']['title']

    def create_history(self):
        serialize = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk))
        json_data = json.loads(serialize)[0]
        History.objects.create(json_data=json_data, editor=self.editor, content_object=self)


class Article(AbstractHistory):
    msg = models.CharField(max_length=256, default='Created the article.')
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article-detail', kwargs={'title': self.title})


class Category(AbstractHistory):
    msg = models.CharField(max_length=256, default='Created the category.')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:category-detail', kwargs={'title': self.title})
