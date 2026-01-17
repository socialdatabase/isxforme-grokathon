from django.db import models

# Create your models here.
class Search(models.Model):
    query = models.TextField()
    keywords = models.TextField()
    countries = models.TextField(null=True)
    query_type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.IntegerField(null=True)

    def __str__(self):
        return self.query
