from django.urls import path, include, re_path
from rest_framework import routers


from pdffullsearch_backend.views import UserViewSet, CategoryViewSet, PDFFileViewSet, FileUploadView

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"category", CategoryViewSet)
router.register(r"pdffile", PDFFileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("index", index, name="index"),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
]