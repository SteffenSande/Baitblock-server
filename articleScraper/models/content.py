from django.db import models
from django.contrib import admin
from articleScraper.models.revision import Revision


class Content(models.Model):
    pos = models.IntegerField(default=-1)
    tag = models.TextField(default=None, null=True)
    content = models.TextField(default=None, null=True)
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)

    def __str__(self):
        result = "Position: " + str(self.pos) + '\tTag: ' + str(self.tag)
        return result

    @property
    def children(self):
        """
        Property to get all child nodes from the current node.
        :return: All child nodes that is contained in this node.
        """
        return self.child_set.all()


admin.site.register(Content)
