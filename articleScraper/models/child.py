from django.db import models
from django.contrib import admin

from articleScraper.models import Content


class Child(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    child = models.IntegerField(default=-1, null=False)

    def __str__(self):
        result = 'content ' + str(self.content.id) + 'has a child at id: ' + str(self.child)
        return result


admin.site.register(Child)
