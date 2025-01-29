from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.db import IntegrityError
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view
from .models import Category
from .serializers import CategorySerializer
from django.core.paginator import Paginator, EmptyPage

@api_view(['GET', 'POST', 'DELETE'])
def category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        
        perpage = request.query_params.get('perpage', default=20)
        page = request.query_params.get('page', default=1)
        paginator = Paginator(categories,per_page=perpage)
        
        try:
            categories = paginator.page(number=page)
        except EmptyPage:
            categories = []
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data) 
    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            try:
                category_serializer.save()
                return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    
    # On récupère une categorie
    try:
        category = Category.objects.get(pk=pk)
        if request.method == 'GET':
            category_serializer = CategorySerializer(category)
            return Response(category_serializer.data)
        elif request.method == 'DELETE':
            category.delete()
            return Response({'message':'La catégorie a été supprimée!'}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            category_data = JSONParser().parse(request)
            category_serializer = CategorySerializer(category, data=category_data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(category_serializer.data)
    except Category.DoesNotExist:
        return Response({'message': 'categorie non trouvé'}, status=status.HTTP_404_NOT_FOUND)

