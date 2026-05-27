from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    # Image can be internet URL OR Cloudinary URL
    image_url = models.URLField(max_length=1000, blank=True, null=True)

    # PDF Cloudinary URL
    pdf_url = models.URLField(max_length=1000, blank=True, null=True)

    rating = models.FloatField(default=0)
    year = models.IntegerField()
    pages = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title