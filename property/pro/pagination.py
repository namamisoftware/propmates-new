from rest_framework.pagination import PageNumberPagination

class PropertyPagination(PageNumberPagination):
    page_size = 10               # 🔹 Default 10 records
    page_size_query_param = "page_size"   # 🔹 frontend se ?page_size=20
    max_page_size = 100          # 🔹 Max allowed
     