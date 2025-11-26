from django.urls import path
from . import dash_views
from pro.views import *  

urlpatterns = [
    path('', dash_views.admin_login, name='admin_login'),
    path('logout/', dash_views.admin_logout, name='admin_logout'),
    path('home/', dash_views.dashboard_home, name='dashboard_home'),  
    path('team/', dash_views.addteam, name='add_member'),  
    
    path('viewteam/', dash_views.viewTeam, name='view_member'),     
    path("team/delete/<int:pk>/", dash_views.deleteMember, name="delete_member"),
    path('team/edit/<int:pk>/', dash_views.editMember, name='edit_member'),
    # path('details/<int:agent_id>/', dash_views.agent_details, name='details'),     
    path('details/<str:type>/<int:pk>/', dash_views.details, name='details'),      
    path('verify-agent/<int:agent_id>/', dash_views.verify_agent, name='verify_agent'),        
    
    path('country/', dash_views.addCountry, name='add_country'),
    path('viewcountry/', dash_views.viewCountry, name='view_country'),
    path("country/delete/<int:pk>/", dash_views.deleteCountry, name="delete_country"),
    path('country/edit/<int:pk>/', dash_views.addCountry, name='edit_country'),
    path('propertytype/', dash_views.addPropertyType, name='add_propertytype'),
    path('viewpropertytype/', dash_views.viewPropertyType, name='view_propertytype'),
    path("propertytype/delete/<int:pk>/", dash_views.deletePropertyType, name="delete_propertytype"),
    path('propertytype/edit/<int:pk>/', dash_views.addPropertyType, name='edit_propertytype'),
    
    path('properties/<int:pk>/', dash_views.property_detail, name='property_detail'),   
    
    path('amenity/', dash_views.addAmenity, name='add_amenity'),
    path('viewamenity/', dash_views.viewAmenity, name='view_amenity'),
    path("amenity/delete/<int:pk>/", dash_views.deleteAmenity, name="delete_amenity"),
    path('amenity/edit/<int:pk>/', dash_views.addAmenity, name='edit_amenity'),
    path('company/', dash_views.addCompany, name='add_company'),
    path('viewcompany/', dash_views.viewCompany, name='view_company'),
    path("company/delete/<int:pk>/", dash_views.deleteCompany, name="delete_company"),
    path('company/edit/<int:pk>/', dash_views.addCompany, name='edit_company'),
     path('slider/', dash_views.addSlider, name='add_slider'),
    path('viewslider/', dash_views.viewSlider, name='view_slider'),
    path("slider/delete/<int:pk>/", dash_views.deleteSlider, name="delete_slider"),
    path('slider/edit/<int:pk>/', dash_views.addSlider, name='edit_slider'),
     path('blog/', dash_views.addBlog, name='add_blog'),
    path('viewblog/', dash_views.viewBlog, name='view_blog'),
    path("blog/delete/<int:pk>/", dash_views.deleteBlog, name="delete_blog"),
    path('blog/edit/<int:pk>/', dash_views.addBlog, name='edit_blog'),
     path('testimonial/', dash_views.addTestimonial, name='add_testimonial'),
    path('viewtestimonial/', dash_views.viewTestimonial, name='view_testimonial'),
    path("testimonial/delete/<int:pk>/", dash_views.deleteTestimonial, name="delete_testimonial"),
    path('testimonial/edit/<int:pk>/', dash_views.addTestimonial, name='edit_testimonial'),
    path('property/', dash_views.addProperty, name='add_property'),
    path('viewproperty/', dash_views.viewProperty, name='view_property'),
  
    path('userproperty/', dash_views.UserPropertyy, name='user_property'),
    
    # For Team User 
    path('viewuser/', dash_views.User, name='view_user'),     
    path('members/add/', dash_views.addteam, name='add_member'),        
    path('members/<int:pk>/edit/', dash_views.editMember, name='edit_member'),
    path('members/<int:pk>/delete/', dash_views.deleteMember, name='delete_member'),       
    
    path('verify-client-member/<int:agent_id>/', dash_views.verify_C_Member, name='verify_client_member'),
 
    #For Normal Jo Need for  P. CRUD -------------
    # ✅ Add New Member
    path("add-member/", dash_views.addNmember, name="add_N_member"),  

    # ✅ Edit Member
    path("edit-member/<int:pk>/", dash_views.editNMember, name="edit_N_member"),

    # ✅ Delete Member
    path("delete-member/<int:pk>/", dash_views.deleteNMember, name="delete_N_member"),    

    # ✅ View Member List
    path('viewuser/', dash_views.User, name='view_user'),
    
    path('assign-agent/', dash_views.assign_agent, name='assign_agent'),
    path("property/delete/<int:pk>/", dash_views.deleteProperty, name="delete_property"),
    path("User/property/delete/<int:pk>/", dash_views.deleteUserProperty, name="delete_user_property"),

    
# urls.py - Update these lines

    path('property/active/<int:property_id>/<int:status>/', dash_views.ActiveProperty, name='active_property'),
    path('property/update-date/<int:property_id>/', dash_views.update_property_date, name='update_property_date'), 
    path('property/edit/<int:pk>/', dash_views.editProperty, name='edit_property'),
    path("delete-property-image/<int:img_id>/", dash_views.delete_property_image, name="delete_property_image"),
    path('ajax/property-types/<int:looking_to_id>/', dash_views.get_property_types, name='get_property_types'),
    path('ajax/property-type/<int:type_id>/', dash_views.get_property_type_detail, name='get_property_type_detail'),

    path('ajax/country-info/<int:country_id>/', dash_views.get_country_info, name='get_country_info'),
    path('contact/', dash_views.Contact, name='view_contact'),
    path('profile/', dash_views.Profile, name='profile'),


    path('contact/delete/<int:pk>/', dash_views.deleteContact, name='delete_contact'),
    
    
    
    # Change by Me
    # For Update Status 
    path("update-status/<int:agent_id>/", update_status, name="update_status"),               
    
    path("update-member-status/<int:pk>/", update_member_status, name="update_member_status"),

    path("updateStatus/<int:id>/", update_P_status, name="updateStatus"),             
    path("AllupdateStatus/<int:id>/", update_PP_status, name="AllupdateStatus"),  

    # path("verify-agent/<int:agent_id>/", dash_views.verify_agent),        
     
    
    # For Role CRUD
    path('add-role/', dash_views.add_role, name='add_role'),  
    
    # For Assign Manager  
    path("assign-manager/<int:agent_id>/<int:manager_id>/", dash_views.assign_manager),  
    path('get-managers/<int:role_id>/', dash_views.get_managers, name='get_managers'),  

    # For Main User Model --------------- 
    path('add-user/', dash_views.adduser, name='add_user'),    
    path('mainUsers/', dash_views.user_list, name='user_list'),  
    
    
    # For Property Create----------------------------  
    
    path("property/add/", dash_views.add_property_wizard, name="add_property_wizard"),
    
    path("property/list/", dash_views.property_list, name="properties_list"),  
    path("property/<int:pk>/", dash_views.property_detail, name="property_detail"),        
    path("property/delete/<str:ptype>/<int:pid>/", dash_views.property_delete, name="property_delete"),
            
    path("property/view/<str:ptype>/<int:pid>/", dash_views.property_detail,),  
          
    
    # for registerUser ki Property Details total P.List
    path('client/<int:pk>/', dash_views.client_detail, name='client_detail'), 
   
   
   # -------------------------------------------------------------------------------------------------
     
     # Create + List
    path('agriculture/create/', dash_views.agriculture_create, name='agriculture_create'),
    path('agriculture/', dash_views.agriculture_list, name='agriculturee_list'),     

    # Detail + Update
    path('agriculture/<int:pk>/', dash_views.agriculture_detail, name='agriculture_detail'),
    path('agriculture/<int:pk>/edit/', dash_views.agriculture_update, name='agriculture_update'),

    # Delete Property (Property + All Media auto delete)
    path('agriculture/<int:pk>/delete/', dash_views.agriculture_delete, name='agriculture_delete'), 



   # ========================================================================================

    path('PG/create/', dash_views.add_pg_property, name='pg_create'),    
    path('PG/', dash_views.pg_list, name='PG_list'),  
    
    
  # ------------------------------------------------------------------------------------------------
  
  
    
    path('BSale/create/', dash_views.business_create, name='BSale_create'),  
    path('BSale/', dash_views.bfors_list, name='BSale_list'),
    
    
        
    
  # ------------------------------------------------------------------------------------------------
   
     path('holiday/create/', dash_views.holiday_View_create, name='holiday_create'),          
     path('holidays/', dash_views.holiday_list, name='holidays_list'),
]            

  
  