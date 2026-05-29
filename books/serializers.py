from rest_framework import serializers
import cloudinary.uploader

from .models import Book


class BookSerializer(serializers.ModelSerializer):
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
        image_file = validated_data.pop("image_file", None)
        pdf_file = validated_data.pop("pdf_file", None)

        if image_file:
            uploaded_image = cloudinary.uploader.upload(
                image_file,
                folder="book_house/images",
                resource_type="image"
            )
            validated_data["image_url"] = uploaded_image["secure_url"]

        if pdf_file:
            uploaded_pdf = cloudinary.uploader.upload(
                pdf_file,
                folder="book_house/pdfs",
                resource_type="auto"
            )
            validated_data["pdf_url"] = uploaded_pdf["secure_url"]

        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image_file = validated_data.pop("image_file", None)
        pdf_file = validated_data.pop("pdf_file", None)

        if image_file:
            uploaded_image = cloudinary.uploader.upload(
                image_file,
                folder="book_house/images",
                resource_type="image"
            )
            instance.image_url = uploaded_image["secure_url"]

        if pdf_file:
            uploaded_pdf = cloudinary.uploader.upload(
                pdf_file,
                folder="book_house/pdfs",
                resource_type="auto"
            )
            instance.pdf_url = uploaded_pdf["secure_url"]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance