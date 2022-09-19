
from django.urls import path
# from haberler.api import views_with_function as Api_Views
from haberler.api import views_with_class as API_Views_Class


urlpatterns = [
    path('makaleler/', API_Views_Class.MakaleListCreateAPIView.as_view(),
         name='makale-listesi'),
    path('makaleler/<int:pk>',
         API_Views_Class.MakaleDetailAPIView.as_view(), name='makale-detay'),
]
