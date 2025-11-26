from rest_framework import serializers
from .models import *  
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import (
#     CustomUser,  
    
#     Country,
#     Slider,
#     RealEstateCompany,
#     Agent,
#     Blogs,
#     Testimonial,
#     regesteruser,
#     PropertyType,
#     Amenity,
#     UserPaymentPlan

    

  
# )

# from .utils import generate_otp,verify_otp

# class EmailCheckSerializer(serializers.Serializer):
#     email = serializers.EmailField()



# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = regesteruser
#         fields = ['user_type', 'phone', 'country']

#     def create(self, validated_data):
#         otp = generate_otp(validated_data['phone'])
#         # send OTP via SMS here (e.g., Twilio)
#         print("Generated OTP:", otp)  # debug
#         return validated_data


# class OTPVerifySerializer(serializers.Serializer):
#     phone = serializers.CharField()
#     otp = serializers.CharField()
#     user_type = serializers.CharField()
#     country = serializers.CharField()

#     def validate(self, data):
#         if not verify_otp(data['phone'], data['otp']):
#             raise serializers.ValidationError("Invalid or expired OTP")
#         return data

#     def create(self, validated_data):
#         user = regesteruser.objects.create(
#             user_type=validated_data['user_type'],
#             phone=validated_data['phone'],
#             country=validated_data['country'],
#             property_limit="3",
            
#             is_verified=True
#         )
#         return user


# class LoginSerializer(serializers.Serializer):
#     phone = serializers.CharField()

#     def validate(self, data):
#         phone = data.get('phone')
#         if not regesteruser.objects.filter(phone=phone, is_verified=True).exists():
#             raise serializers.ValidationError("User not found or not verified")
#         return data

#     def create(self, validated_data):
#         otp = generate_otp(validated_data['phone'])
#         print("Login OTP:", otp)
#         return validated_data


# class LoginOTPVerifySerializer(serializers.Serializer):
#     phone = serializers.CharField()
#     otp = serializers.CharField()

#     def validate(self, data):
#         phone = data.get('phone')
#         otp = data.get('otp')

#         if not regesteruser.objects.filter(phone=phone, is_verified=True).exists():
#             raise serializers.ValidationError("User not found or not verified")

#         if not verify_otp(phone, otp):
#             raise serializers.ValidationError("Invalid or expired OTP")

#         return data

#     def create(self, validated_data):
#         user = regesteruser.objects.get(phone=validated_data['phone'])
#         return user  # return user object directly for session/auth
        

# from .utils import get_logged_in_user

# # class PropertySerializer(serializers.ModelSerializer):
# #     amenities = serializers.PrimaryKeyRelatedField(
# #         queryset=Amenity.objects.all(), many=True, required=False
# #     )

# #     class Meta:
# #         model = UserProperty
# #         fields = "__all__"
# #         read_only_fields = ['user', 'created_at', 'updated_at']

# #     def create(self, validated_data):
# #         request = self.context.get('request')
# #         user_id = request.data.get('user_id')

    

# #         if not user_id:
# #          raise serializers.ValidationError({"user_id": "This field is required."})

# #         try:
# #             user = regesteruser.objects.get(id=user_id)
# #         except regesteruser.DoesNotExist:
# #             raise serializers.ValidationError({"user_id": "Invalid user id."})
# #         # Extract amenitie
# #         amenities = validated_data.pop('amenities', [])

# #         # Create the property with correct user instance
# #         property_instance = UserProperty.objects.create(user=user, **validated_data)

# #         # Assign amenities
# #         if amenities:
# #             property_instance.amenities.set(amenities)

# #         # Handle files
# #         for field in ['video', 'brochure', 'image2', 'image3']:
# #             if request.FILES.get(field):
# #                 setattr(property_instance, field, request.FILES[field])
# #         property_instance.save()
# #         return property_instance

# #     def update(self, instance, validated_data):
# #         amenities = validated_data.pop('amenities', None)
# #         for key, value in validated_data.items():
# #             setattr(instance, key, value)
# #         instance.save()
# #         if amenities is not None:
# #             instance.amenities.set(amenities)
# #         return instance  


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = regesteruser
#         fields = [
#             "name", "email", "phone", "address", "country", "state", "city", "pincode",
#             "image", "company_register_no", "cp_name", "cp_email", "cp_phone", "cp_designation"
#         ]
#         read_only_fields = ["phone"]

#     def update(self, instance, validated_data):
#         request = self.context.get('request')
#         if request.FILES.get('image'):
#             instance.image = request.FILES['image']

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

# # class PropertyDetailSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = UserProperty
# #         fields = "__all__"
# class PropertyTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PropertyType
#         fields = "__all__"

# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = "__all__"

# class SliderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slider
#         fields = "__all__"
# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RealEstateCompany
#         fields = "__all__"



# Agent ke liye He ==== .  

ALLOWED_CV_EXTENSIONS = [".pdf", ".doc", ".docx"]

def validate_cv_file(file):
    import os
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_CV_EXTENSIONS:
        raise serializers.ValidationError("CV must be a PDF, DOC or DOCX file.")
    return file

# class AgentSerializer(serializers.ModelSerializer):
#     created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
#     updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)  
#     cv = serializers.FileField(required=False, allow_null=True, validators=[validate_cv_file])  
#     class Meta:
#         model = Agent
#         fields = "__all__" 
             
class AgentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    cv = serializers.FileField(required=False, allow_null=True, validators=[validate_cv_file])  
    class Meta:
        model = Agent
        exclude = []  # jitna chaho rakh lo

    def get_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d")
        return None

    def get_updated_at(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime("%Y-%m-%d")
        return None

        
        
        
        

        
class RegisterUserSerializer(serializers.ModelSerializer):
   
      
    class Meta:
        model = regesteruser   
        fields = "__all__"   

class PropertyTypeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = PropertyType  
        fields = "__all__" 
        
class AmenitiesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Amenity
        fields = "__all__" 
# class AmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Amenity
#         fields = "__all__"



# class BlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blogs
#         fields = "__all__"
# class TestimonialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Testimonial
#         fields = "__all__"
        
        
# Updated Serilizer -------------------------------------------------------------------------------



from rest_framework import serializers
from .models import *
# Image ke  liye 

class RealEstateCompanySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = RealEstateCompany
        fields = "__all__"  

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = [
            "id", "image", "video_url", "video_file",
            "is_360", "is_featured", "sort_order", "uploaded_at"
        ]
  
class CommercialPropertySerializer(serializers.ModelSerializer):
    # READ-ONLY NESTED FIELDS
    property_type = PropertyTypeSerializer(read_only=True)
    company = RealEstateCompanySerializer(read_only=True)
    # agent = AgentSerializer(source="user", read_only=True)    
    amenities = AmenitiesSerializer(many=True, read_only=True)

    featured_image = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

    subtype_data = serializers.SerializerMethodField()

    class Meta:
        model = CommercialProperty
        fields = "__all__"   # ✔ everything auto included

    # Featured image
    def get_featured_image(self, obj):
        return obj.featured_image.url if obj.featured_image else None

    # Subtype (Office / Shop / Showroom ...)
    def get_subtype_data(self, obj):
        if not obj.subtype:
            return None

        mapping = {
            "office": (Office, OfficeSerializer),
            "shop": (Shop, ShopSerializer),
            "showroom": (Showroom, ShowroomSerializer),
            "warehouse": (Warehouse, WarehouseSerializer),
            "factory": (Factory, FactorySerializer),
            "commercialland": (CommercialLand, CommercialLandSerializer),
        }

        subtype = obj.subtype.lower()

        if subtype not in mapping:
            return None

        model, serializer = mapping[subtype]
        instance = model.objects.filter(property=obj).first()

        return serializer(instance).data if instance else None



class ResidentialPropertySerializer(serializers.ModelSerializer):   

    # Read-only nested fields
    property_type = PropertyTypeSerializer(read_only=True)
    company = RealEstateCompanySerializer(read_only=True)
    amenities = AmenitiesSerializer(many=True, read_only=True)

    # Media fields
    featured_image = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

    # Subtype
    subtype_data = serializers.SerializerMethodField()

    class Meta:
        model = ResidentialProperty
        fields = "__all__"

    def get_featured_image(self, obj):
        return obj.featured_image.url if obj.featured_image else None

    def get_images(self, obj):
        return PropertyImageSerializer(obj.images.all(), many=True).data

    def get_subtype_data(self, obj):
        if not obj.subtype:
            return None

        mapping = {
            "apartment": (Apartment, ApartmentSerializer),
            "villa": (Villa, VillaSerializer),
            "townhouse": (TownhouseSerializer, TownhouseSerializer),
            "studio": (Studio, StudioSerializer),
            "penthouse": (Penthouse, PenthouseSerializer),
            "duplex": (Duplex, DuplexSerializer),
            "compound": (Compound, CompoundSerializer),
            "residentialplot": (ResidentialPlot, ResidentialPlotSerializer),
        }

        subtype = obj.subtype.lower()
        if subtype not in mapping:
            return None

        model, serializer = mapping[subtype]
        instance = model.objects.filter(property=obj).first()
        return serializer(instance).data if instance else None


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = regesteruser
        fields = ["id", "name", "email", "phone"]


class AgentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "name", "phone", "email"]  

# Subtypes Models. 


# R ...
class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = "__all__"

class VillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Villa
        fields = "__all__"

class TownhouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Townhouse
        fields = "__all__"

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = "__all__"

class PenthouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penthouse
        fields = "__all__"

class DuplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duplex
        fields = "__all__"

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"

class ResidentialPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialPlot
        fields = "__all__"
  


# C.... 


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

class ShowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showroom
        fields = "__all__"

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"

class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = "__all__"

class CommercialLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommercialLand
        fields = "__all__"



# --------------------------------------------------------------------------
class PropertySerializer(serializers.Serializer):    
    id = serializers.IntegerField()
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    locality = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    property_type = serializers.CharField(required=False)  

    # --------------------------
    # LOCATION COMBINED FIELD
    # --------------------------
    def get_location(self, obj):
        parts = [
            getattr(obj, "sub_locality", None),
            getattr(obj, "locality", None),
            getattr(obj, "city", None),
            getattr(obj, "country", None),
        ]
        return ", ".join([p for p in parts if p])

    # --------------------------
    # FEATURED IMAGE SAFE CHECK
    # --------------------------
    def get_featured_image(self, obj):
        if hasattr(obj, "featured_image") and obj.featured_image:
            return obj.featured_image.url
        return None

    # --------------------------
    # SUBTYPE DETAILS
    # --------------------------
    def get_subtype_data(self, obj):  

        if not obj.subtype:
            return None

        mapping = {
            "apartment": (Apartment, ApartmentSerializer),
            "villa": (Villa, VillaSerializer),
            "townhouse": (Townhouse, TownhouseSerializer),
            "studio": (Studio, StudioSerializer),
            "penthouse": (Penthouse, PenthouseSerializer),
            "duplex": (Duplex, DuplexSerializer),
            "compound": (Compound, CompoundSerializer),
            "residentialplot": (ResidentialPlot, ResidentialPlotSerializer),

            # Commercial
            "office": (Office, OfficeSerializer),
            "shop": (Shop, ShopSerializer),
            "showroom": (Showroom, ShowroomSerializer),
            "warehouse": (Warehouse, WarehouseSerializer),
            "factory": (Factory, FactorySerializer),
            "commercialland": (CommercialLand, CommercialLandSerializer),
        }

        subtype = obj.subtype.lower()

        if subtype not in mapping:
            return None

        model, serializer = mapping[subtype]

        instance = model.objects.filter(property=obj).first()
        return serializer(instance).data if instance else None


# ------------------------------------------------------------------------------------------


# Auther Properties ...................................add()

class HolidayImageSerializer(serializers.ModelSerializer):  
    class Meta:
        model = HolidayPropertyImage
        fields = "__all__"
        read_only_fields = ("uploaded_at",)
        

class HolidayPropertySerializer(serializers.ModelSerializer):
    media = HolidayImageSerializer(many=True, read_only=True)

    # POST me sirf ID jayegi
    property_type = PropertyTypeSerializer(read_only=True)  
    amenities = AmenitiesSerializer(many=True, read_only=True)  
    company = serializers.PrimaryKeyRelatedField(
        queryset=RealEstateCompany.objects.all(),
        required=False,
        allow_null=True
    )

    # GET me full details
    company_details = RealEstateCompanySerializer(source="company", read_only=True)

    class Meta:
        model = HolidayProperty
        fields = "__all__"

    def create(self, validated_data):
        amenities = validated_data.pop("amenities", [])
        obj = HolidayProperty.objects.create(**validated_data)
        obj.amenities.set(amenities)
        return obj

    def update(self, instance, validated_data):
        amenities = validated_data.pop("amenities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)

        return instance


#  ----------------------------------------------------------


class AgricultureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgriculturePropertyImage
        fields = "__all__"
        read_only_fields = ("uploaded_at",)


class AgriculturePropertySerializer(serializers.ModelSerializer):
    media = AgricultureImageSerializer(many=True, read_only=True)

    property_type = PropertyTypeSerializer(read_only=True)  
    amenities = AmenitiesSerializer(many=True, read_only=True)  
    company = serializers.PrimaryKeyRelatedField(
        queryset=RealEstateCompany.objects.all(),
        required=False,
        allow_null=True
    )
    company_details = RealEstateCompanySerializer(source="company", read_only=True)

    class Meta:
        model = AgricultureProperty
        fields = "__all__"

    def create(self, validated_data):
        amenities = validated_data.pop("amenities", [])
        obj = AgricultureProperty.objects.create(**validated_data)
        obj.amenities.set(amenities)
        return obj

    def update(self, instance, validated_data):
        amenities = validated_data.pop("amenities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)
   
        return instance

from decimal import Decimal, InvalidOperation  
class AgriculturePropertyCreateSerializer(serializers.ModelSerializer):
    # amenities = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Amenity.objects.all(),
    #     required=False
    # )

    amenities = AmenitiesSerializer(many=True, read_only=True)   

    class Meta:
        model = AgricultureProperty
        fields = "__all__"

    def validate(self, data):
        for field in ["total_area", "expected_price", "latitude", "longitude"]:
            value = data.get(field)
            if value in ("", None):
                data[field] = None
            else:
                try:
                    data[field] = Decimal(str(value))
                except (InvalidOperation, ValueError):
                    raise serializers.ValidationError({field: "Invalid decimal value"})
        return data

    def create(self, validated_data):
        validated_data['status'] = 'Pending'  
        amenities = validated_data.pop("amenities", [])
        obj = AgricultureProperty.objects.create(**validated_data)
        obj.amenities.set(amenities)
        return obj

    # -----------------------------------------------------
    
    
class PGImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGPropertyImage
        fields = "__all__"
        read_only_fields = ("uploaded_at",)


class PGPropertySerializer(serializers.ModelSerializer):
    media = PGImageSerializer(many=True, read_only=True)

    property_type = PropertyTypeSerializer(read_only=True)  
    amenities = AmenitiesSerializer(many=True, read_only=True)  
    company = serializers.PrimaryKeyRelatedField(
        queryset=RealEstateCompany.objects.all(),
        required=False,
        allow_null=True
    )
    company_details = RealEstateCompanySerializer(source="company", read_only=True)

    class Meta:
        model = PGProperty
        fields = "__all__"

    def create(self, validated_data):
        amenities = validated_data.pop("amenities", [])
        obj = PGProperty.objects.create(**validated_data)
        obj.amenities.set(amenities)
        return obj

    def update(self, instance, validated_data):
        amenities = validated_data.pop("amenities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)

        return instance  


# --------------------------------------------------------


class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessForSaleImage
        fields = "__all__"
        read_only_fields = ("uploaded_at",)
        

class BusinessForSaleSerializer(serializers.ModelSerializer):
    media = BusinessImageSerializer(many=True, read_only=True)

    property_type = PropertyTypeSerializer(read_only=True)  
    amenities = AmenitiesSerializer(many=True, read_only=True)  
    company = serializers.PrimaryKeyRelatedField(
        queryset=RealEstateCompany.objects.all(),
        required=False,
        allow_null=True
    )
    company_details = RealEstateCompanySerializer(source="company", read_only=True)

    class Meta:
        model = BusinessForSale
        fields = "__all__"

    def create(self, validated_data):
        amenities = validated_data.pop("amenities", [])
        obj = BusinessForSale.objects.create(**validated_data)
        obj.amenities.set(amenities)
        return obj

    def update(self, instance, validated_data):
        amenities = validated_data.pop("amenities", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)

        return instance



# --------------------------------------------------------------------------------------------------

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from .models import regesteruser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  

    def validate(self, attrs):
        email = self.initial_data.get("email")
        password = self.initial_data.get("password")

        # Find user by email in CustomUser
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone
            }
        }
