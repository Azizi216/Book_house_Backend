from django.db.models import Q

import cloudinary.uploader

from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Book
from .serializers import BookSerializer


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = Book.objects.all().order_by("title")

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search)
            )

        if category and category != "All":
            queryset = queryset.filter(category__iexact=category)

        return queryset

    def upload_to_cloudinary(self, file, folder):
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="auto"
        )

        return result.get("secure_url")

    def perform_create(self, serializer):
        cover_image = self.request.FILES.get("cover_image")
        pdf_file = self.request.FILES.get("pdf_file")

        extra_data = {}

        if cover_image:
            extra_data["cover_image_url"] = self.upload_to_cloudinary(
                cover_image,
                "book_house/covers"
            )

        if pdf_file:
            extra_data["pdf_url"] = self.upload_to_cloudinary(
                pdf_file,
                "book_house/pdfs"
            )

        serializer.save(**extra_data)

    def perform_update(self, serializer):
        cover_image = self.request.FILES.get("cover_image")
        pdf_file = self.request.FILES.get("pdf_file")

        extra_data = {}

        if cover_image:
            extra_data["cover_image_url"] = self.upload_to_cloudinary(
                cover_image,
                "book_house/covers"
            )

        if pdf_file:
            extra_data["pdf_url"] = self.upload_to_cloudinary(
                pdf_file,
                "book_house/pdfs"
            )

        serializer.save(**extra_data)