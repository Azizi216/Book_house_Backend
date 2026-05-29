from rest_framework import serializers
import cloudinary.uploader

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    # These come from frontend FormData, but are not saved directly in DB
    image_file = serializers.FileField(write_only=True, required=False, allow_empty_file=False)
    pdf_file = serializers.FileField(write_only=True, required=False, allow_empty_file=False)

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

    def upload_image_to_cloudinary(self, image_file):
        if not image_file or image_file.size == 0:
            raise serializers.ValidationError({
                "image_file": "Image file is empty. Please choose a valid image."
            })

        try:
            image_file.seek(0)

            uploaded_image = cloudinary.uploader.upload(
                image_file,
                folder="book_house/images",
                resource_type="image",
            )

            image_url = uploaded_image.get("secure_url")

            if not image_url:
                raise serializers.ValidationError({
                    "image_file": "Cloudinary did not return an image URL."
                })

            return image_url

        except serializers.ValidationError:
            raise

        except Exception as e:
            raise serializers.ValidationError({
                "image_file": f"Image upload failed: {str(e)}"
            })

    def upload_pdf_to_cloudinary(self, pdf_file):
        if not pdf_file or pdf_file.size == 0:
            raise serializers.ValidationError({
                "pdf_file": "PDF file is empty. Please choose a valid PDF."
            })

        try:
            pdf_file.seek(0)

            uploaded_pdf = cloudinary.uploader.upload(
                pdf_file,
                folder="book_house/pdfs",
                resource_type="raw",
            )

            pdf_url = uploaded_pdf.get("secure_url")

            if not pdf_url:
                raise serializers.ValidationError({
                    "pdf_file": "Cloudinary did not return a PDF URL."
                })

            return pdf_url

        except serializers.ValidationError:
            raise

        except Exception as e:
            raise serializers.ValidationError({
                "pdf_file": f"PDF upload failed: {str(e)}"
            })

    def create(self, validated_data):
        image_file = validated_data.pop("image_file", None)
        pdf_file = validated_data.pop("pdf_file", None)

        if image_file:
            validated_data["image_url"] = self.upload_image_to_cloudinary(image_file)

        if pdf_file:
            validated_data["pdf_url"] = self.upload_pdf_to_cloudinary(pdf_file)

        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image_file = validated_data.pop("image_file", None)
        pdf_file = validated_data.pop("pdf_file", None)

        if image_file:
            instance.image_url = self.upload_image_to_cloudinary(image_file)

        if pdf_file:
            instance.pdf_url = self.upload_pdf_to_cloudinary(pdf_file)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance