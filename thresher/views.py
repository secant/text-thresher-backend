from django.contrib.auth.models import User
from django.core.paginator import Paginator

from rest_framework import routers, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status

from models import Article, SchemaTopic, HighlightGroup, Client
from serializers import (UserSerializer, ArticleSerializer, SchemaTopicSerializer, 
                         HighlightGroupSerializer, ClientSerializer)

# Views for serving the API

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class SchemaTopicViewSet(viewsets.ModelViewSet):
    queryset = SchemaTopic.objects.all()
    serializer_class = SchemaTopicSerializer

class HighlightGroupViewSet(viewsets.ModelViewSet):
    queryset = HighlightGroup.objects.all()
    serializer_class = HighlightGroupSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.DATA, list):
            serializer = HighlightGroupSerializer(data=request.DATA, many=True)
            if serializer.is_valid():
                self.object = serializer.save(force_insert=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return super(HighlightGroupViewSet, self).create(request, *args, **kwargs)

# Register our viewsets with the router
ROUTER = routers.DefaultRouter()
ROUTER.register(r'clients', ClientViewSet)
ROUTER.register(r'users', UserViewSet)
ROUTER.register(r'articles', ArticleViewSet)
ROUTER.register(r'schema_topics', SchemaTopicViewSet)
ROUTER.register(r'highlight_groups', HighlightGroupViewSet)
