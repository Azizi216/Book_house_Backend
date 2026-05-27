from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    # These are only for upload, not saved directly in the database
    image_file = serializers.FileField(write_only=True, required=False)
    pdf_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "category",
            "image_url",
            "pdf_url",
            "image_file",
            "pdf_file",
            "rating",
            "year",
            "pages",
            "description",
        ]