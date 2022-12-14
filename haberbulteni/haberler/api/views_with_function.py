from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from haberler.models import Makale
from haberler.api.serializer import MakaleDefaultSerializer


@api_view(['GET', 'POST'])
def makale_list_create_api_views(request):

    if request.method == 'GET':
        makaleler = Makale.objects.filter(aktif=True)
        serilazier = MakaleDefaultSerializer(makaleler, many=True)
        return Response(serilazier.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MakaleDefaultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def makale_detail_api_view(request, pk):
    try:
        makale_instance = Makale.objects.get(pk=pk)
    except Makale.DoesNotExist:
        return Response(
            {
                'errors': {
                    'status': True,
                    'message': f'Böyle bir id ({pk}) ile ilgili makale bulunamadı.'
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = MakaleDefaultSerializer(makale_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MakaleDefaultSerializer(
            makale_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        makale_instance.delete()
        return Response(
            {
                'işlem': {
                    'code': 204,
                    'message': f'({pk}) id numaralı makale silinmiştir.'
                }
            },
            status=status.HTTP_204_NO_CONTENT
        )
