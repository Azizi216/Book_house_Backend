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

    def create(self, validated_data):
        validated_data.pop("image_file", None)
        validated_data.pop("pdf_file", None)
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("image_file", None)
        validated_data.pop("pdf_file", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance