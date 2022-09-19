from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from haberler.models import Makale
from haberler.api.serializer import MakaleSerializer

from rest_framework.generics import _get_object_or_404


class MakaleListCreateAPIView(APIView):
    def get(self, request):
        makaleler = Makale.objects.filter(aktif=True)
        serializer = MakaleSerializer(makaleler, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailAPIView(APIView):
    def get_obj(self, pk):
        makale_instance = _get_object_or_404(Makale, pk=pk)
        return makale_instance

    def get(self, request, pk):
        makale = self.get_obj(pk=pk)
        serializer = MakaleSerializer(makale)
        return Response(serializer.data)

    def put(self, request, pk):
        makale = self.get_obj(pk=pk)
        serializer = MakaleSerializer(makale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        makale = self.get_obj(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
