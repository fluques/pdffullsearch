from django.urls import path, include, re_path
from rest_framework import routers


from pdffullsearch_backend.views import UserViewSet, CategoryViewSet, PDFFileViewSet

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"category", CategoryViewSet)
router.register(r"pdffile", PDFFileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]