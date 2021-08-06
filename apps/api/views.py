from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import NewsPostSerializer
from news.models import NewsPost
from news.helpers import parse_search_terms


class NewsPostApi(APIView):
    def get(self, request, *args, **kwargs):
        selected_topics, text_search_value = parse_search_terms(request.GET)
        newsposts = NewsPost.search(topics=selected_topics, text_value=text_search_value)
        serializer = NewsPostSerializer(instance=newsposts, many=True)
        response = serializer.data
        return Response(response)
