from rest_framework.views import APIView
from .serializers import Html_to_PDFSerializer
from django.http import HttpResponse
import http.client
import json
import requests

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
            results = data.decode("utf-8")
            data = results.lstrip("'{\"pdf\":\'").rstrip("\"}")
            responses = requests.get(data)
            response = HttpResponse(responses,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            with open('report.pdf', 'wb') as f:
                f.write(responses.content)
            serializer.save()
        return response