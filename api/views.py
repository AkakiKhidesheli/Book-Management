from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from core.models import Book
from .filters import BookFilter
from .serializers import BookSerializer


# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 20

@swagger_auto_schema(
    method='GET',
    operation_summary='Get Book Details',
    operation_description='This endpoint will return the Book Details',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('author', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('language', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('genre', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('shelf', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: BookSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Invalid Request',
        ),
    },
)
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all().order_by('id')

    filterset = BookFilter(request.query_params, queryset=books)

    if filterset.is_valid():
        books = filterset.qs

    # paginator = PageNumberPagination()
    paginator = CustomPagination()
    paginated_queryset = paginator.paginate_queryset(books, request)

    # serializer = BookSerializer(books, many=True)
    serializer = BookSerializer(paginated_queryset, many=True)


    result = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data,
    }



    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(result, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='POST',
    operation_summary='Add Book',
    operation_description='This endpoint will add a new Book',
    manual_parameters=[openapi.Parameter(
        'cover',
        openapi.IN_FORM,
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_FILE),
    )],
    request_body=BookSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Book Added',
            examples={
                'application/json': {'message': 'Book added successfully'},
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description='Invalid Request',
            examples={
                'application/json': {
                    'message': {
                        "title": ["This field is required."],
                        "author": ["This field is required."]
                    }
                }
            }
        )
    }
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book added successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': f'Book updated successfully', 'book': serializer.data},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
