from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class ProductsListView(generics.GenericAPIView):
    # permission_classes = permissions.IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK,
            'message': 'Products List' if serializer.data else 'No data yet',
        })


class ProductCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'message': 'Product Created'
            }

        else:
            response = {
                'data': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data'
            }

        return Response(response)
    

class ProductUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'data': serializer.data,
                    'status': status.HTTP_200_OK,
                    'message': 'Product Updated'
                }
            else:
                response = {
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data'
                }
            return Response(response)
        
        except Exception as e:
            response = {
                'data': str(e),
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Product not found'
            }
            return Response(response)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'data': serializer.data,
                    'status': status.HTTP_200_OK,
                    'messages': 'Product Updated'
                }
            else:
                response = {
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid data'
                }
            return Response(response)
        
        except Exception as e:
            response = {
                'data': str(e),
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Product not found'
            }
            return Response(response)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            response = {
                'data': serializer.data,
                'status': status.HTTP_200_OK,
                'message': 'Product data'
            }
            return Response(response)
        
        except Exception as message:
                response = {
                    'data': str(message),
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Product not found'
                }
                return Response(response)


class ProductDeleteView(APIView):
    permission_classes = (permissions.AllowAny,)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            response = {
                'data': None,
                'status': status.HTTP_200_OK,
                'message': 'Product deleted'
            }
            return Response(response)

        except Exception as message:
            response = {
                'data': str(message),
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Product not found'
            }
            return Response(response)
    

# Viewsets orqali yozilgan view
class ProductsViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer