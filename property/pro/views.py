from django.contrib.auth.models import User  
from django.db import connection
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  

from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.core.mail import send_mail

from .models import *  
from django.shortcuts import get_object_or_404 
from django.contrib.admin import ModelAdmin
from rest_framework.generics import ListAPIView
from .utils import get_logged_in_user


# class EmailCheckView(APIView):  
#     def post(self, request):
#         serializer = EmailCheckSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
            
#             if CustomUser.objects.filter(email=email).exists():
#                 # User already exists
#                 return Response(
#                     {"message": "User exists, please enter password", "email": email, "status": "login"},
#                     status=status.HTTP_200_OK
#                 )
#             else:
#                 # New user
#                 return Response(
#                     {"message": "New user, please create password", "email": email, "status": "register"},
#                     status=status.HTTP_200_OK
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # -----------------------
# # Registration & OTP
# # -----------------------
# class RegisterView(APIView):
#     def post(self, request):
#         phone = request.data.get('phone')
#         if regesteruser.objects.filter(phone=phone).exists():
#             return Response({"error": "Phone number already registered"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "OTP sent to your phone"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OTPVerifyView(APIView):  
#     def post(self, request):
#         serializer = OTPVerifySerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # set session after registration
#             request.session['user_id'] = user.id
#             request.session.modified = True
#             return Response({"message": "User registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # -----------------------
# # Login & OTP Verify
# # -----------------------
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Login OTP sent to your phone"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginOTPVerifyView(APIView):
#     def post(self, request):
#         serializer = LoginOTPVerifySerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()  # this returns the regesteruser instance
#             request.session['user_id'] = user.id
#             request.session.modified = True
#             return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     def post(self, request):
#         request.session.flush()
#         return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# -----------------------
# Property CRUD
# -----------------------
class PropertyCreateView(APIView):
    def post(self, request):
       
        serializer = PropertySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            property_obj = serializer.save()

            # Handle optional images
            images = request.FILES.getlist('images') if 'images' in request.FILES else []
            for img in images:
                PropertyImage.objects.create(property=property_obj, image=img)

            # Handle optional payment plans
            plan_names = request.data.getlist('payment_name[]') if 'payment_name[]' in request.data else []
            plan_amounts = request.data.getlist('payment_amount[]') if 'payment_amount[]' in request.data else []
            for name, amount in zip(plan_names, plan_amounts):
                if name and amount:
                    UserPaymentPlan.objects.create(property=property_obj, payment_name=name, payment_amount=amount)

            return Response({"message": "Property added successfully", "property_id": property_obj.id}, status=201)
        return Response(serializer.errors, status=400)


class PropertyUpdateView(APIView):
    def put(self, request, pk):
     
        property_obj = get_object_or_404(UserProperty, pk=pk)
        serializer = PropertySerializer(property_obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            property_obj = serializer.save()

            # Optional images
            images = request.FILES.getlist('images') if 'images' in request.FILES else []
            for img in images:
                PropertyImage.objects.create(property=property_obj, image=img)

            # Optional payment plans
            plan_names = request.data.getlist('payment_name[]') if 'payment_name[]' in request.data else []
            plan_amounts = request.data.getlist('payment_amount[]') if 'payment_amount[]' in request.data else []
            if plan_names and plan_amounts:
                UserPaymentPlan.objects.filter(property=property_obj).delete()
                for name, amount in zip(plan_names, plan_amounts):
                    if name and amount:
                        UserPaymentPlan.objects.create(property=property_obj, payment_name=name, payment_amount=amount)

            return Response({"message": "Property updated successfully", "property_id": property_obj.id}, status=200)
        return Response(serializer.errors, status=400)


class PropertyListView(APIView):
    def get(self, request,user):
       

        properties = UserProperty.objects.filter(user=user)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=200)


class PropertyDeleteView(APIView):
    def delete(self, request, pk):
        
       
        property_obj = get_object_or_404(UserProperty, pk=pk)
        property_obj.delete()
        return Response({"message": "Property deleted successfully"}, status=200)



# -----------------------
# User Profile (GET & UPDATE)
# -----------------------
# class UserProfileView(APIView):
  
#     def get(self, request,pk):
       

#         serializer = UserProfileSerializer(pk)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request,pk):
       

#         serializer = UserProfileSerializer(
#             pk, 
#             data=request.data, 
#             partial=True, 
#             context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Profile updated successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyStepView(APIView):
    def post(self, request, step):
        data = request.data.copy()
        data["user"] = request.user.id  

        # Agar naye property create karna hai
        if step == "basic":
            serializer = PropertySerializer(data=data)
            if serializer.is_valid():
                property_obj = serializer.save()
                return Response({"message": "Step 1 completed", "property_id": property_obj.id}, status=201)
            return Response(serializer.errors, status=400)

        # Agar existing property ko update karna hai
        property_id = request.data.get("property_id")
        if not property_id:
            return Response({"error": "property_id required"}, status=400)

        try:
            property_obj = UserProperty.objects.get(id=property_id, user=request.user)
        except UserProperty.DoesNotExist:
            return Response({"error": "Property not found"}, status=404)

        serializer = PropertySerializer(property_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Step {step} saved", "property_id": property_id}, status=200)
        return Response(serializer.errors, status=400)


# # Get Property Details
# class PropertyDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             property_obj = UserProperty.objects.get(pk=pk)
#         except Property.DoesNotExist:
#             return Response({"error": "Property not found"}, status=404)

#         serializer = PropertySerializer(property_obj)
#         return Response(serializer.data, status=200)
    



# class PropertyFullDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             property_obj = UserProperty.objects.filter(   
#                 pk=pk,
#                 status=1
#             ).filter(
#                 Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
#             ).first()
            
#             if not property_obj:
#                 raise UserProperty.DoesNotExist
                
#         except UserProperty.DoesNotExist:
#             return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = PropertyDetailSerializer(property_obj)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class AllPropertiesView(APIView):
    def get(self, request):
        properties = UserProperty.objects.filter(
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyByCountryView(APIView):
    def get(self, request, country_id):
        properties = UserProperty.objects.filter(
            country_id=country_id,
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyByTypeView(APIView):
    def get(self, request, looking_to):
        properties = UserProperty.objects.filter(
            looking_to=looking_to,
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
class PropertyByPropertyTypeView(APIView):
    def get(self, request, property_type_id):
        properties = UserProperty.objects.filter(
            property_type_id=property_type_id,
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyByCommercialView(APIView):
    def get(self, request):
        properties = UserProperty.objects.filter(
            status=1
        ).filter(
            Q(looking_to=3) | Q(looking_to=4)
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyByAgentView(APIView):
    def get(self, request, agent_id):
        properties = UserProperty.objects.filter(
            agent_id=agent_id,
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyByCompanyView(APIView):
    def get(self, request, company_id):
        properties = UserProperty.objects.filter(
            company_id=company_id,
            status=1
        ).filter(
            Q(expire_at__isnull=True) | Q(expire_at__gte=timezone.now())
        )
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# ✅ All Countries
# class CountryListView(APIView):
#     def get(self, request):
#         countries = Country.objects.all()
#         serializer = CountrySerializer(countries, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# # ✅ All Sliders
# class SliderListView(APIView):
#     def get(self, request):
#         sliders = Slider.objects.all()
#         serializer = SliderSerializer(sliders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    # ✅ All Agents
class AgentListView(APIView):   
    # GET all agents
    def get(self, request):
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST create a new agent
    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT update an existing agent (requires pk)
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Agent ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        agent = get_object_or_404(Agent, pk=pk)
        serializer = AgentSerializer(agent, data=request.data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE remove an agent by ID
    def delete(self, request, pk=None):   
        if not pk:
            return Response({"error": "Agent ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        agent = get_object_or_404(Agent, pk=pk)
        agent.delete()
        return Response({"message": "Agent deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
    
    
    
    
# class CompanyListView(APIView):
#     def get(self, request):
#         companies = RealEstateCompany.objects.all()
#         serializer = CompanySerializer(companies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class CompanyById(APIView):
#     def get(self, request, company_id):
#         company = RealEstateCompany.objects.filter(id=company_id)
#         serializer = CompanySerializer(company, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class PropertyTypeById(APIView):
#     def get(self, request, property_type_id):
#         property_type = PropertyType.objects.filter(id=property_type_id)
#         serializer = PropertyTypeSerializer(property_type, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
# class PropertyTypeByLookingTo(APIView):
#     def get(self, request, looking_to):
#         property_type = PropertyType.objects.filter(looking_to=looking_to)
#         serializer = PropertyTypeSerializer(property_type, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
# class CountryById(APIView):
#     def get(self, request, country_id):
#         country = Country.objects.filter(id=country_id)
#         serializer = CountrySerializer(country, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class AmenityById(APIView):
    def get(self, request, amenity_id):
        amenity = Amenity.objects.filter(id=amenity_id)
        serializer = AmenitySerializer(amenity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PropertyAmenityList(APIView):
    def get(self, request, property_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, property_id, amenity_id FROM pro_property_amenities where property_id=%s", [property_id])
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            data = [
                {"id": row[0], "property_id": row[1], "amenity_id": row[2]}
                for row in rows
            ]
        return Response(data)
# class BlogListView(APIView):
#     def get(self, request):
#         blogs = Blogs.objects.all()
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class TestimonialListView(APIView):
#     def get(self, request):
#         testimonials = Testimonial.objects.all()
#         serializer = TestimonialSerializer(testimonials, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK) 
   
   






# Just for Cheking
  
from django.shortcuts import render, redirect, HttpResponse  
def chack(request):
    return render(request, 'dashboard/Propmatez_main.html') 


# For Update Agent Status
from django.shortcuts import render, get_object_or_404
from .models import Agent
from django.http import JsonResponse
from .models import Agent
import json

def update_status(request, agent_id):   
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")

            agent = Agent.objects.get(id=agent_id)
            agent.status = new_status
            agent.save()

            return JsonResponse({"success": True, "status": new_status})
        except Agent.DoesNotExist:
            return JsonResponse({"success": False, "error": "Agent not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})   



# Fro Update Status Normal User --------------------  
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404  

@csrf_exempt
def update_member_status(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        new_status = data.get("status")

        member = get_object_or_404(regesteruser, id=pk)  

        # ✅ Update status
        member.status = new_status

        # ✅ Auto-update is_verified based on status
        if new_status == "Active":
            member.is_verified = True
        else:
            member.is_verified = False

        member.save()

        return JsonResponse({
            "success": True,
            "status": member.status,
            "is_verified": member.is_verified,
        })

    return JsonResponse({"success": False}, status=400)  

  
#  Agent_Details  

 

  




#
#  views.py  
# from django.http import JsonResponse  
# import requests  
# from django.conf import settings

# GEOAPIFY_API_URL = "https://api.geoapify.com/v1/geocode/autocomplete"     
# GEOAPIFY_API_KEY = '7cb4a231b8d7445e817a708878a5a5cc'  # aap settings.py me define kar lo

# def search_location(request):
#     query = request.GET.get('q', '').strip()
#     if len(query) < 2:
#         return JsonResponse({"countries": [], "cities": [], "locations": []})

#     params = {
#         "text": query,
#         "format": "json",
#         "apiKey": GEOAPIFY_API_KEY,
#         # optionally restrict to India:
#         "filter": "countrycode:in",
#         "limit": 10
#     }

#     try:
#         resp = requests.get(GEOAPIFY_API_URL, params=params, timeout=5)
#         resp.raise_for_status()
        
#          # 👇 Debug prints
#         # print("Query:", query)
#         print("Geoapify response:", resp.json())          
        
#     except Exception as e:
#         # error handling
#         return JsonResponse({"countries": [], "cities": [], "locations": []})

#     data = resp.json().get("results", [])
#     print(data)  
#     # Now map results into your frontend structure
#     countries = []
#     cities = []
#     locations = []
#     for item in data:
#         prop = item.get("properties", {})
#         country = prop.get("country")
#         city = prop.get("city")
#         formatted = prop.get("formatted")

#         # If it is a country-level result (no city)
#         if city is None and country:
#             countries.append({"name": country})
#         # If city present
#         if city:
#             cities.append({"name": city, "country": country})
#         # Use the full formatted address as "location"
#         if formatted:
#             locations.append({"name": formatted, "city": city or ""})
#     print(cities)        
#     return JsonResponse({
#         "countries": countries,
#         "cities": cities,
#         "locations": locations
#     })    



def update_P_status(request, id):         
    if request.method == "POST":
        data = json.loads(request.body)

        status = data.get("status")
        model = data.get("model")   # <- yahi add kar rahe

        if model == "commercial":
            obj = CommercialProperty.objects.get(id=id)

        elif model == "residential":
            obj = ResidentialProperty.objects.get(id=id)

        else:
            return JsonResponse({"success": False, "error": "Invalid model"})

        obj.status = status
        obj.save()

        return JsonResponse({
            "success": True,
            "status": obj.status,
            "is_verified": obj.is_verified
        })
        
def update_PP_status(request, id):
    if request.method == "POST":
        data = json.loads(request.body)

        status = data.get("status")
        model = data.get("model")
     
        # Model mapper
        MODEL_MAP = {
             
            "pg": PGProperty,
            "agricultural": AgricultureProperty,     
            "business": BusinessForSale,
            "holiday": HolidayProperty,
        }

        # Invalid model check
        if model not in MODEL_MAP:
            return JsonResponse({"success": False, "error": "Invalid model type"})

        ModelClass = MODEL_MAP[model]

        try:
            obj = ModelClass.objects.get(id=id)
        except ModelClass.DoesNotExist:
            return JsonResponse({"success": False, "error": "Property not found"})

        # Update Status
        obj.status = status
        obj.save()

        return JsonResponse({
            "success": True,
            "status": obj.status,
            "is_verified": getattr(obj, "is_verified", False)
        })


















from django.http import JsonResponse  

from django.views.decorators.csrf import csrf_exempt
# from property.property.pro.models import UserProperty   # 👈 apne model ka naam yaha likho
import requests

GEOAPIFY_API_URL = "https://api.geoapify.com/v1/geocode/autocomplete"
GEOAPIFY_API_KEY = "7cb4a231b8d7445e817a708878a5a5cc"

def search_location(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"results": []})

    params = {
        "text": query,
        "apiKey": GEOAPIFY_API_KEY,
        "filter": "countrycode:in",
        "limit": 10,
        "lang": "en"  # 👈 add this for consistent results
    }

    try:
        resp = requests.get(GEOAPIFY_API_URL, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # print("RAW JSON:", data)  # 👈 print full JSON to inspect
    except Exception as e:
        # print("Geoapify error:", e)   
        return JsonResponse({"results": []})

    features = data.get("features", [])
    # print("FEATURE COUNT:", len(features))

    suggestions = []
    for item in features:
        prop = item.get("properties", {})
        formatted = prop.get("formatted")
        city = prop.get("city")
        country = prop.get("country")

        if formatted:
            suggestions.append({
                "label": formatted,
                "city": city or "",
                "country": country or ""
            })

   
    return JsonResponse({"results": suggestions})  



# @csrf_exempt
# def filter_properties(request):
#     """Filter property data by city or location"""
#     city = request.GET.get("city", "").strip()  
#     if not city:
#         return JsonResponse({"results": []})

#     # Example property filtering (adjust field names according to your model)
#     # Suppose your model has fields: title, address, city, price
#     properties = UserProperty.objects.filter(city__icontains=city)[:20]  

#     results = []
#     for prop in properties:
#         results.append({
#             "id": prop.id,
#             "title": prop.title,
#             "address": prop.address,
#             "price": prop.price,
#         })

#     return JsonResponse({"results": results})   

# Auto Location   fetch  
import requests
from django.http import JsonResponse

def reverse_location(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")  

    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    data = requests.get(url, headers={'User-Agent': 'YourApp'}).json()

    return JsonResponse({
        "label": data.get("display_name", ""),
        "city": data.get("address", {}).get("city", ""),
        "country": data.get("address", {}).get("country", "")
    })
    
    
from django.http import JsonResponse
from .models import UserProperty
from django.db.models import Q

def filter_by_location(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse({"results": []})

    try:
        results = UserProperty.objects.filter(
            Q(city__icontains=q) |
            Q(locality__icontains=q) |
            Q(sub_locality__icontains=q) |
            Q(address__icontains=q) |
            Q(apartment_name__icontains=q)  
        )

        data = []
        for r in results:
              # ✅ Safe agent field detection
            agent_name = (
                getattr(r.agent, "name", None) or
                getattr(r.agent, "full_name", None) or
                getattr(r.agent, "agent_name", None) or
                "No Agent"
            )
            data.append({
                "name": r.name or "",
                "address": r.address or "",
                       
                "location": f"{r.locality}, {r.city}",       
                "image": r.image2.url if r.image2 else "",    
                "agent": agent_name,  
                   
            })

        return JsonResponse({"results": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





from django.http import JsonResponse
from .models import Agent, CustomUser, RoleModel  

def verify_agent(request, agent_id):  
    agent = Agent.objects.get(id=agent_id)

    role_id = request.GET.get("role_id")
    if not role_id:
        return JsonResponse({"error": "Role ID missing"}, status=400)

    role = RoleModel.objects.get(id=role_id)

    user = CustomUser.objects.create_user(
        email=agent.email,
        full_name=agent.name,
        phone=agent.phone,
        password=agent.password,  # password hashing handled by create_user()
    )

    user.role_id = role   # ✅ role assign      
    user.save()

    agent.user = user     # ✅ link agent with new user
    agent.save()

    return JsonResponse({"success": True})





#   updated serializer  kr  liye Views Logics ----------------------------.................add()



from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q

from .models import *
from .serializers import PropertySerializer


@api_view(["GET"])
def property_list_api(request):    
    # -------------------------
    # Query Params
    # -------------------------
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    subtype = request.GET.get("subtype", "").strip()
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    address = request.GET.get("address", "").strip()
    sort = request.GET.get("sort", "")  # id, -id, price, -price etc.

    # -------------------------
    # Base Querysets
    # -------------------------
    commercial = CommercialProperty.objects.all()
    residential = ResidentialProperty.objects.all()

    # -------------------------
    # Search Filter
    # -------------------------
    if q:
        commercial = commercial.filter(
            Q(title__icontains=q) |
            Q(subtype__icontains=q)
        )
        residential = residential.filter(
            Q(title__icontains=q) |
            Q(subtype__icontains=q)
        )

    # -------------------------
    # Category Filter
    # -------------------------
    if category:
        commercial = commercial.filter(category__iexact=category)
        residential = residential.filter(category__iexact=category)

    # -------------------------
    # Subtype Filter
    # -------------------------
    if subtype:
        commercial = commercial.filter(subtype__iexact=subtype)
        residential = residential.filter(subtype__iexact=subtype)

    # -------------------------
    # Price Filter
    # -------------------------
    if min_price:
        commercial = commercial.filter(price__gte=min_price)
        residential = residential.filter(price__gte=min_price)

    if max_price:
        commercial = commercial.filter(price__lte=max_price)
        residential = residential.filter(price__lte=max_price)

    # -------------------------
    # Address Filter
    # -------------------------
    if address:
        commercial = commercial.filter(
            Q(location__icontains=address) |
            Q(map_address__icontains=address) |
            Q(address__icontains=address) |
            Q(city__icontains=address) |
            Q(area__icontains=address)
        )

        residential = residential.filter(
            Q(location__icontains=address) |
            Q(map_address__icontains=address) |
            Q(address__icontains=address) |
            Q(city__icontains=address) |
            Q(area__icontains=address)
        )

    # -------------------------
    # Merge Commercial + Residential
    # -------------------------
    properties = list(commercial) + list(residential)

    # -------------------------
    # Sorting
    # -------------------------
    if sort:
        try:
            properties.sort(
                key=lambda p: getattr(p, sort.lstrip("-")),
                reverse=sort.startswith("-")
            )
        except:
            pass

    # -------------------------
    # Pagination
    # -------------------------
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Default page size

    page_data = paginator.paginate_queryset(properties, request)

    # -------------------------
    # Serializing Data
    # -------------------------
    serializer = PropertySerializer(page_data, many=True)

    return paginator.get_paginated_response(serializer.data)



from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def property_detail_api(request, ptype, pid):

    MODEL_MAP = {
        "commercial": CommercialProperty,
        "residential": ResidentialProperty,
        "holiday": HolidayProperty,
        "agriculture": AgricultureProperty,
        "pg": PGProperty,
        "business": BusinessForSale,    
    }

    if ptype not in MODEL_MAP:
        return Response({"error": "Invalid property type"}, status=400)

    Model = MODEL_MAP[ptype]

    try:
        property_obj = Model.objects.get(id=pid)
    except Model.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    SERIALIZER_MAP = {
        "commercial": CommercialPropertySerializer,
        "residential": ResidentialPropertySerializer,
        "holiday": HolidayPropertySerializer,
        "agriculture": AgriculturePropertySerializer,
        "pg": PGPropertySerializer,
        "business": BusinessForSaleSerializer,
    }

    SerializerClass = SERIALIZER_MAP[ptype]

    serializer = SerializerClass(property_obj, context={"request": request})

    return Response(serializer.data, status=200)    
  

  


from .serializers import *  
from .pagination import PropertyPagination  

    
from .pagination import PropertyPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
     


from rest_framework.views import APIView
from rest_framework.response import Response

class AllPropertiesView(APIView):    

    def get(self, request):

        search = request.GET.get("search")
        property_type = request.GET.get("property_type")     
        beds = request.GET.get("beds")
        baths = request.GET.get("baths")
        category = request.GET.get("category")

        # 1) Fetch all models
        commercial = list(CommercialProperty.objects.all())
        residential = list(ResidentialProperty.objects.all())
        holiday = list(HolidayProperty.objects.all())
        agriculture = list(AgricultureProperty.objects.all())
        pg = list(PGProperty.objects.all())
        business = list(BusinessForSale.objects.all())

        # 2) merge
        queryset = (
            commercial + residential + holiday +
            agriculture + pg + business
        )

        # 3) SEARCH FILTER
        if search:
            s = search.strip().lower()
            queryset = [
                obj for obj in queryset if (
                    hasattr(obj, "title") and obj.title and s in obj.title.lower()
                ) or (
                    hasattr(obj, "description") and obj.description and s in obj.description.lower()
                ) or (
                    hasattr(obj, "city") and obj.city and s in obj.city.lower()
                ) or (
                    hasattr(obj, "locality") and obj.locality and s in obj.locality.lower()
                )
            ]

        # 4) PROPERTY TYPE FILTER
        if property_type:
            pt = property_type.lower()
            queryset = [
                obj for obj in queryset
                if (
                    hasattr(obj, "property_type") and obj.property_type and str(obj.property_type).lower() == pt
                ) or (
                    hasattr(obj, "subtype") and obj.subtype and obj.subtype.lower() == pt
                )
            ]

        # 5) BEDS FILTER
        if beds:
            if beds == "studio":
                queryset = [obj for obj in queryset if hasattr(obj, "bedrooms") and obj.bedrooms == 0]
            elif beds == "8+":
                queryset = [obj for obj in queryset if hasattr(obj, "bedrooms") and obj.bedrooms >= 8]
            else:
                queryset = [obj for obj in queryset if hasattr(obj, "bedrooms") and obj.bedrooms == int(beds)]

        # 6) BATHS FILTER
        if baths:
            if baths == "8+":
                queryset = [obj for obj in queryset if hasattr(obj, "bathrooms") and obj.bathrooms >= 8]
            else:
                queryset = [obj for obj in queryset if hasattr(obj, "bathrooms") and obj.bathrooms == int(baths)]

         # 7) CATEGORY FILTER  (Residential / Commercial / PG / etc.)
        # 7) CATEGORY FILTER  (Commercial / Residential / PG / etc.)
        if category:
         cat = category.strip().lower()
         filtered = []

         for obj in queryset:  
           matched = False

        # 1) Model.category → residential / commercial / pg / holiday
           if hasattr(obj, "category") and obj.category:
            if obj.category.strip().lower() == cat:
                matched = True

        # 2) property_type.name → buy / rent (CATEGORY → Buy/Rent only)
           if hasattr(obj, "property_type") and obj.property_type:
            pt_name = obj.property_type.name.strip().lower()

            if cat in ["buy", "rent"] and pt_name == cat:
                matched = True

           if matched:
            filtered.append(obj)

    # only inside category block
         queryset = filtered


# ---------------------------------------------------
# ⭐ NEW FILTER → MAIN PROPERTY TYPE (Buy / Rent)
# ---------------------------------------------------
        main_type = request.GET.get("type")   # ?type=rent or ?type=buy
        if main_type:
         mt = main_type.strip().lower()
         queryset = [
          obj for obj in queryset
          if hasattr(obj, "property_type")
          and obj.property_type
          and obj.property_type.name.strip().lower() == mt
    ]


# ---------------------------------------------------
# ⭐ NEW FILTER → SUBTYPE (Studio / Villa / Plots)
# ---------------------------------------------------
        subtype = request.GET.get("subtype")   # ?subtype=villa
        if subtype:
         st = subtype.strip().lower()
         queryset = [
          obj for obj in queryset
          if hasattr(obj, "subtype")
          and obj.subtype
          and obj.subtype.strip().lower() == st
        ]


        # -------------------------------------------
        # ⭐ FINAL LOOP — extract images & video HERE
        # -------------------------------------------
        final_data = []

        for obj in queryset:

            images_list = []
            video_url = None

            # First: related_name="media"
            if hasattr(obj, "media") and obj.media.exists():
                for m in obj.media.all():
                    if m.image:
                        images_list.append(m.image.url)
                    if m.image_360:
                        images_list.append(m.image_360.url)
                    if not video_url and m.video_url:
                        video_url = m.video_url
                    if not video_url and m.video_file:
                        video_url = m.video_file.url

            # Second: auto reverse lookup
            else:
                for rel in obj._meta.get_fields():
                    if rel.one_to_many and rel.auto_created:
                        rel_name = rel.get_accessor_name()
                        qs = getattr(obj, rel_name).all()

                        if qs.exists():
                            for m in qs:
                                if hasattr(m, "image") and m.image:
                                    images_list.append(m.image.url)
                                if hasattr(m, "image_360") and m.image_360:
                                    images_list.append(m.image_360.url)
                                if hasattr(m, "video_url") and m.video_url:
                                    video_url = video_url or m.video_url
                                if hasattr(m, "video_file") and m.video_file:
                                    video_url = video_url or m.video_file.url
                            break
  
            # property type text
            if hasattr(obj, "property_type") and obj.property_type:
                property_type_value = str(obj.property_type)
            else:
                property_type_value = getattr(obj, "subtype", None)
            
            # company logo (if company exists)
            company_logo = None
            if hasattr(obj, "company") and obj.company:
             if hasattr(obj.company, "image") and obj.company.image:
               company_logo = obj.company.image.url    
               
            agent_obj = None
            if getattr(obj, "user_id", None):
              try:
                agent_obj = CustomUser.objects.get(id=obj.user_id)
              except CustomUser.DoesNotExist:
                agent_obj = None
            final_data.append({
                "id": obj.id,
                "title": getattr(obj, "title", None),
                "description": getattr(obj, "description", None),
                "subtype" : getattr(obj, "subtype", None),  
                "city": getattr(obj, "city", None),
                "locality": getattr(obj, "locality", None),
                "full_location": getattr(obj, "address", None),  
                "price": getattr(obj, "price", None) or getattr(obj, "expected_price", None),
                "asking_price" : getattr(obj, "asking_price", None),
                "business_type" : getattr(obj, "business_type", None),  
               "payment_frequency" : getattr(obj, "business_type", None),       
                "bedrooms": getattr(obj, "bedrooms", None),
                "bathrooms": getattr(obj, "bathrooms", None),
                "category": getattr(obj, "category", None) or getattr(obj, "listing_type", None),
                "property_type": property_type_value,
                "images": images_list,
                "video": video_url,
                
                "company_logo": company_logo,  # ⭐ NEW  
                
                "currency": getattr(obj, "currency", None),  # ⭐ NEW
                # AREA (Sq Ft)
                "area": getattr(obj, "area", None),       # ⭐ NEW
                "area_unit": getattr(obj, "area_unit", None),  # e.g. "Sq.Ft"
                "total_area" : getattr(obj, "total_area", None),
                "builtup_area": getattr(obj, "builtup_area", None),  
                "carpet_area" : getattr(obj, "carpet_area", None),
                "plot_area" : getattr(obj, "plot_area", None),
                "area_sqft" : getattr(obj, "area_sqft", None),
                "super_area" : getattr(obj, "super_area", None),  
                  # ⭐ AGENT DETAILS (from user_id)
                "agent": {
                  "name": getattr(agent_obj, "full_name", None) if agent_obj else None,  
                #   "image": agent_obj.image.url if (agent_obj and agent_obj.image) else None,
                  "phone": getattr(agent_obj, "phone", None) if agent_obj else None,
                  "whatsapp": getattr(agent_obj, "phone", None) if agent_obj else None,  
    }
            })

        return Response(final_data)






# ==============================================================================================================================
# Create krne ke liye Pehle Data Share krna padta he ..add()

@api_view(["GET"])
def company_list(request):
    companies = RealEstateCompany.objects.all().values("id", "name")
    return Response(list(companies))


@api_view(["GET"])
def property_type_list(request):
    types = PropertyType.objects.all().values("id", "name")  
    return Response(list(types))


@api_view(["GET"])
def amenity_list(request):
    amenities = Amenity.objects.all().values("id", "name")    
    return Response(list(amenities))  


# Holiday Post ---
from django.db import transaction

@api_view(["POST"])
def create_holiday_property(request):
    # ----- 1. Copy normal fields -----  
    data = request.data.dict()  
    
     # Convert total_area to number
    try:
        data["total_area"] = float(data.get("total_area", 0))
    except:
        data["total_area"] = 0

    # amenities = request.data.get("amenities")
    # if isinstance(amenities, str):
    #     amenities = [x.strip() for x in amenities.split(",")]
    # data["amenities"] = amenities       
    # Amenities list (multiple values)
    amenities = request.data.getlist("amenities")
    data["amenities"] = amenities       
       
    # ----- 2. File uploads -----
    images = request.FILES.getlist("media")             # multiple gallery images
    profile_photo = request.FILES.get("profile_photo")  # main profile photo
    image_360 = request.FILES.get("image_360")          # 360 image
    video_file = request.FILES.get("video_file")        # uploaded video

    # Specific room/layout images
    exterior_image = request.FILES.get("exterior_image")
    living_room_image = request.FILES.get("living_room_image")
    bedroom_image = request.FILES.get("bedroom_image")
    bathroom_image = request.FILES.get("bathroom_image")
    kitchen_image = request.FILES.get("kitchen_image")
    floor_plan_image = request.FILES.get("floor_plan_image")
    master_plan_image = request.FILES.get("master_plan_image")
    location_map_image = request.FILES.get("location_map_image")

    # Add files to data for serializer if required
    if profile_photo:
        data["profile_photo"] = profile_photo
    if image_360:
        data["image_360"] = image_360
    if video_file:
        data["video_file"] = video_file

    # ----- 3. Create property -----
    serializer = HolidayPropertySerializer(data=data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                property_obj = serializer.save()

                # ----- 4. Save multiple gallery images with all new fields -----
                # If you want one HolidayPropertyImage for each media type, you can create individually:
                HolidayPropertyImage.objects.create(
                    property=property_obj,
                    exterior_image=exterior_image,
                    living_room_image=living_room_image,
                    bedroom_image=bedroom_image,
                    bathroom_image=bathroom_image,
                    kitchen_image=kitchen_image,
                    floor_plan_image=floor_plan_image,
                    master_plan_image=master_plan_image,
                    location_map_image=location_map_image,
                    image_360=image_360,
                    video_file=video_file,
                    video_url=data.get("video_url"),
                    is_featured=data.get("is_featured", False),
                    sort_order=data.get("sort_order", 0)
                )

                # ----- 5. Save generic gallery images -----
                if images:
                    HolidayPropertyImage.objects.bulk_create([
                        HolidayPropertyImage(property=property_obj, image=img)
                        for img in images
                    ])

        except Exception as e:
            return Response({"error": str(e)}, status=400)

        # ----- 6. Return Full Serialized Data -----
        full_data = HolidayPropertySerializer(property_obj).data
        return Response(full_data, status=201)

    return Response(serializer.errors, status=400)


#--------------------------------------------------------------------------------------

# Agricuture POST .add()

@api_view(["POST"])
def create_agriculture_property(request):

    data = request.data.dict()        

    # Convert total_area to number
    try:
        data["total_area"] = float(data.get("total_area", 0))
    except:
        data["total_area"] = 0
    
    # Amenities list
    # Amenities list (multiple values)
    amenities = request.data.getlist("amenities")
    data["amenities"] = amenities   

    # amenities = request.data.get("amenities")
    # if isinstance(amenities, str):
    #     amenities = [x.strip() for x in amenities.split(",")]
    # data["amenities"] = amenities  

    # MULTI IMAGES
    images = request.FILES.getlist("images")   # 👈 FIXED

    # Single files
    image_360 = request.FILES.get("image_360")
    video_file = request.FILES.get("video_file")

    

    # Create main record
    serializer = AgriculturePropertySerializer(data=data)

    if serializer.is_valid():
        property_obj = serializer.save()

        # Save gallery images
        for img in images:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                image=img
            )

        # 360 image
        if image_360:
            AgriculturePropertyImage.objects.create(  
                property=property_obj,
                image_360=image_360
            )

        # video file
        if video_file:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                video_file=video_file
            )   

        return Response(
            AgriculturePropertySerializer(property_obj).data,
            status=201
        )

    return Response(serializer.errors, status=400)    

# ----------------------------------------------------------------------------

# PG POST .. 


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import PGProperty, PGPropertyImage
from .serializers import PGPropertySerializer

@api_view(["POST"])
def create_pg_property(request):  
    # Safe for JSON and FormData
    if hasattr(request.data, "dict"):
        data = request.data.dict()
    else:
        data = request.data.copy() 

    # Convert total_area to number
    try:
        data["total_area"] = float(data.get("total_area", 0))
    except:
        data["total_area"] = 0

    # Amenities list
    # amenities = request.data.get("amenities")
    # if isinstance(amenities, str):
    #     amenities = [x.strip() for x in amenities.split(",")]
    # data["amenities"] = amenities   
    # Amenities list (multiple values)

    # amenities = request.data.getlist("amenities")
    # data["amenities"] = amenities 
    # 
    # Amenities fix     
    amenities = request.data.getlist("amenities") if hasattr(request.data, "getlist") else request.data.get("amenities", [])
    data["amenities"] = amenities   

    # MULTIPLE GALLERY IMAGES
    gallery_images = request.FILES.getlist("media")
    # 360° + VIDEO
    image_360 = request.FILES.get("image_360")
    video_file = request.FILES.get("video_file")

    # SPECIFIC IMAGES
    exterior_image = request.FILES.get("exterior_image")
    living_room_image = request.FILES.get("living_room_image")
    bedroom_image = request.FILES.get("bedroom_image")
    bathroom_image = request.FILES.get("bathroom_image")
    kitchen_image = request.FILES.get("kitchen_image")
    floor_plan_image = request.FILES.get("floor_plan_image")
    master_plan_image = request.FILES.get("master_plan_image")
    location_map_image = request.FILES.get("location_map_image")

    

    # Add to data (if PGProperty has these fields)
    if image_360:
        data["image_360"] = image_360
    if video_file:
        data["video_file"] = video_file

    serializer = PGPropertySerializer(data=data)

    if serializer.is_valid():
        try:
            with transaction.atomic():

                # CREATE MAIN PROPERTY
                property_obj = serializer.save()

                # CREATE ONE IMAGE ENTRY FOR SPECIFIC IMAGES
                PGPropertyImage.objects.create(
                    property=property_obj,
                    exterior_image=exterior_image,
                    living_room_image=living_room_image,
                    bedroom_image=bedroom_image,
                    bathroom_image=bathroom_image,
                    kitchen_image=kitchen_image,
                    floor_plan_image=floor_plan_image,
                    master_plan_image=master_plan_image,
                    location_map_image=location_map_image,
                    image_360=image_360,
                    video_file=video_file,
                    video_url=data.get("video_url"),
                    is_featured=data.get("is_featured", False),
                    sort_order=data.get("sort_order", 0)
                )

                # CREATE MULTIPLE GALLERY IMAGES
                if gallery_images:
                    PGPropertyImage.objects.bulk_create([
                        PGPropertyImage(property=property_obj, image=img)
                        for img in gallery_images
                    ])

        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response(PGPropertySerializer(property_obj).data, status=201)

    return Response(serializer.errors, status=400)

#-----------------------------------------------------------------------------------------
@api_view(["GET"])
def get_R_properties_by_user(request, user_id):
    
    properties = ResidentialProperty.objects.filter(user_id=user_id, status="Active").order_by("-id")
    serializer = ResidentialPropertySerializer(properties, many=True)
    return Response(serializer.data) 

@api_view(["GET"])
def get_C_properties_by_user(request, user_id):
    
    properties = CommercialProperty.objects.filter(user_id=user_id, status="Active").order_by("-id")
    serializer = CommercialPropertySerializer(properties, many=True)     
    return Response(serializer.data) 


@api_view(["GET"])
def get_pg_properties_by_user(request, user_id):
    
    properties = PGProperty.objects.filter(user_id=user_id, status="Active").order_by("-id")
    serializer = PGPropertySerializer(properties, many=True)
    return Response(serializer.data)    


@api_view(["GET"])
def get_holiday_properties_by_user(request, user_id):
    properties = HolidayProperty.objects.filter(user_id=user_id, status="Active").order_by("-id")
    serializer = HolidayPropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_agriculture_properties_by_user(request, user_id):
    properties = AgricultureProperty.objects.filter(user_id=user_id, status="Active").order_by("-id")
    serializer = AgriculturePropertySerializer(properties, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_business_properties_by_user(request, user_id):
    properties = BusinessForSale.objects.filter(user_id=user_id, status="Active").order_by("-id")  
    serializer = BusinessForSaleSerializer(properties, many=True)
    return Response(serializer.data)  


# ---------------------------------------------------------------------------------------------------------
# For User Side Delete Tamprary .......... Not All .

@api_view(["PUT"])
def soft_delete_agriculture_property(request, pk):
    try:
        prop = AgricultureProperty.objects.get(id=pk)
    except AgricultureProperty.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Agriculture property marked as Inactive"}, status=200)


@api_view(["PUT"])
def soft_delete_holiday_property(request, pk):
    try:
        prop = HolidayProperty.objects.get(id=pk)
    except HolidayProperty.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Holiday property marked as Inactive"}, status=200)

@api_view(["PUT"])
def soft_delete_pg_property(request, pk):
    try:
        prop = PGProperty.objects.get(id=pk)
    except PGProperty.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Holiday property marked as Inactive"}, status=200)

@api_view(["PUT"])
def soft_delete_business_property(request, pk):
    try:
        prop = BusinessForSale.objects.get(id=pk)
    except BusinessForSale.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Holiday property marked as Inactive"}, status=200)

@api_view(["PUT"])
def soft_delete_C_property(request, pk):
    try:
        prop = CommercialProperty.objects.get(id=pk)
    except CommercialProperty.DoesNotExist:
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Holiday property marked as Inactive"}, status=200)



@api_view(["PUT"])
def soft_delete_R_property(request, pk):
    try:
        prop = ResidentialProperty.objects.get(id=pk)
    except ResidentialProperty.DoesNotExist:     
        return Response({"error": "Property not found"}, status=404)

    prop.status = "Inactive"
    prop.save()

    return Response({"message": "Holiday property marked as Inactive"}, status=200)


# -------------------------------------------------------------------------------

# BusinessForSale POST ..add()  



@api_view(["POST"])  
def create_business_for_sale(request):

    data = request.data.dict()

    # Convert total_area to float
    try:
        data["total_area"] = float(data.get("total_area", 0))
    except:
        data["total_area"] = 0

    # Amenities list
    # Amenities list (multiple values)
    amenities = request.data.getlist("amenities")
    data["amenities"] = amenities  
    # amenities = request.data.get("amenities")
    # if isinstance(amenities, str):
    #     amenities = [x.strip() for x in amenities.split(",")]
    # data["amenities"] = amenities     

    # Multiple images (main images)
    multiple_images = request.FILES.getlist("media")
    # 360 image & video
    image_360 = request.FILES.get("image_360")
    video_file = request.FILES.get("video_file")

    # Specific images
    exterior_image = request.FILES.get("exterior_image")
    living_room_image = request.FILES.get("living_room_image")
    bedroom_image = request.FILES.get("bedroom_image")
    bathroom_image = request.FILES.get("bathroom_image")
    kitchen_image = request.FILES.get("kitchen_image")
    floor_plan_image = request.FILES.get("floor_plan_image")
    master_plan_image = request.FILES.get("master_plan_image")
    location_map_image = request.FILES.get("location_map_image")

    

    if image_360:
        data["image_360"] = image_360

    if video_file:
        data["video_file"] = video_file

    serializer = BusinessForSaleSerializer(data=data)

    if serializer.is_valid():
        property_obj = serializer.save()

        # ---------------------------
        # 1) Save multiple images
        # ---------------------------
        for img in multiple_images:
            BusinessForSaleImage.objects.create(
                property=property_obj,
                image=img
            )

        # ---------------------------
        # 2) Save specific images
        # ---------------------------
        BusinessForSaleImage.objects.create(
            property=property_obj,
            exterior_image=exterior_image,
            living_room_image=living_room_image,
            bedroom_image=bedroom_image,
            bathroom_image=bathroom_image,
            kitchen_image=kitchen_image,
            floor_plan_image=floor_plan_image,
            master_plan_image=master_plan_image,
            location_map_image=location_map_image,
        )

        return Response(BusinessForSaleSerializer(property_obj).data, status=201)

    return Response(serializer.errors, status=400)  
    
# --------------------------------------------------------------------------------------------------------- 
# C And R Property POST ----------------------------------

# @api_view(["POST"])
# def create_property(request):
#     print("=== FUNCTION CALLED ===")  
#     data = request.data.copy()  
    
#     images = request.FILES.getlist("media")  # generic gallery
#     exterior_image = request.FILES.get("exterior_image")
#     living_room_image = request.FILES.get("living_room_image")
#     bedroom_image = request.FILES.get("bedroom_image")
#     bathroom_image = request.FILES.get("bathroom_image")
#     kitchen_image = request.FILES.get("kitchen_image")
#     floor_plan_image = request.FILES.get("floor_plan_image")
#     master_plan_image = request.FILES.get("master_plan_image")
#     location_map_image = request.FILES.get("location_map_image")
#     image_360 = request.FILES.get("image_360")
#     video_file = request.FILES.get("video_file")

#     # -----------------------------
#     # 1) Basic Validations
#     # -----------------------------
#     print("Hello")  
#     print("REQUEST DATA = ", request.data)     
#     required_fields = [
#         "title", "description", "category", "subtype",
#         "price", "price_type", "country", "city"
#     ]

#     for field in required_fields:
#         if field not in data:
#             return Response(
#                 {field: "This field is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     # Validate USER
#     user_id = data.get("user")
#     if user_id:
#         try:
#             user = regesteruser.objects.get(id=user_id)
#         except regesteruser.DoesNotExist:
#             return Response({"user": ["Invalid user id"]}, status=400)
#     else:
#         user = None

#     # Validate AGENT
#     agent_id = data.get("agent")
#     agent = None
#     if agent_id:
#         try:
#             agent = Agent.objects.get(id=agent_id)
#         except Agent.DoesNotExist:
#             return Response({"agent": ["Invalid agent id"]}, status=400)

#     # Validate Property Type
#     ptype_id = data.get("property_type")
#     if ptype_id:
#         try:
#             ptype = PropertyType.objects.get(id=ptype_id)
#         except PropertyType.DoesNotExist:
#             return Response({"property_type": ["Invalid property type"]}, status=400)
#     else:
#         ptype = None
    
#     # Validate COMPANY
#     company_id = data.get("company")
#     company = None
#     if company_id:
#      try:
#         company = RealEstateCompany.objects.get(id=company_id)
#      except RealEstateCompany.DoesNotExist:
#         return Response({"company": ["Invalid company id"]}, status=400)



#     # -----------------------------
#     # 2) Create Main Property Model (Commercial / Residential)
#     # -----------------------------
#     category = data.get("category").lower()

#     if category == "commercial":
#         property_obj = CommercialProperty.objects.create(
#             company=company,
#             user=user,
#             agent=agent,
#             property_type=ptype,
#             title=data.get("title"),
#             description=data.get("description"),
#             category=category,
#             subtype=data.get("subtype"),

#             country=data.get("country"),
#             city=data.get("city"),
#             locality=data.get("locality"),
#             sub_locality=data.get("sub_locality"),
#             map_address=data.get("map_address"),
#             latitude=data.get("latitude"),
#             longitude=data.get("longitude"),

#             area_sqft=data.get("area_sqft"),
#             super_area=data.get("super_area"),
#             furnishing=data.get("furnishing"),
#             parking_spaces=data.get("parking_spaces"),
#             washrooms=data.get("washrooms"),
#             pantry=data.get("pantry", False),
            
#             currency=data.get("currency"),
#             price=data.get("price"),
#             price_type=data.get("price_type"),
#             payment_frequency=data.get("payment_frequency"),
#             deposit_amount=data.get("deposit_amount"),
#             maintenance_fees=data.get("maintenance_fees"),
#             service_charge_included=data.get("service_charge_included", False),

#             available_from=data.get("available_from"),
#             status=data.get("status", "Pending"),
#             property_status=data.get("property_status"),
#             ownership_type=data.get("ownership_type"),
#             featured=data.get("featured", False),
#         )

#     elif category == "residential":
#         property_obj = ResidentialProperty.objects.create(
#             company=company,  
#             user=user,
#             agent=agent,
#             property_type=ptype,
#             title=data.get("title"),
#             description=data.get("description"),
#             category=category,
#             subtype=data.get("subtype"),
            
#             # 🔥 FIX ADDED HERE
#             bedrooms=data.get("bedrooms"),
#             bathrooms=data.get("bathrooms"),
#             balcony=data.get("balcony"),
#             view=data.get("view"),      
            
#             country=data.get("country"),
#             city=data.get("city"),
#             locality=data.get("locality"),
#             sub_locality=data.get("sub_locality"),
#             map_address=data.get("map_address"),
#             latitude=data.get("latitude"),
#             longitude=data.get("longitude"),

#             area_sqft=data.get("area_sqft"),
#             super_area=data.get("super_area"),
#             furnishing=data.get("furnishing"),
#             parking_spaces=data.get("parking_spaces"),
#             washrooms=data.get("washrooms"),
#             pantry=data.get("pantry", False),
            
#             currency=data.get("currency"),  
#             price=data.get("price"),
#             price_type=data.get("price_type"),
#             payment_frequency=data.get("payment_frequency"),
#             deposit_amount=data.get("deposit_amount"),
#             maintenance_fees=data.get("maintenance_fees"),
#             service_charge_included=data.get("service_charge_included", False),

#             available_from=data.get("available_from"),
#             status=data.get("status", "Pending"),
#             property_status=data.get("property_status"),
#             ownership_type=data.get("ownership_type"),
#             featured=data.get("featured", False),
#         )

#     else:
#         return Response({"category": "Invalid category"}, status=400)

#     # -----------------------------
#     # 3) Save Amenities (M2M)
#     # -----------------------------
#     amenities = data.get("amenities", [])
#     if isinstance(amenities, list):
#         property_obj.amenities.set(amenities)

#     # -----------------------------
#     # 4) Create Subtype Model (Office, Shop, Villa...)
#     # -----------------------------
#     subtype = data.get("subtype").lower()
#     subtype_data = request.data.get(subtype, {})

#     SUBTYPE_MAP = {
#         # COMMERCIAL
#         "office": Office,
#         "shop": Shop,
#         "showroom": Showroom,
#         "warehouse": Warehouse,
#         "factory": Factory,
#         "commercial_land": CommercialLand,

#         # RESIDENTIAL
#         "apartment": Apartment,
#         "villa": Villa,
#         "townhouse": Townhouse,
#         "studio": Studio,
#         "penthouse": Penthouse,
#         "duplex": Duplex,
#         "compound": Compound,
#         "plot": ResidentialPlot,
#     }

#     ModelClass = SUBTYPE_MAP.get(subtype)

#     if ModelClass:
#         ModelClass.objects.create(property=property_obj, **subtype_data)
#     else:
#         return Response({"subtype": "Invalid subtype"}, status=400)

#     # -----------------------------
#     # 5) Final Response
#     # -----------------------------
#     return Response({
#         "success": True,
#         "id": property_obj.id, 
#         "message": "Property created successfully"
#     }, status=201)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import *  

@api_view(["POST"])  
def create_property(request):
    data = request.data.copy()

    # -----------------------------
    # 1) Extract uploaded files
    # -----------------------------
    gallery_images = request.FILES.getlist("media")  
    exterior_image = request.FILES.get("exterior_image")
    living_room_image = request.FILES.get("living_room_image")
    bedroom_image = request.FILES.get("bedroom_image")
    bathroom_image = request.FILES.get("bathroom_image")
    kitchen_image = request.FILES.get("kitchen_image")

    floor_plan_image = request.FILES.get("floor_plan_image")
    master_plan_image = request.FILES.get("master_plan_image")
    location_map_image = request.FILES.get("location_map_image") 
    image_360 = request.FILES.get("image_360")
    video_file = request.FILES.get("video_file")

    # -----------------------------
    # 2) Validations
    # -----------------------------
    required_fields = ["title", "description", "category", "subtype",
                       "price", "price_type", "country", "city"]

    for field in required_fields:
        if field not in data:
            return Response({field: "This field is required"}, status=400)

    # Validate models
    user = regesteruser.objects.filter(id=data.get("user")).first()
    agent = Agent.objects.filter(id=data.get("agent")).first()
    ptype = PropertyType.objects.filter(id=data.get("property_type")).first()
    company = RealEstateCompany.objects.filter(id=data.get("company")).first()

    # -----------------------------
    # 3) Create Property
    # -----------------------------
    category = data.get("category").lower()

    try:
        with transaction.atomic():     
    
            #  Pick the correct model
            if category == "commercial":    
                MainModel = CommercialProperty
            else:
                MainModel = ResidentialProperty
            
            # Detect all concrete fields (exclude M2M / reverse relations)
            model_fields = [
                f.name for f in MainModel._meta.get_fields()
                if f.concrete and not f.many_to_many and not f.one_to_many
            ]
            
            # Fields we should never allow through safe_data
            exclude_keys = ["user", "agent", "company", "property_type", "amenities", "media"]
            
            # Build final safe_data dynamically
            safe_data = {
                k: data.get(k)
                for k in data
                if k in model_fields and k not in exclude_keys
            }
            
            # Create property
            property_obj = MainModel.objects.create(
                company=company,
                user=user,
                agent=agent,
                property_type=ptype,
                **safe_data
            )
          
            # -----------------------------
            # 4) Amenities
            # -----------------------------
            # -----------------------------
        # ✅ Set amenities (JSON-friendly)
            # -----------------------------
            amenities = data.get("amenities", [])
            property_obj.amenities.set(amenities)   

            # -----------------------------
            # 5) Subtype Model Create
            # -----------------------------
            subtype = data.get("subtype").lower()
            subtype_data = request.data.get(subtype, {})

            SUBTYPE_MAP = {
                # COMMERCIAL
                "office": Office,
                "shop": Shop,
                "showroom": Showroom,
                "warehouse": Warehouse,
                "factory": Factory,
                "commercialland": CommercialLand,

                # RESIDENTIAL
                "apartment": Apartment,
                "villa": Villa,
                "townhouse": Townhouse,
                "studio": Studio,
                "penthouse": Penthouse,
                "duplex": Duplex,
                "compound": Compound,
                "residentialplot": ResidentialPlot,
            }

            ModelClass = SUBTYPE_MAP.get(subtype)

            if not ModelClass:
                return Response({"subtype": "Invalid subtype"}, status=400)

            ModelClass.objects.create(property=property_obj, **subtype_data)

            # -----------------------------
            # 6) Save Images 
            # -----------------------------

            # (A) COMMERCIAL IMAGES
            if category == "commercial":
                # Single image set (room/layout/video)
                CommercialPropertyImage.objects.create(
                    property=property_obj,
                    exterior_image=exterior_image,
                    living_room_image=living_room_image,
                    bedroom_image=bedroom_image,
                    bathroom_image=bathroom_image,
                    kitchen_image=kitchen_image,
                    floor_plan_image=floor_plan_image,
                    master_plan_image=master_plan_image,
                    location_map_image=location_map_image,
                    image_360=image_360,
                    video_file=video_file,
                    video_url=data.get("video_url")
                )

                # Gallery images
                for img in gallery_images:
                    CommercialPropertyImage.objects.create(
                        property=property_obj,
                        image=img
                    )

            # (B) RESIDENTIAL IMAGES
            elif category == "residential":
                ResidentialPropertyImage.objects.create(
                    property=property_obj,
                    exterior_image=exterior_image,
                    living_room_image=living_room_image,
                    bedroom_image=bedroom_image,
                    bathroom_image=bathroom_image,
                    kitchen_image=kitchen_image,
                    floor_plan_image=floor_plan_image,
                    master_plan_image=master_plan_image,
                    location_map_image=location_map_image,
                    image_360=image_360,
                    video_file=video_file,
                    video_url=data.get("video_url")
                )

                for img in gallery_images:
                    ResidentialPropertyImage.objects.create(
                        property=property_obj,
                        image=img
                    )

    except Exception as e:
        return Response({"error": str(e)}, status=400)

    return Response({
        "success": True,
        "id": property_obj.id,
        "message": "Property created successfully"
    }, status=201)   


# --------------------------------------------------------------------------------------------

# Agent ke liye Team Menmber  ---------
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser   


@api_view(["GET"])
def get_agents(request):
    agents = Agent.objects.filter(status="Active").order_by("-id")
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data)        



@api_view(["GET"])
def get_agent_detail(request, id):
    try:
        agent = Agent.objects.get(id=id)
    except Agent.DoesNotExist:
        return Response({"error": "Agent not found"}, status=404)

    serializer = AgentSerializer(agent)
    return Response(serializer.data)  


from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

@api_view(["POST"])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def create_agent(request):
    serializer = AgentSerializer(data=request.data)
    if serializer.is_valid():
        agent = serializer.save()
        return Response(AgentSerializer(agent).data, status=201)
    return Response(serializer.errors, status=400)      


# ----------------------------------------------------------------------------------------


# Normal User Jo Propertys List kregaa ---------

from rest_framework import generics
import random
from django.core.cache import cache


class RegisterUserListAPIView(generics.ListAPIView):
    queryset = regesteruser.objects.all()
    serializer_class = RegisterUserSerializer
    
# class RegisterUserCreateAPIView(generics.CreateAPIView):
#     queryset = regesteruser.objects.all()
#     serializer_class = RegisterUserSerializer

# STEP 1 — Send OTP
class SendOTPAPIView(APIView):
    def post(self, request):
        data = request.data

        email = data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save temporarily
        cache.set(f"register_{email}", {
            "data": data,
            "otp": otp
        }, timeout=600)  # 10 min

        # Send Email
        send_mail(
            subject="Your OTP Verification Code",
            message=f"Your OTP is: {otp}",
            from_email="skingkhan9174@gmail.com",  
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({
            "message": "OTP sent successfully to email",
            "email": email
        })


# STEP 2 — Verify OTP + Create User
class VerifyOTPAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP required"}, status=400)

        cached_data = cache.get(f"register_{email}")

        if not cached_data:
            return Response({"error": "OTP expired or invalid"}, status=400)

        if str(cached_data["otp"]) != str(otp):
            return Response({"error": "Invalid OTP"}, status=400)

       # OTP Match — Create User NOW
        user_data = cached_data["data"]
        
        serializer = RegisterUserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            
            # ----------------------------------------
            # Create in CustomUser also
            # ----------------------------------------
            custom_user = CustomUser(
                full_name=user_data.get("name"),   
                email=user_data.get("email"),
                phone=user_data.get("phone"),
            )
            custom_user.set_password(user_data.get("password"))  # Properly hash
            custom_user.save()
        
            # Delete temp data
            cache.delete(f"register_{email}")
        
            return Response({
                "message": "OTP verified & user created successfully",
                "register_user_id": user.id,
                "custom_user_id": custom_user.id,  
            })


        return Response(serializer.errors, status=400)


class RegisterUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = regesteruser.objects.all()
    serializer_class = RegisterUserSerializer
    
class RegisterUserUpdateAPIView(generics.UpdateAPIView):
    queryset = regesteruser.objects.all()
    serializer_class = RegisterUserSerializer

class RegisterUserDeleteAPIView(generics.DestroyAPIView):
    queryset = regesteruser.objects.all()
    serializer_class = RegisterUserSerializer  


# -----------------------------------------------------------------------------------------

# Login or Logout ke liye -------               .............add()

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from datetime import timedelta  

   

class MyTokenObtainPairView(TokenObtainPairView):  
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:

            access = response.data.get("access")
            refresh = response.data.get("refresh")

            # FIXED → email case-insensitive
            email = request.data.get("email", "").lower()
            user = CustomUser.objects.filter(email__iexact=email).first()

            user_data = {}
            if user:
                user_data = {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "phone": user.phone,
                    "city": user.city,
                    "pincode" : user.pincode  
                }

            return Response({
                "access": access,
                "user": user_data
            })

        return response



@api_view(["POST"])  
def logout_view(request):
    # Delete refresh cookie on logout. If you use blacklisting, also blacklist refresh from cookie.
    refresh = request.COOKIES.get("refresh_token")
    if refresh:
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except:
            pass

    resp = Response({"detail": "Logged out"}, status=200)
    resp.delete_cookie("refresh_token", path="/api/token/refresh/")
    return resp





# -------------------------------------------------------------------------------------------------------

# For Verify Company ....

from django.http import JsonResponse    
import json
from .models import RealEstateCompany

def update_verified_company(request, company_id):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        verified_value = data.get("verified")

        try:
            company = RealEstateCompany.objects.get(id=company_id)
            company.verified = True if verified_value == "1" else False
            company.save()
            return JsonResponse({"status": "ok"})
        except RealEstateCompany.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Company not found"})
