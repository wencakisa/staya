from django.urls import path, include

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('docs/', include_docs_urls(
        title='Staya API Docs',
        authentication_classes=[],
        permission_classes=[]
    )),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('', include('listings.urls')),
]
