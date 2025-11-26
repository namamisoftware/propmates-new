from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import datetime


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import models
from .models import CustomUser, UserProperty, Country, Slider, RealEstateCompany, Agent, Blogs, Testimonial, PropertyType, Amenity, UserPaymentPlan,UserPropertyImage,regesteruser,Contactquery

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')   # form me 'username' ko 'email' se match karein
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_staff:  # sirf admin ya staff login kar sake
                login(request, user)
                return redirect('dashboard_home')  # dashboard ka home page
            else:
                messages.error(request, "You are not authorized!")
        else:
            messages.error(request, "Invalid email or password!")

    return render(request, "dashboard/login.html")

def dashboard_home(request):
    today = datetime.date.today()  # YYYY-MM-DD

    # Filter users created today
    today_users = regesteruser.objects.filter(created_at=today).order_by('-id')

    user_name_subquery = regesteruser.objects.filter(id=OuterRef('user')).values('name')[:1]

    # property_list = UserProperty.objects.filter(created_at=today).annotate(user_name=Subquery(user_name_subquery)).exclude(user=0).order_by('-id')
    property_list = UserProperty.objects.all()  
    totals = {
        'contact_queries': Contactquery.objects.count(),
        'properties': UserProperty.objects.filter(status=1).count(),
        'users': regesteruser.objects.count(),
        'agents': Agent.objects.count(),
        'amenities': Amenity.objects.count(),
        'blogs': Blogs.objects.count(),
        'testimonials': Testimonial.objects.count(),
        'sliders': Slider.objects.count(),
        'companies': RealEstateCompany.objects.count(),
        'buy_property': UserProperty.objects.filter(looking_to=1).count(),
        'rent_property': UserProperty.objects.filter(looking_to=2).count(),
        'new_property': UserProperty.objects.filter(looking_to=5).count(),


        
    }

    return render(request, "dashboard/dashboard.html", {'totals': totals,'todayuser':today_users,"property": property_list})


@login_required
def Profile(request):
    user = request.user  # logged-in user

    if request.method == "POST":
        if "update_profile" in request.POST:
            name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            user.full_name = name
            user.email = email
            user.phone = phone
            user.save()

            messages.success(request, "✅ Profile updated successfully!")

        elif "change_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not user.check_password(current_password):
                messages.error(request, "❌ Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "❌ New passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # keeps user logged in
                messages.success(request, "🔒 Password changed successfully!")

        return redirect("profile")  # reload page after post

    return render(request, "dashboard/profile.html", {"row": user})


# CRUD in Team Agent
def addteam(request):    

    if request.method == "POST":

        # ✅ 1. Form data copy
        form_data = request.POST.copy()

        # ✅ 2. Remove unwanted keys
        remove_keys = ['csrfmiddlewaretoken', 'imageUpload']
        for key in remove_keys:
            form_data.pop(key, None)

        # ✅ 3. Get Agent model fields
        model_fields = [field.name for field in Agent._meta.get_fields()]

        # ✅ 4. Only include fields that exist in Agent model
        clean_data = {
            key: value 
            for key, value in form_data.items() 
            if key in model_fields
        }

        # ✅ 5. Image handle
        image = request.FILES.get("imageUpload")
        if image:
            clean_data["image"] = image

        # ✅ 6. Numeric fields — convert safely
        numeric_fields = ["experience_years", "closed_deals", "rating"]
        for nf in numeric_fields:
            if nf in clean_data and clean_data[nf] != "":
                try:
                    clean_data[nf] = float(clean_data[nf])  
                except:
                    clean_data[nf] = 0

        # ✅ 7. Create Agent
        agent = Agent.objects.create(**clean_data)

        # ✅ 8. Success message
        messages.success(request, f"Team member '{agent.name}' added successfully!")
        return redirect("view_member")

    # ✅ GET request: load roles
    roles = RoleModel.objects.all()
    return render(request, "dashboard/ourteam.html", {"roles": roles})   
  



def editMember(request, pk):
    member = get_object_or_404(Agent, pk=pk)

    if request.method == "POST":
        # Convert POST data to a dict
        from_data = request.POST.dict()

        # Remove keys that are not model fields
        ignore_keys = ['csrfmiddlewaretoken', 'imageUpload']
        for key in ignore_keys:
            from_data.pop(key, None)

        # Update all fields dynamically
        for key, value in from_data.items():
            setattr(member, key, value)

        # Handle new image if uploaded
        image = request.FILES.get('imageUpload')
        if image:
            member.image = image

        member.save()
        messages.success(request, f"Member '{member.name}' updated successfully!")
        return redirect("view_member")  # ✅ redirect to member list

    context = {"member": member}
    return render(request, "dashboard/ourteam.html", context)   
def viewTeam(request):  
    agents = Agent.objects.all().order_by('-id')      
    roles = RoleModel.objects.all()
    return render(request, "dashboard/view_team.html", {"agents": agents, "roles": roles})

def deleteMember(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent.delete()
    messages.success(request, f"Member '{agent.name}' deleted successfully!")
    return redirect("view_member")
from django.shortcuts import render, redirect, HttpResponse
# def agent_details(request, agent_id):  
#     # agent_id से agent की जानकारी लो
#     agent = get_object_or_404(Agent, id=agent_id)       
#     context = {
#         "agent": agent
#     }
#     return render(request, "dashboard/agent_details.html", context)     
def details(request, type, pk):  
    if type == "agent":
        agent = get_object_or_404(Agent, pk=pk)
        return render(request, "dashboard/agent_details.html", {"agent": agent})
    elif type == "member":
        member = get_object_or_404(regesteruser, pk=pk)
        return render(request, "dashboard/member_details.html", {"member": member})
    else:
        return HttpResponse("Invalid type", status=400)      










# CRUD in Normal Agent
def addNmember(request):        
    if request.method == "POST":
        form_data = request.POST.copy()

        remove_keys = ['csrfmiddlewaretoken', 'imageUpload']
        for key in remove_keys:
            form_data.pop(key, None)

        # ✅ Use correct model here
        model_fields = [field.name for field in regesteruser._meta.get_fields()]

        clean_data = {
            key: value 
            for key, value in form_data.items() 
            if key in model_fields
        }
        # ✅ Convert company ID to object
        company_id = clean_data.get("company")  
        if company_id:
           clean_data["company"] = RealEstateCompany.objects.get(id=company_id)
           
        image = request.FILES.get("imageUpload")
        if image:
            clean_data["image"] = image

        numeric_fields = ["experience_years", "closed_deals", "rating"]
        for nf in numeric_fields:
            if nf in clean_data and clean_data[nf] != "":
                try:
                    clean_data[nf] = float(clean_data[nf])
                except:
                    clean_data[nf] = 0

        # ✅ Create correct model object
        agent = regesteruser.objects.create(**clean_data)

        messages.success(request, f"Team member '{agent.name}' added successfully!")
        return redirect("view_user")  

    companies = RealEstateCompany.objects.all()
    return render(request, "dashboard/add_Normal_U.html", {"companies": companies})
  



def editNMember(request, pk):
    member = get_object_or_404(regesteruser, pk=pk)    

    if request.method == "POST":
        # Convert POST data to a dict
        from_data = request.POST.dict()

        # Remove keys that are not model fields
        ignore_keys = ['csrfmiddlewaretoken', 'imageUpload']
        for key in ignore_keys:
            from_data.pop(key, None)

        # Update all fields dynamically
        for key, value in from_data.items():
            setattr(member, key, value)

        # Handle new image if uploaded
        image = request.FILES.get('imageUpload')
        if image:
            member.image = image

        member.save()
        messages.success(request, f"Member '{member.name}' updated successfully!")
        return redirect("view_user")  # ✅ redirect to member list
   
    context = {"member": member}
    return render(request, "dashboard/ourteam.html", context)   





def User(request):
    user = regesteruser.objects.all().order_by('-id')
    
    # Sirf wo agents jo manage_user_property ya is_subadmin hai
    agents = Agent.objects.all().order_by('-id')
    
    return render(request, "dashboard/view_user.html", {
        "user": user,
        "agents": agents   
    }) 
    
    
    
    
     

def deleteNMember(request, pk):  
    agent = get_object_or_404(regesteruser, pk=pk)        
    agent.delete()
    messages.success(request, f"Member '{agent.name}' deleted successfully!")
    return redirect("view_user")











def addCountry(request, pk=None):
  
    if pk:
        row = get_object_or_404(Country, pk=pk)
    else:
        row = None

    if request.method == "POST":
        from_data = request.POST.dict()  # convert QueryDict to dict

        # Remove csrf token
        from_data.pop('csrfmiddlewaretoken', None)

        if row:  # Edit
            for key, value in from_data.items():
                setattr(row, key, value)
            row.save()
            messages.success(request, f"Country '{row.name}' updated successfully!")
        else:  # Add
            Country.objects.create(**from_data)
            messages.success(request, f"Country '{from_data.get('name')}' added successfully!")

        return redirect("view_country")

    context = {"row": row}
    return render(request, "dashboard/country.html", context)



def viewCountry(request):
    country = Country.objects.all().order_by('-id')  
    return render(request, "dashboard/view_country.html", {"country": country})

def deleteCountry(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    messages.success(request, f"Country deleted successfully!")
    return redirect("view_country")

def addPropertyType(request, pk=None):
    # Fetch row if editing
    if pk:
        row = get_object_or_404(PropertyType, pk=pk)
    else:
        row = None

    # Define categories for dropdown
    categories = [
        (1, 'Buy'),
        (2, 'Rent'),
        (3, 'Commercial Buy'),
        (4, 'Commercial Rent'),
        (5, 'New Project')
    ]

    if request.method == "POST":
        from_data = request.POST.dict()  # convert QueryDict to dict
        from_data.pop('csrfmiddlewaretoken', None)

        if row:  # Edit
            for key, value in from_data.items():
                setattr(row, key, value)
            row.save()
            messages.success(request, f"Property Type '{row.name}' updated successfully!")
        else:  # Add
            PropertyType.objects.create(**from_data)
            messages.success(request, f"Property Type '{from_data.get('name')}' added successfully!")

        return redirect("view_propertytype")

    context = {
        "row": row,
        "categories": categories,  # pass categories to template
    }
    return render(request, "dashboard/propertytype.html", context)

def viewPropertyType(request):
    property_types = PropertyType.objects.all().order_by('-id')  # descending by id
    return render(request, "dashboard/view_propertytype.html", {"PropertyType": property_types})
def deletePropertyType(request, pk):
    property_type = get_object_or_404(PropertyType, pk=pk)  # fetch instance
    property_type.delete()  # delete the instance
    messages.success(request, "Property Type deleted successfully!")
    return redirect("view_propertytype")
def addAmenity(request, pk=None):
  
    if pk:
        row = get_object_or_404(Amenity, pk=pk)
    else:
        row = None

    if request.method == "POST":
        from_data = request.POST.dict()  # convert QueryDict to dict

        # Remove csrf token
        from_data.pop('csrfmiddlewaretoken', None)

        if row:  # Edit
            for key, value in from_data.items():
                setattr(row, key, value)
            row.save()
            messages.success(request, f"Amenity '{row.name}' updated successfully!")
        else:  # Add
            Amenity.objects.create(**from_data)
            messages.success(request, f"Amenity '{from_data.get('name')}' added successfully!")

        return redirect("view_amenity")

    context = {"row": row}
    return render(request, "dashboard/amenities.html", context)



def viewAmenity(request):
    Amenities = Amenity.objects.all().order_by('-id')  
    return render(request, "dashboard/view_amenities.html", {"amenity": Amenities})

def deleteAmenity(request, pk):
    Amenities = get_object_or_404(Amenity, pk=pk)
    Amenities.delete()
    messages.success(request, f"Amenity deleted successfully!")
    return redirect("view_amenity")
def addCompany(request, pk=None):
    if pk:
        company = get_object_or_404(RealEstateCompany, pk=pk)
    else:
        company = None

    if request.method == "POST":
        # Convert POST data to dict
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)  # Remove CSRF token

        # Handle image upload
        image = request.FILES.get('imageUpload')
        if image:
            form_data['image'] = image

        if company:  # Edit
            for key, value in form_data.items():
                setattr(company, key, value)
            company.save()
            messages.success(request, f"Company '{company.name}' updated successfully!")
        else:  # Add
            RealEstateCompany.objects.create(**form_data)
            messages.success(request, f"Company '{form_data.get('name')}' added successfully!")

        return redirect("view_company")

    context = {"row": company}
    return render(request, "dashboard/add_company.html", context)

def viewCompany(request):
    company = RealEstateCompany.objects.all().order_by('-id')  
    return render(request, "dashboard/view_company.html", {"company": company})

def deleteCompany(request, pk):
    company = get_object_or_404(RealEstateCompany, pk=pk)
    company.delete()
    messages.success(request, f"Company deleted successfully!")
    return redirect("view_company")

def addSlider(request, pk=None):
    if pk:
        slider = get_object_or_404(Slider, pk=pk)
    else:
        slider = None

    if request.method == "POST":
        # Convert POST data to dict
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)  # Remove CSRF token

        # Handle image upload
        image = request.FILES.get('imageUpload')
        if image:
            form_data['image'] = image

        if slider:  # Edit
            for key, value in form_data.items():
                setattr(slider, key, value)
            slider.save()
            messages.success(request, f"slider '{slider.title}' updated successfully!")
        else:  # Add
            Slider.objects.create(**form_data)
            messages.success(request, f"slider '{form_data.get('title')}' added successfully!")

        return redirect("view_slider")

    context = {"row": slider}
    return render(request, "dashboard/slider.html", context)

def viewSlider(request):
    slider = Slider.objects.all().order_by('-id')  
    return render(request, "dashboard/view_slider.html", {"slider": slider})

def deleteSlider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    slider.delete()
    messages.success(request, f"slider deleted successfully!")
    return redirect("view_slider")
def addBlog(request, pk=None):
    if pk:
        blog = get_object_or_404(Blogs, pk=pk)
    else:
        blog = None

    if request.method == "POST":
        # Convert POST data to dict
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)  # Remove CSRF token

        # Handle image upload
        image = request.FILES.get('imageUpload')
        if image:
            form_data['image'] = image

        if blog:  # Edit
            for key, value in form_data.items():
                setattr(blog, key, value)
            blog.save()
            messages.success(request, f"Blog '{blog.title}' updated successfully!")
        else:  # Add
            Blogs.objects.create(**form_data)
            messages.success(request, f"Blog '{form_data.get('title')}' added successfully!")

        return redirect("view_blog")

    context = {"row": blog}
    return render(request, "dashboard/blog.html", context)

def viewBlog(request):
    blog = Blogs.objects.all().order_by('-id')  
    return render(request, "dashboard/view_blog.html", {"blog": blog})

def deleteBlog(request, pk):
    blog = get_object_or_404(Blogs, pk=pk)
    blog.delete()
    messages.success(request, f"blog deleted successfully!")
    return redirect("view_blog")
def addTestimonial(request, pk=None):
    if pk:
        testimonial = get_object_or_404(Testimonial, pk=pk)
    else:
        testimonial = None

    if request.method == "POST":
        # Convert POST data to dict
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)  # Remove CSRF token

        # Handle image upload
        image = request.FILES.get('imageUpload')
        if image:
            form_data['image'] = image

        if testimonial:  # Edit
            for key, value in form_data.items():
                setattr(testimonial, key, value)
            testimonial.save()
            messages.success(request, f"Testimonial '{testimonial.name}' updated successfully!")
        else:  # Add
            Testimonial.objects.create(**form_data)
            messages.success(request, f"Testimonial '{form_data.get('name')}' added successfully!")

        return redirect("view_testimonial")

    context = {"row": testimonial}
    return render(request, "dashboard/testimonial.html", context)

def viewTestimonial(request):
    testimonial = Testimonial.objects.all().order_by('-id')  
    return render(request, "dashboard/view_testimonial.html", {"testimonial": testimonial})

def deleteTestimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, f"Testimonial deleted successfully!")
    return redirect("view_testimonial")



def addProperty(request, pk=None):
    """Add or Edit Property"""
    property_obj = get_object_or_404(UserProperty, pk=pk) if pk else None

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        # Country + Currency
        country = Country.objects.filter(id=data.get('country')).first()
        currency = country.currency if country else None

        # Required: looking_to
        looking_to = data.get('looking_to')
        if not looking_to or looking_to == "0":
            messages.error(request, "Please select what you are looking to.")
            return redirect(request.path)

        # Company and Property Type
        company = None
        if data.get('company_id'):
            company = RealEstateCompany.objects.filter(id=data.get('company_id')).first()

        property_type = None
        if data.get('property_type'):
            property_type = PropertyType.objects.filter(id=data.get('property_type')).first()

        # Helper to safely convert to int
        def safe_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return 0

        # Collect all property fields
        property_fields = {
            'name': data.get('name'),
            'city': data.get('city'),
            'locality': data.get('locality'),
            'sub_locality': data.get('sub_locality'),
            'apartment_name': data.get('apartment_name'),
            'address': data.get('address'),
            'bedrooms': safe_int(data.get('bedrooms')),
            'bathrooms': safe_int(data.get('bathrooms')),
            'balconies': safe_int(data.get('balconies')),
            'carpet_area': safe_int(data.get('carpet_area')),
            'area_unit': data.get('area_unit'),
            'lease': data.get('lease'),
            'available': data.get('available_from'),
            'rent_type': data.get('rent_type'),
            'rent_price': data.get('rent_price'),
            'maintenance_price': data.get('maintenance_price'),
            'possession': data.get('possession'),
            'possession_date': data.get('possession_date'),
            'available_date': data.get('available_date'),
            'ploat_area': data.get('ploat_area'),
            'ploat_no': data.get('ploat_no'),
            'loan': data.get('loan_available'),
            'builtup_area': safe_int(data.get('builtup_area')),
            'super_builtup_area': safe_int(data.get('super_builtup_area')),
            'furnishing_status': data.get('furnishing_status'),
            'expected_price': safe_int(data.get('expected_price')),
            'all_inclusive': bool(data.get('all_inclusive')),
            'price_negotiable': bool(data.get('price_negotiable')),
            'description': data.get('description'),
            'parking_spaces': safe_int(data.get('parking_spaces')),
            'parking_type': data.get('parking_type'),
            'facing': data.get('facing'),
            'latitude': data.get('latitude') or None,
            'longitude': data.get('longitude') or None,
            'looking_to': looking_to,
            'country': country,
            'currency': currency,
            'company': company,
            'property_type': property_type,
            'status':1
            
        }

        # Create or Update Property
        if property_obj:
            for key, value in property_fields.items():
                setattr(property_obj, key, value)
            property_obj.save()
            message_text = f"Property '{property_obj.name}' updated successfully!"
        else:
            property_obj = UserProperty.objects.create(**property_fields)
            message_text = f"Property '{property_obj.name}' added successfully!"

        # Handle Images
        if 'images' in files:
            for img in files.getlist('images'):
                UserPropertyImage.objects.create(property=property_obj, image=img)

        # Handle Video
        if 'video' in files:
            property_obj.video = files['video']

        # Handle Brochure
        if 'brochure' in files:
            property_obj.brochure = files['brochure']
        if 'image1' in files:
            property_obj.image1 = files['image1']
        if 'image2' in files:
            property_obj.image2 = files['image2']

        if 'image3' in files:
            property_obj.image3 = files['image3']

        property_obj.save()

        # Handle Amenities
        amenities_ids = data.getlist('amenities')
        if amenities_ids:
            property_obj.amenities.set(amenities_ids)

        # Handle Payment Plans
        UserPaymentPlan.objects.filter(property=property_obj).delete()
        plan_names = data.getlist('payment_name[]')
        plan_amounts = data.getlist('payment_amount[]')
        for name, amount in zip(plan_names, plan_amounts):
            if name and amount:
                UserPaymentPlan.objects.create(
                    property=property_obj,
                    payment_name=name,
                    payment_amount=safe_int(amount)
                )

        messages.success(request, message_text)
        return redirect("view_property")

    context = {
        "row": property_obj,
        "countries": Country.objects.all(),
        "companies": RealEstateCompany.objects.all(),
        "property_types": PropertyType.objects.all(),  
        "amenities": Amenity.objects.all(),  
    }
    return render(request, "dashboard/property.html", context)


def editProperty(request, pk):
    """Edit Existing Property"""
    property_obj = get_object_or_404(UserProperty, pk=pk)
    categories = [
        (1, 'Buy'),
        (2, 'Rent'),
        (3, 'Commercial Buy'),
        (4, 'Commercial Rent'),
        (5, 'New Project')
    ]

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        # Get related objects
        country = Country.objects.filter(id=data.get('country')).first()
        currency = country.currency if country else None

        looking_to = data.get('looking_to')
        if not looking_to:
            messages.error(request, "Please select what you are looking to.")
            return redirect(request.path)

        company = RealEstateCompany.objects.filter(id=data.get('company_id')).first() if data.get('company_id') else None
        property_type = PropertyType.objects.filter(id=data.get('property_type')).first() if data.get('property_type') else None

        def safe_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return 0

        # ✅ Update property fields
        property_fields = {
            'name': data.get('name'),
            'city': data.get('city'),
            'locality': data.get('locality'),
            'sub_locality': data.get('sub_locality'),
            'apartment_name': data.get('apartment_name'),
            'address': data.get('address'),
            'bedrooms': safe_int(data.get('bedrooms')),
            'bathrooms': safe_int(data.get('bathrooms')),
            'balconies': safe_int(data.get('balconies')),
            'carpet_area': data.get('carpet_area'),
            'area_unit': data.get('area_unit'),
            'lease': data.get('lease'),
            'available_from': data.get('available_from'),
            'rent_type': data.get('rent_type'),
            'rent_price': safe_int(data.get('rent_price')),
            'maintenance_price': data.get('maintenance_price'),
            'possession': data.get('possession'),
            'possession_date': data.get('possession_date'),
            'available_date': data.get('available_date'),
            'ploat_area': data.get('ploat_area'),
            'ploat_no': data.get('ploat_no'),
            'loan_available': data.get('loan_available'),

            'builtup_area': data.get('builtup_area'),
            'super_builtup_area': data.get('super_builtup_area'),
            'furnishing_status': data.get('furnishing_status'),
            'expected_price': safe_int(data.get('expected_price')),
            'all_inclusive': bool(data.get('all_inclusive')),
            'price_negotiable': bool(data.get('price_negotiable')),
            'description': data.get('description'),
            'parking_spaces': data.get('parking_spaces'),
            'parking_type': data.get('parking_type'),
            'facing': data.get('facing'),
            'latitude': data.get('latitude') or None,
            'longitude': data.get('longitude') or None,
            'looking_to': looking_to,
            'country': country,
            'currency': currency,
            'company': company,
            'property_type': property_type,
            # 'user':"0"
        }

        for key, value in property_fields.items():
            setattr(property_obj, key, value)

        # ✅ Handle single file fields
        for img_field in ['image1', 'image2', 'image3', 'video', 'brochure']:
            if img_field in files:
                setattr(property_obj, img_field, files[img_field])

        # ✅ Handle multiple image uploads
        if 'images' in files:
            for img in files.getlist('images'):
                UserPropertyImage.objects.create(property=property_obj, image=img)

        property_obj.save()

        # ✅ Amenities (ManyToMany)
        selected_amenities = data.getlist('amenities')
        property_obj.amenities.set(selected_amenities)

        # ✅ Payment Plans
        UserPaymentPlan.objects.filter(property=property_obj).delete()
        plan_names = data.getlist('payment_name[]')
        plan_amounts = data.getlist('payment_amount[]')
        for name, amount in zip(plan_names, plan_amounts):
            if name and amount:
                UserPaymentPlan.objects.create(
                    property=property_obj,
                    payment_name=name,
                    payment_amount=amount
                )

        messages.success(request, f"Property '{property_obj.name}' updated successfully!")
        return redirect("view_property")

    # ✅ GET Request — prefill data
    context = {
        "row": property_obj,
        "categories": categories,
        "countries": Country.objects.all(),
        "companies": RealEstateCompany.objects.all(),
        "property_types": PropertyType.objects.all(),
        "amenities": Amenity.objects.all(),

        # Extra context for existing data
        "property_images": UserPropertyImage.objects.filter(property=property_obj),
        "selected_amenities": property_obj.amenities.values_list('id', flat=True),
        "payment_plans": UserPaymentPlan.objects.filter(property=property_obj),
    }

    return render(request, "dashboard/edit_property.html", context)


def viewProperty(request):
    property_list = UserProperty.objects.select_related('property_type', 'country') \
        .filter(user=None) \
        .order_by('-id')
    return render(request, "dashboard/view_property.html", {"property": property_list})

# def property_detail(request, pk):
#     property = get_object_or_404(UserProperty, pk=pk)  
#     return render(request, 'dashboard/property_detail.html', {'property': property})  






def delete_property_image(request, img_id):
    image = get_object_or_404(UserPropertyImage, id=img_id)
    property_id = image.property.id
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect("edit_property", pk=property_id)

def deleteProperty(request, pk):
    property = get_object_or_404(UserProperty, pk=pk)
    property.delete()
    messages.success(request, f"property deleted successfully!")
    return redirect("view_property")

def deleteUserProperty(request, pk):
    property = get_object_or_404(UserProperty, pk=pk)
    property.delete()
    messages.success(request, f"property deleted successfully!")
    return redirect("user_property")

# def ActiveProperty(request, pk, status):
#     property_obj = get_object_or_404(UserProperty, pk=pk)
#     property_obj.status = status
#     property_obj.save()

#     if status == 1:
#         messages.success(request, f"✅ Property activated successfully!")
#     else:
#         messages.warning(request, f"⚠️ Property deactivated successfully!")

#     return redirect("user_property")



def ActiveProperty(request, property_id, status):
    try:
        property_obj = UserProperty.objects.get(id=property_id)
       
        # If approving (status == 1), get expire_date from request
        if status == 1:
            expire_date_str = request.GET.get('expire_date')
            print(f"Expire date received: {expire_date_str}")  # Debug
            
            if expire_date_str:
                try:
                    property_obj.expire_at = datetime.strptime(expire_date_str, '%Y-%m-%d').date()
                    print(f"Date parsed successfully: {property_obj.expire_at}")  # Debug
                except ValueError as ve:
                    messages.error(request, f'Invalid date format: {str(ve)}')
                    return redirect('user_property')
            else:
                messages.warning(request, 'No expiration date provided!')
       
        property_obj.status = status
        property_obj.save()
        print(f"Property saved - ID: {property_obj.id}, Status: {property_obj.status}, Expire: {property_obj.expire_at}")  # Debug
       
        if status == 1:
            messages.success(request, f'Property approved successfully! Expiration date: {property_obj.expire_at}')
        elif status == 2:
            messages.success(request, 'Property rejected successfully!')
           
    except UserProperty.DoesNotExist:
        messages.error(request, 'Property not found!')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        print(f"Exception occurred: {str(e)}")  # Debug
   
    return redirect('user_property')


def update_property_date(request, property_id):
    try:
        property_obj = get_object_or_404(UserProperty, id=property_id)
       
        expire_date_str = request.GET.get('expire_date')
        print(f"Update - Expire date received: {expire_date_str}")  # Debug
        print(f"Old expire date: {property_obj.expire_at}")  # Debug
        
        if expire_date_str:
            try:
                property_obj.expire_at = datetime.strptime(expire_date_str, '%Y-%m-%d').date()
                property_obj.save()
                print(f"New expire date: {property_obj.expire_at}")  # Debug
                messages.success(request, f'Expiration date updated successfully to {property_obj.expire_at}!')
            except ValueError as ve:
                messages.error(request, f'Invalid date format: {str(ve)}')
        else:
            messages.error(request, 'Please provide a valid expiration date!')
           
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        print(f"Exception in update: {str(e)}")  # Debug
   
    return redirect('user_property')

def get_property_types(request, looking_to_id):
    """Return property types filtered by 'looking_to' choice."""
    types = PropertyType.objects.filter(looking_to=looking_to_id).values('id', 'name','plot')
    return JsonResponse(list(types), safe=False)
def get_property_type_detail(request, type_id):
    """Return details for one property type (used when user selects type)."""
    try:
        ptype = PropertyType.objects.get(id=type_id)
        return JsonResponse({
            'id': ptype.id,
            'name': ptype.name,
            'plot': ptype.plot
        })
    except PropertyType.DoesNotExist:
        return JsonResponse({'error': 'Property type not found'}, status=404)
def get_country_info(request, country_id):
    country = Country.objects.filter(id=country_id).first()
    if country:
        return JsonResponse({
            'name': country.name,
            'currency': country.currency or ''
        })
    return JsonResponse({'name': '', 'currency': ''})
def UserPropertyy(request):
    # Subquery to get the user's name based on user_id
    user_name_subquery = regesteruser.objects.filter(id=OuterRef('user')).values('name')[:1]

    property_list = UserProperty.objects.all().annotate(user_name=Subquery(user_name_subquery)).exclude(user=0).order_by('-id')

    return render(request, "dashboard/user_property.html", {"property": property_list})

   
  
@csrf_exempt
def assign_agent(request):  
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            agent_id = data.get('agent_id')
            
            # User aur Agent ko fetch karein
            user = regesteruser.objects.get(id=user_id)
            agent = Agent.objects.get(id=agent_id)
            
            # Check karein ki agent ke paas permission hai ya nahi
            if not (agent.manage_user_property or agent.is_subadmin):
                return JsonResponse({
                    'success': False,
                    'message': 'This agent does not have permission to manage users'
                })
            
            # Agent assign karein
            user.assign_id = agent.id
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Agent assigned successfully'
            })
            
        except regesteruser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            })
        except Agent.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Agent not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    rows = regesteruser.objects.select_related('assign_id').all()  
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method',  
        'rows': rows  
    })

def Contact(request):
    contact_list = Contactquery.objects.all().order_by('-id')
    return render(request, "dashboard/Contactquery.html", {"contact": contact_list})

def deleteContact(request, pk):
    contact = get_object_or_404(Contactquery, pk=pk)
    contact.delete()
    messages.success(request, f"Contact Query deleted successfully!")
    return redirect("view_contact")

def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin_login')




# Agent Verify Hone pr ye chalega   -----------       
from django.http import JsonResponse
from .models import Agent, CustomUser, RoleModel

# Our Team Memeber Users. --------------------------------------------
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

# Claints Users ----------------------------------------------------
def verify_C_Member(request, agent_id):  
    C_Member = regesteruser.objects.get(id=agent_id)

    user = CustomUser.objects.create_user(
        email=C_Member.email,
        full_name=C_Member.name,
        phone=C_Member.phone,
        password=C_Member.password,  # password hashing handled by create_user()
    )
  
    user.save()

    C_Member.user = user     # ✅ link agent with new user
    C_Member.save()

    return JsonResponse({"success": True})   



from django.http import JsonResponse  
from .models import Agent, CustomUser

def get_managers(request, role_id):

    # 1️⃣ Get agent
    agent = Agent.objects.get(id=role_id)  

    # 2️⃣ Fetch managers from CustomUser table
    managers = CustomUser.objects.filter(
        role__role="manager",        
        is_active=True,
        state=agent.Pstate,   
        # city=agent.Pcity,
        # pincode=agent.Ppincode   
    )
    print(managers)   
    # 3️⃣ Prepare JSON output
    data = [
        {"id": m.id, "name": m.email}              
        for m in managers
    ]

    return JsonResponse(data, safe=False)



# Role Add
from django.shortcuts import render, redirect
from .models import RoleModel

def add_role(request):

    if request.method == "POST":
        role_name = request.POST.get("role").strip()

        # ✅ validations
        if role_name == "":
            messages.error(request, "Role field cannot be empty.")
            return redirect("add_role")

        # ✅ check duplicate
        if RoleModel.objects.filter(role__iexact=role_name).exists():
            messages.warning(request, f"Role '{role_name}' already exists.")
            return redirect("add_role")

        # ✅ create role
        RoleModel.objects.create(role=role_name)

        messages.success(request, f"Role '{role_name}' added successfully!")
        return redirect("add_role")
    roles = RoleModel.objects.all
    return render(request, "dashboard/add_role.html", {"roles": roles})    
            
 
# For Assign manager  
def assign_manager(request, agent_id, manager_id):

    agent = Agent.objects.get(id=agent_id)
    manager = CustomUser.objects.get(id=manager_id)

    agent.manager = manager
    agent.save()

    return JsonResponse({"success": True})




# Main User Model Me Add ke Liye   

from django.shortcuts import render, redirect
from .models import CustomUser, RoleModel

def adduser(request):

    if request.method == "POST":
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        country = request.POST.get('Country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        role_id = request.POST.get('role')
        password = request.POST.get('password')   # ✅ User entered password

        # ✅ User Create
        user = CustomUser(
            email=email,
            full_name=full_name,
            phone=phone,
            Country=country,
            state=state,
            city=city,
            pincode=pincode,
            role_id=role_id
        )

        # ✅ Save user-entered password
        user.set_password(password)

        user.save()

        return redirect('dashboard/home')

    # Dropdown: fetch roles
    roles = RoleModel.objects.all()
    return render(request, 'dashboard/ADDUSER.html', {'roles': roles})  


# Get Show Main User -------
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/main-user-list.html', {'users': users})    




from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import (
    CommercialProperty, ResidentialProperty, PropertyImage,
    Office, Shop, Showroom, Warehouse, Factory, CommercialLand,
    Apartment, Villa, Townhouse, Studio, Penthouse, Duplex, Compound, ResidentialPlot
)




#              Updated                ---------------------------


def add_property_wizard(request):  
    """Multi-step property creation wizard — saves data to DB only at the final step."""
    
    step = request.GET.get("step", "category")
    category = request.GET.get("category")

    # -------------------------------------------------------
    # 🧭 INIT SESSION DATA
    # -------------------------------------------------------
    if "property_wizard" not in request.session:
        request.session["property_wizard"] = {}
    wizard_data = request.session["property_wizard"]

    # -------------------------------------------------------
    # ✅ STEP 1 — CATEGORY SELECTION
    # -------------------------------------------------------
    if step == "category":
        request.session["property_wizard"] = {}  # clear previous wizard
        return render(request, "dashboard/add_property_wizard.html", {"step": "category"})

    # -------------------------------------------------------
    # ✅ STEP 2 — BASIC DETAILS (Title, Description, Price)
    # -------------------------------------------------------
    if step == "base1":
        if request.method == "POST":
            wizard_data.update({
                "category": category,
                "title": request.POST.get("title"),
                "description": request.POST.get("description"),
                "subtype": request.POST.get("subtype"),
                "price": request.POST.get("price"),
                "price_type": request.POST.get("price_type"),

                # ✅ New Fields
                "furnishing": request.POST.get("furnishing"),
                "parking_spaces": request.POST.get("parking_spaces"),
                "washrooms": request.POST.get("washrooms"),
                "pantry": request.POST.get("pantry") == "on",
                "deposit_amount": request.POST.get("deposit_amount"),
                "maintenance_fees": request.POST.get("maintenance_fees"),
                "service_charge_included": request.POST.get("service_charge_included") == "on",
                "available_from": request.POST.get("available_from"),
                "property_status": request.POST.get("property_status"),
                "ownership_type": request.POST.get("ownership_type"),
                "featured": request.POST.get("featured") == "on",
                # New Fields
                "bedrooms": request.POST.get("bedrooms"),
                "bathrooms": request.POST.get("bathrooms"),
                "balcony": request.POST.get("balcony") == "on",
                "view": request.POST.get("view"),
                
                  
                  # ✅ Foreign Keys (store ID only)
                "agent": request.POST.get("agent"),
                "property_type": request.POST.get("property_type"),

                 # ✅ M2M (store list of IDs)
                "amenities": request.POST.getlist("amenities")   
                 
            })
         
            request.session.modified = True
            return redirect(f"/dashboard/property/add/?step=base2")

        amenities = Amenity.objects.all()
        return render(request, "dashboard/add_property_wizard.html", {
            "step": "base1",
            "category": category,
            "amenities": amenities,
            "property_types": PropertyType.objects.all(),
            "agents": Agent.objects.all(),
        })

    # -------------------------------------------------------
    # ✅ STEP 3 — LOCATION DETAILS
    # -------------------------------------------------------
    if step == "base2":
        if request.method == "POST":
            wizard_data.update({
                "selectedAddress": request.POST.get("selectedAddress"),
                "latitude": request.POST.get("latitude"),
                "longitude": request.POST.get("longitude"),
                "area_sqft": request.POST.get("area_sqft"),
                "super_area": request.POST.get("super_area"),

                "country": request.POST.get("country"),
                "city": request.POST.get("city"),
                "locality": request.POST.get("locality"),
                "sub_locality": request.POST.get("sub_locality"),
            })
            request.session.modified = True
            return redirect("/dashboard/property/add/?step=subtype_form")

        return render(request, "dashboard/add_property_wizard.html", {
            "step": "base2",
            "category": wizard_data.get("category")
        })

    # -------------------------------------------------------
    # ✅ STEP 4 — SUBTYPE-SPECIFIC FORM (SAVE IN SESSION ONLY)
    # -------------------------------------------------------
    if step == "subtype_form":
        subtype = request.GET.get("subtype") or wizard_data.get("subtype")

        if request.method == "POST":
            wizard_data["subtype"] = subtype
            form_data = request.POST.dict()
            form_data.pop("csrfmiddlewaretoken", None)
            wizard_data["subtype_form_data"] = form_data
            request.session.modified = True

            subtype_model_map = {
                "office": "Office",
                "shop": "Shop",
                "showroom": "Showroom",
                "warehouse": "Warehouse",
                "factory": "Factory",
                "commercialland": "CommercialLand",
                "apartment": "Apartment",
                "villa": "Villa",
                "townhouse": "Townhouse",
                "studio": "Studio",
                "penthouse": "Penthouse",
                "duplex": "Duplex",
                "compound": "Compound",
                "residentialplot": "ResidentialPlot",
            }
            wizard_data["subtype_model_name"] = subtype_model_map.get(subtype.lower())
            request.session.modified = True

            return redirect("/dashboard/property/add/?step=images")

        return render(request, "dashboard/add_property_wizard.html", {
            "step": "subtype_form",
            "subtype": subtype,
            "category": wizard_data.get("category"),
            "form_data": wizard_data.get("subtype_form_data", {}),
        })

    # -------------------------------------------------------
    # ✅ STEP 5 — IMAGES & FINAL SAVE
    # -------------------------------------------------------
    if step == "images":
        if request.method == "POST":
            images = request.FILES.getlist("images")
            image_360 = request.FILES.get("image_360")
            video_url = request.POST.get("video_url")
            video_file = request.FILES.get("video_file")

            wizard_data["images"] = [img.name for img in images]
            wizard_data["video_url"] = video_url
            request.session.modified = True

            category = wizard_data.get("category")
            subtype = wizard_data.get("subtype")

            # -------------------------------
            # 1️⃣ Base Property Save
            # -------------------------------
            base_model = CommercialProperty if category == "commercial" else ResidentialProperty

            # 🧹 Safe float conversion
            def to_float(val):
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return None

            base = base_model.objects.create(
                title=wizard_data.get("title"),
                description=wizard_data.get("description"),
                category=category,
                subtype=subtype,
                price=to_float(wizard_data.get("price")),
                price_type=wizard_data.get("price_type", "fixed"),
                furnishing=wizard_data.get("furnishing"),
                parking_spaces=wizard_data.get("parking_spaces") or 0,
                washrooms=wizard_data.get("washrooms") or 0,
                pantry=wizard_data.get("pantry"),
                deposit_amount=to_float(wizard_data.get("deposit_amount")),
                maintenance_fees=to_float(wizard_data.get("maintenance_fees")),
                service_charge_included=wizard_data.get("service_charge_included"),
                available_from=wizard_data.get("available_from") or None,
                property_status=wizard_data.get("property_status"),
                ownership_type=wizard_data.get("ownership_type"),
                featured=wizard_data.get("featured"),
                map_address=wizard_data.get("selectedAddress"),
                latitude=wizard_data.get("latitude"),
                longitude=wizard_data.get("longitude"),
                area_sqft=to_float(wizard_data.get("area_sqft")),
                super_area=to_float(wizard_data.get("super_area")),
                country=wizard_data.get("country"),
                city=wizard_data.get("city"),
                locality=wizard_data.get("locality"),
                sub_locality=wizard_data.get("sub_locality"),
                
                      

                agent_id=wizard_data["agent"],                            # ✅ FK via ID
                property_type_id=wizard_data["property_type"],  # ✅ FK via ID 
               

                 )
            base.amenities.set(wizard_data["amenities"])  
#    
            # -------------------------------
            # 2️⃣ Subtype Model Save
            # -------------------------------
            commercial = {
                "office": Office,
                "shop": Shop,
                "showroom": Showroom,
                "warehouse": Warehouse,
                "factory": Factory,
                "commercialland": CommercialLand,
            }
            residential = {
                "apartment": Apartment,
                "villa": Villa,
                "townhouse": Townhouse,
                "studio": Studio,
                "penthouse": Penthouse,
                "duplex": Duplex,
                "compound": Compound,
                "residentialplot": ResidentialPlot,
            }

            model_class = commercial.get(subtype) if category == "commercial" else residential.get(subtype)
            if model_class:
                subtype_form_data = wizard_data.get("subtype_form_data", {})
                subtype_form_data.pop("csrfmiddlewaretoken", None)

                clean_data = {}
                for k, v in subtype_form_data.items():
                    if v == "on":
                        clean_data[k] = True
                    elif v in ["", None]:
                        clean_data[k] = None
                    else:
                        clean_data[k] = v
                model_class.objects.create(property=base, **clean_data)

            # -------------------------------
            # 3️⃣ Property Images Save
            # -------------------------------
            ct = ContentType.objects.get_for_model(base)
            for img in images:
                PropertyImage.objects.create(content_type=ct, object_id=base.pk, image=img)
            if image_360:
                PropertyImage.objects.create(content_type=ct, object_id=base.pk, image=image_360, is_360=True)
            if video_url:
                PropertyImage.objects.create(content_type=ct, object_id=base.pk, video_url=video_url)
            if video_file:
                PropertyImage.objects.create(content_type=ct, object_id=base.pk, video_file=video_file)

            # -------------------------------
            # 4️⃣ Clear Session and Redirect
            # -------------------------------
            if "property_wizard" in request.session:
                del request.session["property_wizard"]

            return redirect("/dashboard/property/add/?step=done")
        
        step = request.GET.get("step", "category")  # default = step 1
        return render(request, "dashboard/add_property_wizard.html", {
            "step": "images",
            "category": wizard_data.get("category"),
            "step" : step  
        })

    # -------------------------------------------------------
    # ✅ STEP 6 — DONE PAGE
    # -------------------------------------------------------
    if step == "done":
        return render(request, "dashboard/add_property_wizard.html", {"step": "done"})

    return HttpResponse("Invalid step", status=400)







# Property List Show -----------------------------------



from django.shortcuts import render
from .models import *  
from .models import ResidentialProperty, CommercialProperty, Duplex, Villa, Apartment

def property_list(request): 
   
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    commercial = CommercialProperty.objects.all()
    residential = ResidentialProperty.objects.all()
    # Dono models me field add kar do (temporary attribute)
    
    if q:
     commercial = commercial.filter(
        Q(title__icontains=q) | Q(subtype__icontains=q)
    )
     residential = residential.filter(
        Q(title__icontains=q) | Q(subtype__icontains=q)
    )   


    if category:
        commercial = commercial.filter(category__iexact=category)
        residential = residential.filter(category__iexact=category)
    
    properties = list(commercial) + list(residential)
    properties.sort(key=lambda p: p.id, reverse=True)

    # ✅ Add related subtype object dynamically
    for prop in properties:
        subtype_name = getattr(prop, 'subtype', None)  
        if subtype_name:  
            try:
               if subtype_name.lower() == "apartment":
                 prop.subtype_data = Apartment.objects.filter(property=prop).first()
               elif subtype_name.lower() == "villa":
                 prop.subtype_data = Villa.objects.filter(property=prop).first()
               elif subtype_name.lower() == "townhouse":
                 prop.subtype_data = Townhouse.objects.filter(property=prop).first()
               elif subtype_name.lower() == "studio":
                 prop.subtype_data = Studio.objects.filter(property=prop).first()
               elif subtype_name.lower() == "penthouse":
                 prop.subtype_data = Penthouse.objects.filter(property=prop).first()
               elif subtype_name.lower() == "duplex":
                 prop.subtype_data = Duplex.objects.filter(property=prop).first()
               elif subtype_name.lower() == "compound":
                 prop.subtype_data = Compound.objects.filter(property=prop).first()
               elif subtype_name.lower() == "residentialplot":
                 prop.subtype_data = ResidentialPlot.objects.filter(property=prop).first()

    # 🔹 Commercial Subtypes
               elif subtype_name.lower() == "office":
                 prop.subtype_data = Office.objects.filter(property=prop).first()
               elif subtype_name.lower() == "shop":
                 prop.subtype_data = Shop.objects.filter(property=prop).first()
               elif subtype_name.lower() == "showroom":
                 prop.subtype_data = Showroom.objects.filter(property=prop).first()
               elif subtype_name.lower() == "warehouse":
                 prop.subtype_data = Warehouse.objects.filter(property=prop).first()
               elif subtype_name.lower() == "factory":
                 prop.subtype_data = Factory.objects.filter(property=prop).first()
               elif subtype_name.lower() == "commercialland":
                 prop.subtype_data = CommercialLand.objects.filter(property=prop).first()
               else:
                 prop.subtype_data = None
            except Exception:
                prop.subtype_data = None 
        else:
            prop.subtype_data = None

    return render(request, "dashboard/property_list.html", {
        "properties": properties,
        
        "search": q,
        "category": category,
    })

# For User Property List pr user ke hisab se 
def client_detail(request, pk):  
    client = pk
    return render(request, 'dashboard/client_Property_List.html', {'client': client})  



# def property_detail(request, category, property_id):  
#     if category.lower() == "commercial":
#         prop = get_object_or_404(CommercialProperty, id=property_id)
#     elif category.lower() == "residential":
#         prop = get_object_or_404(ResidentialProperty, id=property_id)
#     else:
#         return render(request, "404.html", {"message": "Invalid property category"})

#     content_type = ContentType.objects.get_for_model(prop)
#     images = PropertyImage.objects.filter(content_type=content_type, object_id=prop.id)

#     return render(request, "dashboard/property_detail.html", {
#         "property": prop,
#         "images": images,   
#     })
 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages    
from .models import CommercialProperty, ResidentialProperty   
def property_detail(request, ptype, pid):       
    if ptype == "commercial":
        model = CommercialProperty
    elif ptype == "residential":
        model = ResidentialProperty
    else:
        messages.error(request, "Invalid property type!")
        return redirect("property_list")

    prop = get_object_or_404(model, id=pid)

    # Fetch all images related to this property
    images = PropertyImage.objects.filter(
        content_type=ContentType.objects.get_for_model(model),
        object_id=prop.id
    )

    return render(request, "dashboard/property_detail.html", {
        "property": prop,
        "images": images,
        "ptype": ptype
    })
    

  



def property_delete(request, ptype, pid):  
    if ptype == "commercial":
        model = CommercialProperty
    elif ptype == "residential":
        model = ResidentialProperty
    elif ptype == "agriculture":   
        model = AgricultureProperty 
    elif ptype == "holiday":  
        model = HolidayProperty
    elif ptype == "pg":
        model = BusinessForSale
    elif ptype == "pg":
        model = PGProperty  
    else:
        messages.error(request, "Invalid property type!")
        return redirect("property_list")

    obj = get_object_or_404(model, id=pid)    
    obj.delete()

    messages.success(request, f"{ptype.capitalize()} property deleted successfully.")
    return redirect("property_list")
  


# agriculture ke liye section he ----------------------------------------------------------------------------------

#  @csrf_exempt
def agriculture_create(request):
    if request.method == "POST":

        # Convert POST to dict
        data = request.POST
        company_id = data.get("company")
        company_obj = RealEstateCompany.objects.get(id=company_id) if company_id else None

        # Create property
        property_obj = AgricultureProperty.objects.create(
            
            company=company_obj,
            title=data.get("title"),
            user_id=data.get("user_id"),
            total_area=data.get("total_area"),
            area_unit=data.get("area_unit"),
            water_source=data.get("water_source"),
            ownership_type=data.get("ownership_type"),
            soil_type=data.get("soil_type"),
            current_use=data.get("current_use"),
            fenced_property=data.get("fenced_property") == "on",
            road_access=data.get("road_access") == "on",
            electricity_available=data.get("electricity_available") == "on",
            irrigation_system=data.get("irrigation_system") == "on",
            currency=data.get("currency"),
            expected_price=data.get("expected_price"),
            description=data.get("description"),
            
            property_type_id=int(data.get("property_type")),  
 
            # Location
            country=data.get("country"),
            state=data.get("state"),
            city=data.get("city"),
            locality=data.get("locality"),
            address=data.get("address"),  
            landmark=data.get("landmark"),
            pincode=data.get("pincode"),    
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),  
        )

        # AMENITIES (Many-to-Many)
        amenity_ids = request.POST.getlist("amenities")
        property_obj.amenities.set(amenity_ids)

        # MEDIA (Images, 360 Image, Video)
        images = request.FILES.getlist("images")
        images_360 = request.FILES.getlist("images_360")
        videos = request.FILES.getlist("video_file")

        # Normal images
        for img in images:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                image=img
            )

        # 360° Images
        for img in images_360:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                image_360=img
            )

        # Video files
        for vid in videos:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                video_file=vid
            )

        # Video URL
        video_url = data.get("video_url")
        if video_url:
            AgriculturePropertyImage.objects.create(
                property=property_obj,
                video_url=video_url
            )

        return JsonResponse({"message": "Property Created", "id": property_obj.id})  
    property_types = PropertyType.objects.all()
    amenities = Amenity.objects.all()
    company =  RealEstateCompany.objects.all()
    return render(request, "dashboard/AgriculturePcreate.html", {"amenities": amenities, "property_types":property_types, "company" : company})  


@csrf_exempt
def agriculture_update(request, pk):
    property_obj = get_object_or_404(AgricultureProperty, pk=pk)

    if request.method == "POST":
        data = request.POST

        property_obj.total_area = data.get("total_area")
        property_obj.area_unit = data.get("area_unit")
        property_obj.water_source = data.get("water_source")
        property_obj.ownership_type = data.get("ownership_type")
        property_obj.soil_type = data.get("soil_type")
        property_obj.current_use = data.get("current_use")
        property_obj.fenced_property = data.get("fenced_property") == "on"
        property_obj.road_access = data.get("road_access") == "on"
        property_obj.electricity_available = data.get("electricity_available") == "on"
        property_obj.irrigation_system = data.get("irrigation_system") == "on"
        property_obj.expected_price = data.get("expected_price")
        property_obj.description = data.get("description")     
        property_obj.property_type = data.get("property_type")       
        # Location
        property_obj.country = data.get("country")
        property_obj.state = data.get("state")
        property_obj.city = data.get("city")
        property_obj.locality = data.get("locality")
        property_obj.address = data.get("address")
        property_obj.landmark = data.get("landmark")
        property_obj.pincode = data.get("pincode")
        property_obj.latitude = data.get("latitude")
        property_obj.longitude = data.get("longitude")

        property_obj.save()

        # Update amenities
        property_obj.amenities.set(request.POST.getlist("amenities"))

        # Add new Media
        images = request.FILES.getlist("images")
        for img in images:
            AgriculturePropertyImage.objects.create(property=property_obj, image=img)

        return JsonResponse({"message": "Property Updated"})  
    property_types = PropertyType.objects.all()
    return render(request, "dashboard/agriculture/edit.html", {"property": property_obj, "property_types": property_types})

def agriculture_list(request):  
    properties = AgricultureProperty.objects.all().order_by("-created_at")
    print(properties)   
    return render(request, "dashboard/agriculture_list.html", {"properties": properties})  

def agriculture_detail(request, pk):
    property_obj = get_object_or_404(AgricultureProperty, pk=pk)
    return render(request, "agriculture/detail.html", {
        "property": property_obj,
        "media": property_obj.media.all()
    })
    
@csrf_exempt
def agriculture_delete(request, pk):
    property_obj = get_object_or_404(AgricultureProperty, pk=pk)
    property_obj.delete()   # <-- इसे चलाते ही media भी delete हो जाता है (CASCADE)
    return JsonResponse({"message": "Property & its Media Deleted"})





# PG ke  liye --------------------------------------------------------------------------------------------


def add_pg_property(request):      
    amenities = Amenity.objects.all()
    
    if request.method == "POST":
        try:
            # ---------------------------
            # BASIC PG PROPERTY FIELDS
            # ---------------------------
            
            room_type = request.POST.get("room_type")
            furnishing = request.POST.get("furnishing")
            preferred_gender = request.POST.get("preferred_gender")

            minimum_stay = request.POST.get("minimum_stay")
            total_beds = request.POST.get("total_beds")

            expected_price = request.POST.get("expected_price")

            # Utilities
            electricity = bool(request.POST.get("electricity"))
            water = bool(request.POST.get("water"))
            wifi = bool(request.POST.get("wifi"))
            cleaning = bool(request.POST.get("cleaning"))
            
            raw_value = request.POST.get("property_type")
            print("RAW VALUE:", raw_value)

            # If tuple or list comes → fix it
            if isinstance(raw_value, (list, tuple)):  
              raw_value = raw_value[0]

            property_type_id = int(raw_value)
            property_type_obj = PropertyType.objects.get(id=property_type_id)  
            description = request.POST.get("description")
            raw_title=request.POST.get("title"),
            # If tuple or list → pick first value
            if isinstance(raw_title, (list, tuple)):
              raw_title = raw_title[0]

            title = str(raw_title).strip()  
            company_id = request.POST.get("company")
            company_obj = RealEstateCompany.objects.get(id=company_id) if company_id else None
            # ---------------------------
            # LOCATION DETAILS
            # ---------------------------
            country = request.POST.get("country")
            state = request.POST.get("state")
            city = request.POST.get("city")
            locality = request.POST.get("locality")
            address = request.POST.get("address")  
            landmark = request.POST.get("landmark")
            pincode = request.POST.get("pincode")

            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")

            # ---------------------------
            # CREATE PROPERTY OBJECT
            # ---------------------------
            pg = PGProperty.objects.create(
                title=title,
                company = company_obj,
                property_type=property_type_obj,    
                room_type=room_type,
                furnishing=furnishing,
                preferred_gender=preferred_gender,
                
                minimum_stay=minimum_stay,
                total_beds=total_beds,

                expected_price=expected_price,

                electricity=electricity,
                water=water,
                wifi=wifi,
                cleaning=cleaning,

                description=description,

                country=country,
                state=state,
                city=city,
                locality=locality,
                address=address,
                landmark=landmark,
                pincode=pincode,

                latitude=latitude or None,
                longitude=longitude or None,
            )

            # ---------------------------
            # AMENITIES - MANY TO MANY
            # ---------------------------
            selected_amenities = request.POST.getlist("amenities")
            if selected_amenities:
                pg.amenities.add(*selected_amenities)

            # ---------------------------
            # MEDIA UPLOADS
            # ---------------------------

            # Normal Images
            images = request.FILES.getlist("images")  
            for img in images:
                PGPropertyImage.objects.create(
                    property=pg,
                    image=img
                )

            # 360 Images
            images_360 = request.FILES.getlist("images_360")
            for img360 in images_360:
                PGPropertyImage.objects.create(
                    property=pg,
                    image_360=img360
                )

            # Video File
            video_file = request.FILES.get("video_file")
            if video_file:
                PGPropertyImage.objects.create(
                    property=pg,
                    video_file=video_file
                )

            # Video URL
            video_url = request.POST.get("video_url")  
            if video_url:
                PGPropertyImage.objects.create(
                    property=pg,
                    video_url=video_url
                )

            messages.success(request, "PG Property added successfully!")
            return redirect("pg_property_list")  # <- apni listing page ka URL name

        except Exception as e:
            print("Error:", e)
            messages.error(request, f"Something went wrong: {e}")
    property_types = PropertyType.objects.all() 
    company =  RealEstateCompany.objects.all()
      
    return render(request, "dashboard/PG_create.html", {    
        "amenities": amenities,
        "property_types" : property_types,
        "company": company
          
    })    
    
def pg_list(request):  
    properties = PGProperty.objects.all().order_by("-created_at")
    return render(request, "dashboard/pg_p_list.html", {"properties": properties})   
    
    
# For Business F Sale ke liye he  ----------------------------------------------------------------------------------------------------------



def business_create(request):
    if request.method == "POST":

        data = request.POST
        company_id=data.get("company"),   
        company_obj = RealEstateCompany.objects.get(id=company_id) if company_id else None
        # ------------------------------
        # 1️⃣ Create Business Property
        # ------------------------------
        business = BusinessForSale.objects.create(  
            user_id=data.get("user_id"),

            # Basic Info
            # 🔹 Company Save Here
            company=company_obj,
            
            title=data.get("title"),
            business_type=data.get("business_type"),
            established_year=data.get("established_year"),
            property_type_id=int(data.get("property_type")),      
            # Pricing
            asking_price=data.get("asking_price"),
            price_negotiable=data.get("price_negotiable") == "on",

            # Revenue Info
            monthly_revenue=data.get("monthly_revenue"),
            profit_margin=data.get("profit_margin"),
            number_of_employees=data.get("number_of_employees"),

            # Property Details
            total_area=data.get("total_area"),
            ownership_type=data.get("ownership_type"),

            description=data.get("description"),
            facilities_included=data.get("facilities_included"),
            reason_for_sale=data.get("reason_for_sale"),

            # Contact Info
            contact_person=data.get("contact_person"),
            contact_phone=data.get("contact_phone"),
            contact_email=data.get("contact_email"),

            # LOCATION
            country=data.get("country"),
            state=data.get("state"),
            city=data.get("city"),
            locality=data.get("locality"),
            address=data.get("address"),
            landmark=data.get("landmark"),
            pincode=data.get("pincode"),  
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )

        # ------------------------------
        # 2️⃣ Many-to-Many (Amenities)
        # ------------------------------
        amenity_ids = request.POST.getlist("amenities")
        business.amenities.set(amenity_ids)

        # ------------------------------
        # 3️⃣ MEDIA (Images + 360 + Video)
        # ------------------------------
        images = request.FILES.getlist("images")
        images_360 = request.FILES.getlist("images_360")
        videos = request.FILES.getlist("video_file")

        # Normal Images
        for img in images:
            BusinessForSaleImage.objects.create(
                property=business,
                image=img
            )

        # 360° Images
        for img in images_360:
            BusinessForSaleImage.objects.create(
                property=business,
                image_360=img
            )

        # Video Files
        for vid in videos:
            BusinessForSaleImage.objects.create(
                property=business,
                video_file=vid
            )

        # Video URL
        video_url = data.get("video_url")
        if video_url:
            BusinessForSaleImage.objects.create(
                property=business,
                video_url=video_url
            )

        return JsonResponse({"message": "Business Created", "id": business.id})

    # GET Request
    property_types = PropertyType.objects.all()
    amenities = Amenity.objects.all()  
    company =  RealEstateCompany.objects.all()
    return render(request, "dashboard/Business_Sale_create.html", {"amenities": amenities, "property_types": property_types, "company": company})

    
def bfors_list(request):  
    properties = BusinessForSale.objects.all().order_by("-created_at")
    print(properties)  
    return render(request, "dashboard/business_list.html", {"properties": properties}) 



# ----------------------------------------------------------------------------------------------------------------------



def holiday_View_create(request):       
    if request.method == "POST":

        data = request.POST
        company_id=data.get("company")    
        company_obj = RealEstateCompany.objects.get(id=company_id) if company_id else None
        # ------------------------------------------------
        # 1️⃣ Create Holiday Property
        # ------------------------------------------------
        holiday = HolidayProperty.objects.create(  
            country=company_obj,  
            # Basic  
            title=data.get("title"),
            Subproperty_type=data.get("subproperty_type"),    
            listing_type=data.get("listing_type"),
            price=data.get("price"),
            price_type=data.get("price_type"),
            available_from=data.get("available_from") or None,
            available_to=data.get("available_to") or None,
            description=data.get("description"),
            property_type_id=int(request.POST.get("property_type")),   
            # Location
            
            
            state=data.get("state"),
            city=data.get("city"),
            locality=data.get("locality"),
            address=data.get("address"),
            landmark=data.get("landmark"),
            pincode=data.get("pincode"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),

            # Property Specs
            bedrooms=data.get("bedrooms"),
            bathrooms=data.get("bathrooms"),
            balconies=data.get("balconies"),
            builtup_area=data.get("builtup_area"),
            carpet_area=data.get("carpet_area"),
            plot_area=data.get("plot_area"),
            furnishing=data.get("furnishing"),
            floor_number=data.get("floor_number"),
            total_floors=data.get("total_floors"),
            parking_spaces=data.get("parking_spaces"),
            facing_direction=data.get("facing_direction"),
            property_age=data.get("property_age"),

            # Nearby
            beach_distance=data.get("beach_distance"),
            market_distance=data.get("market_distance"),
            restaurant_distance=data.get("restaurant_distance"),
            airport_distance=data.get("airport_distance"),

            # Owner / Agent
            listed_by=data.get("listed_by"),
            owner_name=data.get("owner_name"),
            contact_number=data.get("contact_number"),
            email=data.get("email"),
            profile_photo=request.FILES.get("profile_photo"),

            # SEO
            meta_title=data.get("meta_title"),
            meta_description=data.get("meta_description"),
            tags=data.get("tags"),
            featured=data.get("featured") == "on",
             # 🔹 Company Save Here
            company_id=data.get("company"),    
        )

        # ------------------------------------------------
        # 2️⃣ Amenities (Many-to-Many)
        # ------------------------------------------------
        amenity_ids = request.POST.getlist("amenities")
        holiday.amenities.set(amenity_ids)

        # ------------------------------------------------
        # 3️⃣ Media Upload (Images + 360 + Video)
        # ------------------------------------------------
        images = request.FILES.getlist("images")
        images_360 = request.FILES.getlist("images_360")
        videos = request.FILES.getlist("video_file")

        # Normal Images
        for img in images:
            HolidayPropertyImage.objects.create(
                property=holiday,
                image=img,
            )

        # 360° Images
        for img in images_360:
            HolidayPropertyImage.objects.create(
                property=holiday,
                image_360=img,
            )

        # Video Files
        for vid in videos:
            HolidayPropertyImage.objects.create(
                property=holiday,
                video_file=vid,
            )

        # Video URL
        video_url = data.get("video_url")
        if video_url:
            HolidayPropertyImage.objects.create(
                property=holiday,
                video_url=video_url,
            )

        return JsonResponse({"message": "Holiday Property Created", "id": holiday.id})

    # ------------------------------------------------
    # GET REQUEST (Render Form)
    # ------------------------------------------------
    
    property_types = PropertyType.objects.all()
    amenities = Amenity.objects.all()
    company = RealEstateCompany.objects.all()
    return render(request, "dashboard/holiday_create.html", {     
        "amenities": amenities,
        "property_types" : property_types,
        "company": company 
           
    })


def holiday_list(request):     
    properties = HolidayProperty.objects.all().order_by("-created_at")    
    return render(request, "dashboard/holiday_p_list.html", {"properties": properties}) 