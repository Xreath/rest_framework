from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from haberler.models import Makale
from haberler.api.serializer import MakaleDefaultSerializer


class MakaleListCreateAPIView(APIView):
    def get(self, request):
        makaleler = Makale.objects.filter(aktif=True)
        serializer = MakaleDefaultSerializer(makaleler, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MakaleDefaultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
