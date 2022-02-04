import json
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core import serializers
from django.db import models
from django.urls import reverse


class AbstractHistory(models.Model):
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    edited_on = models.DateTimeField()
    version = models.PositiveIntegerField(default=0)
    history = GenericRelation('History')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.edited_on = datetime.utcnow().isoformat()
        self.version += 1
        super().save(*args, **kwargs)

        return History.create_history(self)


class History(models.Model):
    json_data = models.JSONField()
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='editor')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = 'histories'

    def __str__(self):
        return self.json_data['fields'].get('title')

    @classmethod
    def create_history(cls, instance):
        """Serializes and saves an instance to the History."""
        serialize = serializers.serialize("json", instance.__class__.objects.filter(pk=instance.pk))
        json_data = json.loads(serialize)[0]
        cls.objects.create(json_data=json_data, editor=instance.editor, content_object=instance)


class Article(AbstractHistory):
    title = models.CharField(max_length=256, unique=True)
    text = models.TextField(blank=True)
    msg = models.CharField(max_length=256, default='Created the article.')
    category = models.ManyToManyField('Category', related_name='category')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:article-detail', kwargs={'title': self.title})


class Category(AbstractHistory):
    title = models.CharField(max_length=256, unique=True)
    text = models.TextField(blank=True)
    msg = models.CharField(max_length=256, default='Created the category.')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('wiki:category-detail', kwargs={'title': self.title})
