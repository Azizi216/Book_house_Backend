from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    # Option 1: image from internet URL
    image_url = models.CharField(max_length=500, blank=True)

    # Option 2: image uploaded from computer
    image_file = models.ImageField(upload_to='books/images/', blank=True, null=True)

    # PDF uploaded from computer
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True)

    rating = models.FloatField(default=0)
    year = models.IntegerField()
    pages = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title