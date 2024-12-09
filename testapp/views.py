from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def fake_endpoint(_):
    test_data = {"hello": "igl"}
    return Response(test_data)

