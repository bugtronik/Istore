from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import IntegrityError
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .models import Product
from django.core.paginator import Paginator, EmptyPage

@api_view(['GET', 'POST', 'DELETE'])
def product(request):
    if request.method == 'GET':
        products = Product.objects.all()
        
        perpage = request.query_params.get('perpage', default=20)
        page = request.query_params.get('page', default=1)
        paginator = Paginator(products,per_page=perpage)
        try:
            products = paginator.page(number=page)
        except EmptyPage:
            products = []
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data) 
    elif request.method == 'POST':
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            try:
                product_serializer.save()
                return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    
    # On récupère une categorie
    try:
        product = Product.objects.get(pk=pk)
        if request.method == 'GET':
            product_serializer = ProductSerializer(product)
            return Response(product_serializer.data)
        elif request.method == 'DELETE':
            product.delete()
            return Response({'message':'La catégorie a été supprimée!'}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            product_data = JSONParser().parse(request)
            product_serializer = ProductSerializer(product, data=product_data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data)
    except Product.DoesNotExist:
        return Response({'message': 'categorie non trouvé'}, status=status.HTTP_404_NOT_FOUND)