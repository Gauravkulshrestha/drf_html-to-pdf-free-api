from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Html_to_PDFSerializer
import http.client
import json

class HTML_to_PDFView(APIView):
    serializer_class = Html_to_PDFSerializer

    def post(self, request, format=None):
        serializer = Html_to_PDFSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            conn = http.client.HTTPSConnection("api.pdfmark.com")
            payload = json.dumps({
                "url": self.request.data.get('url'),
                "margin": "10mm",
                "page_size": "legal"
                })

            headers = {
            'key': 'YOUR_API_KEY',
            'Content-Type': 'application/json'
            }
            conn.request("POST", "/pdf", payload, headers)
            res = conn.getresponse()
            data = res.read()
            result = data.decode("utf-8")
            serializer.save()
        return Response(result)