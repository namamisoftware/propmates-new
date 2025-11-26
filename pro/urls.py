from django.urls import path
from .views import *
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView  
from django.conf import settings
from django.conf.urls.static import static  
from .views import MyTokenObtainPairView, logout_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [    
    
    
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="token_logout"),     
    # path('check-email/', EmailCheckView.as_view(), name='check-email'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('verify-login-otp/', LoginOTPVerifyView.as_view(), name='verify-login-otp'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    path("property/<str:step>/", PropertyStepView.as_view(), name="property-step"),
    path("property-create/", PropertyCreateView.as_view(), name="property-create"),
  
    path("property-update/<int:pk>/", PropertyUpdateView.as_view(), name="property-update"),
    path("property-list/<int:user>/", PropertyListView.as_view(), name="property-list"),
    path("property-delete/<int:pk>/", PropertyDeleteView.as_view(), name="property-delete"),
    # path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    # path("property/detail/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
    # path("property/full/<int:pk>/", PropertyFullDetailView.as_view(), name="property-full"),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('properties/', AllPropertiesView.as_view(), name='all-properties'),
    path('properties/', AllPropertiesView.as_view(), name='all-properties'),
    path('properties/commercial/', PropertyByCommercialView.as_view(), name='properties-by-commercial'),
    path('properties/country/<int:country_id>/', PropertyByCountryView.as_view(), name='properties-by-country'),
    path('properties/type/<int:looking_to>/', PropertyByTypeView.as_view(), name='properties-by-type'),
    path('properties/propertytype/<int:property_type_id>/', PropertyByPropertyTypeView.as_view(), name='properties-by-propertytype'),

    path('properties/agent/<int:agent_id>/', PropertyByAgentView.as_view(), name='properties-by-agent'),
    path('properties/company/<int:company_id>/', PropertyByCompanyView.as_view(), name='properties-by-company'),
    # path('countries/', CountryListView.as_view(), name='all-countries'),
    # path('company/<int:company_id>/', CompanyById.as_view(), name='company-by-id'),
    # path('propertytype/<int:property_type_id>/', PropertyTypeById.as_view(), name='property-type-by-id'),
    # path('propertytype/looking_to/<int:looking_to>/', PropertyTypeByLookingTo.as_view(), name='property-type-by-looking-to'),
    # path('country/<int:country_id>/', CountryById.as_view(), name='country-by-id'),
    path('amenity/<int:amenity_id>/', AmenityById.as_view(), name='amenity-by-id'),
    path('propertyamenity/<int:property_id>/', PropertyAmenityList.as_view(), name='property-amenity-by-id'),

    # path('sliders/', SliderListView.as_view(), name='all-sliders'),
    path('agents/', AgentListView.as_view(), name='all-agents'),
    # path('companies/', CompanyListView.as_view(), name='all-companies'),
    # path('blogs/', BlogListView.as_view(), name='all-blogs'),
    # path('testimonials/', TestimonialListView.as_view(), name='all-testimonials'),


    # Check 
    path('c/', chack, name='c'),          
   
    path('search-location/', search_location, name='search-location'),
    path('reverse-location/', reverse_location, name='reverse_location'),
    path('filter-by-location/', filter_by_location, name='filter_by_location'), 
    # path('details/<int:agent_id>/', agent_details, name='details'),
    
    path('verify-agent/<int:agent_id>/', verify_agent, name='verify_agent'),
    
     
    path("update-status/", update_status, name="update_status"),       
    # Normal Users
    # path('agent/<int:id>/edit/', edit_member, name='edit_member'),  
    # path('agent/<int:id>/delete/', delete_member, name='delete_member'),  
    # path('agent/<int:id>/details/', details, name='details'),   
    
    
    # Updated Serilizer ke liye For APIs.-------------------------------------------------------
    
   

    # path("properties/", property_list_api, name="property_list"),       
    
   
    
    
    
    
    
    
    # Properties Filtering and Details ke liye -----------------
    path("properties/", AllPropertiesView.as_view(), name="property_list"),   
    path("property/detail/<str:ptype>/<int:pid>/", property_detail_api, name="property_detail"),     
    
    
    # Get Data For Post Property --------------------------------------------------------
    path("companies/", company_list, name="company-list"),
    path("property-types/", property_type_list, name="property-type-list"),
    path("amenities/", amenity_list, name="amenity-list"),    
    
    # Property POST All TYpes ---------------------------------------------------------------------------
    path("propertyCR/create/", create_property),        
    path("business/create/", create_business_for_sale),    
    path("pg/create/", create_pg_property),
    path("agriculture/create/", create_agriculture_property, name="create_agriculture_property"),
    path("holiday/create/", create_holiday_property, name="create_holiday_property"),  
    
    
    
    # Agent ke liye --------------------------------------------------------------
    path("agent/create/", create_agent),  
    path("agent/", get_agents),
    path("agent/<int:id>/", get_agent_detail, name="agentDetails"),  
    
    
    # Normal Users ke lite  (registeruser model)   
    
    path("users/", RegisterUserListAPIView.as_view(), name="user-list"),
    # path("users/create/", RegisterUserCreateAPIView.as_view(), name="user-create"),
    path("send-otp/", SendOTPAPIView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify-otp"),  
    
    path("users/<int:pk>/", RegisterUserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", RegisterUserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", RegisterUserDeleteAPIView.as_view(), name="user-delete"), 

    # Detail API — /property/<category>/<id>/
    # path("property/<str:category>/<int:pk>/", 
    #      PropertyDetailAPI, 
    #      name="property_detail"),     
]    




if settings.DEBUG:    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)