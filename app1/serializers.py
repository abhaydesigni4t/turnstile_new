from rest_framework import serializers
from .models import UserEnrolled,Asset,Site,Notification,Upload_File,Turnstile_S,Orientation,PreShift,ToolBox



class ActionStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AssetSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=True, required=False)
    footage = serializers.ImageField(max_length=None, use_url=True, required=False)
    site = serializers.CharField()  # Field to accept site name

    class Meta:
        model = Asset
        fields = [ 'picture', 'asset_name', 'tag_id', 'footage', 'description', 'status', 'location', 'time_log', 'site']

    def validate_site(self, value):
        try:
            site_instance = Site.objects.get(name=value.upper())
            return site_instance
        except Site.DoesNotExist:
            raise serializers.ValidationError("Site with this name does not exist.")

    def create(self, validated_data):
        site = validated_data.pop('site')
        asset = Asset.objects.create(site=site, **validated_data)
        return asset
    
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError


class UserEnrolledSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrolled
        exclude = ['sr', 'password']
        extra_kwargs = {
            'email': {'validators': []},  # Remove default unique validator
        }

    def get_picture(self, obj):
        request = self.context.get('request')
        user_folder = os.path.join(settings.MEDIA_ROOT, 'facial_data', obj.get_folder_name())
        if default_storage.exists(user_folder):
            user_images = [f for f in default_storage.listdir(user_folder)[1] if f.endswith('.jpg') or f.endswith('.jpeg')]
            if user_images:
                image_path = os.path.join('facial_data', obj.get_folder_name(), user_images[0])
                image_url = request.build_absolute_uri(settings.MEDIA_URL + image_path)
                return image_url
        return None

    def get_site(self, obj):
        if obj.site:
            return obj.site.name  # Assuming the Site model has a 'name' field
        return None

    def validate_email(self, value):
        if UserEnrolled.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value
    
class UserEnrolledSerializer1(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['email','tag_id']
       
class UserEnrolledSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['mycompany_id','orientation']

from django.utils import timezone

class ExitSerializer(serializers.ModelSerializer):
    time_log = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Asset
        fields = ['asset_id', 'asset_name', 'tag_id', 'footage', 'location', 'time_log']
        read_only_fields = ['time_log']  # Ensuring time_log is read-only as it is automatically set
        
    def create(self, validated_data):
        # Convert empty string to null for location
        if validated_data.get('location') == '':
            validated_data['location'] = None
        return super().create(validated_data)

class SiteSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ['picture', 'name', 'location', 'total_users', 'active_users', 'inactive_users']

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.picture:
            return request.build_absolute_uri(obj.picture.url)
        return None

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['subject', 'description', 'username']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload_File
        fields = '__all__'

class TurnstileSerializer(serializers.ModelSerializer):
    safety_confirmation = serializers.SerializerMethodField()

    def get_safety_confirmation(self, obj):
        return 1 if obj.safety_confirmation else 0

    class Meta:
        model = Turnstile_S
        fields = ['turnstile_id', 'location', 'safety_confirmation']

class AssetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['asset_id', 'status','location']

class facialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ('email', 'facial_data')

class OrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        fields = '__all__'
    


from rest_framework import serializers
from .models import PreShift, Site

class PreShiftSerializer(serializers.ModelSerializer):
    site = serializers.CharField()

    class Meta:
        model = PreShift
        fields = ['document', 'date', 'site']

    def validate_site(self, value):
        try:
            return Site.objects.get(name__iexact=value)
        except Site.DoesNotExist:
            raise serializers.ValidationError("Site with this name does not exist.")

    def create(self, validated_data):
        site_name = validated_data.pop('site')
        site = Site.objects.get(name__iexact=site_name)
        return PreShift.objects.create(site=site, **validated_data)

from rest_framework import serializers
from .models import ToolBox, Site

class ToolBoxSerializer(serializers.ModelSerializer):
    site = serializers.CharField()

    class Meta:
        model = ToolBox
        fields = ['document', 'date', 'site']

    def validate_site(self, value):
        try:
            return Site.objects.get(name__iexact=value)
        except Site.DoesNotExist:
            raise serializers.ValidationError("Site with this name does not exist.")

    def create(self, validated_data):
        site_name = validated_data.pop('site')
        site = Site.objects.get(name__iexact=site_name)
        return ToolBox.objects.create(site=site, **validated_data)



from rest_framework import serializers

class FacialImageDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    facial_data = serializers.ListField(child=serializers.ImageField())


# serializers.py
from rest_framework import serializers
from .models import UserEnrolled, Site

class UserProfileSerializer(serializers.ModelSerializer):
    site = serializers.CharField(required=False, allow_blank=True)  # Change to CharField for site name

    class Meta:
        model = UserEnrolled
        fields = ['name', 'company_name', 'job_role', 'mycompany_id', 'job_location', 'email', 'site']
    
    def create(self, validated_data):
        validated_data['status'] = 'active'
        return UserEnrolled.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['status'] = validated_data.get('status', 'active')
        return super().update(instance, validated_data)


class UserComplySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['email', 'my_comply']


from rest_framework import serializers
from .models import OnSiteUser


# class OnSiteUserSerializer(serializers.ModelSerializer):
#     site = serializers.CharField(required=False)

#     class Meta:
#         model = OnSiteUser
#         fields = ['name', 'tag_id', 'status', 'site']

#     def to_internal_value(self, data):
#         # Convert site name to Site instance
#         internal_data = super().to_internal_value(data)
#         site_name = data.get('site')

#         if site_name:
#             try:
#                 site = Site.objects.get(name=site_name)
#                 internal_data['site'] = site
#             except Site.DoesNotExist:
#                 raise serializers.ValidationError({'site': 'Site with the provided name does not exist.'})
#         else:
#             internal_data['site'] = None
        
#         return internal_data

#     def to_representation(self, instance):
#         # Convert Site instance to site name for the response
#         representation = super().to_representation(instance)
#         representation['site'] = instance.site.name if instance.site else None
#         return representation

class OnSiteUserSerializer(serializers.ModelSerializer):
    site = serializers.CharField(required=False)
    face = serializers.BooleanField(required=True)  # Include the face field in the serializer

    class Meta:
        model = OnSiteUser
        fields = ['name', 'tag_id', 'status', 'site', 'face']  # Add face to the fields list

    def to_internal_value(self, data):
        # Convert site name to Site instance
        internal_data = super().to_internal_value(data)
        site_name = data.get('site')

        if site_name:
            try:
                site = Site.objects.get(name=site_name)
                internal_data['site'] = site
            except Site.DoesNotExist:
                raise serializers.ValidationError({'site': 'Site with the provided name does not exist.'})
        else:
            internal_data['site'] = None
        
        return internal_data

    def to_representation(self, instance):
        # Convert Site instance to site name for the response
        representation = super().to_representation(instance)
        representation['site'] = instance.site.name if instance.site else None
        representation['face'] = 1 if instance.face else 0  # Convert boolean to 0 or 1
        return representation


        
    
'''    
        
# this is correct post onsite user api post data using site only do this changes in serializer 

class OnSiteUserSerializer(serializers.ModelSerializer):
    site = serializers.CharField()

    class Meta:
        model = OnSiteUser
        fields = ['name', 'tag_id', 'status', 'site']

    def validate_site(self, value):
        try:
            return Site.objects.get(name__iexact=value)
        except Site.DoesNotExist:
            raise serializers.ValidationError("Site with this name does not exist.")

    def create(self, validated_data):
        site_name = validated_data.pop('site')
        site = Site.objects.get(name__iexact=site_name)
        return OnSiteUser.objects.create(site=site, **validated_data)
        '''

class OnsiteGetSerializer(serializers.ModelSerializer):
    site = serializers.SerializerMethodField()

    class Meta:
        model = OnSiteUser
        fields = ['name', 'tag_id', 'status', 'face', 'timestamp', 'site']

    def get_site(self, obj):
        # Return the site name instead of the primary key
        return obj.site.name if obj.site else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the boolean face field to 1 or 0
        representation['face'] = 1 if instance.face else 0
        return representation



class PostSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['picture', 'name', 'location']
        
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
import os
from django.conf import settings

class GetUserEnrolledSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    orientation = serializers.SerializerMethodField()
    facial_data = serializers.SerializerMethodField()
    my_comply = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrolled
        fields = ['picture', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location', 'orientation', 'facial_data', 'my_comply', 'status', 'email']

    def get_picture(self, obj):
        request = self.context.get('request')
        user_folder = os.path.join(settings.MEDIA_ROOT, 'facial_data', obj.get_folder_name())

        if os.path.exists(user_folder):
            user_images = [f for f in os.listdir(user_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]
            if user_images:
                image_path = os.path.join('facial_data', obj.get_folder_name(), user_images[0])
                return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def get_orientation(self, obj):
        request = self.context.get('request')
        if obj.orientation and os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.orientation.name)):
            return request.build_absolute_uri(settings.MEDIA_URL + obj.orientation.name)
        return None

    def get_facial_data(self, obj):
        request = self.context.get('request')
        user_folder = os.path.join(settings.MEDIA_ROOT, 'facial_data', obj.get_folder_name())

        if os.path.exists(user_folder):
            user_images = [f for f in os.listdir(user_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]
            if user_images:
                image_path = os.path.join('facial_data', obj.get_folder_name(), user_images[0])
                return request.build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def get_my_comply(self, obj):
        request = self.context.get('request')
        if obj.my_comply and os.path.isfile(os.path.join(settings.MEDIA_ROOT, obj.my_comply.name)):
            return request.build_absolute_uri(settings.MEDIA_URL + obj.my_comply.name)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in ['picture', 'orientation', 'facial_data', 'my_comply']:
            if representation[field] is None:
                representation[field] = None
        return representation
    
    
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserEnrolled

class UserEnrolledSerializer11(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ('name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location', 'status', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return UserEnrolled.objects.create(**validated_data)


class UserEnrolledUpdateSerializer11(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ('name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location', 'status', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        # Hash the password if it's being updated
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['name', 'email', 'password']
    
    def validate_password(self, value: str) -> str:
        """Hash the password before saving."""
        return make_password(value)



from django.contrib.auth.hashers import check_password


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        if email and password:
            try:
                user = UserEnrolled.objects.get(email=email)
            except UserEnrolled.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not check_password(password, user.password):
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        
        data["user"] = user
        return data

from django.contrib.auth import get_user_model

class SignupSerializer_new(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    
class LoginSerializer_new(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email').lower()  # Convert to lowercase
        password = data.get('password')
        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            data['user'] = user
            return data
        raise serializers.ValidationError('Incorrect email or password.')

class UserSerializer_new(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')
        
        
class signup_app(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['name', 'email', 'password']
        
        
class LoginSerializerApp(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = UserEnrolled.objects.filter(email=email, password=password).first()
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        return data
    

from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializerApp1(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = UserEnrolled.objects.filter(email=email, password=password).first()
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        # Generate JWT token (if you want to do it here)
        refresh = RefreshToken.for_user(user)
        data['token'] = str(refresh.access_token)
        data['refresh_token'] = str(refresh)

        return data


from django.contrib.auth import get_user_model
from rest_framework import serializers

class SignupUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')
        # Note: You may want to exclude or include other fields as necessary
        
class SignupUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')
        read_only_fields = ('date_joined',)  # Prevent updating these fields

    


class UserEnrolledSerializerExpiry(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ('email', 'name', 'my_comply', 'expiry_date')
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'my_comply': {'required': False},
            'expiry_date': {'required': True}
        }

    def validate_email(self, value):
        # Check if the user exists
        try:
            user = UserEnrolled.objects.get(email=value)
            return user
        except UserEnrolled.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        
'''   
        
from rest_framework import serializers

class UpdateEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        exclude = ['password']

'''
        
    
class BulkUpdateByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    status = serializers.ChoiceField(choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ])
    
    
    
    
class UserEnrolledSerializer_update(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = '__all__'  # Or specify the fields you want to include
        read_only_fields = ('password',)

    def get_site_name(self, obj):
        return obj.site.name if obj.site else None
    


from rest_framework import serializers
from .models import Turnstile_S

class TurnstileUnlockSerializer(serializers.ModelSerializer):
    unlock = serializers.SerializerMethodField()

    class Meta:
        model = Turnstile_S
        fields = ['turnstile_id', 'unlock']

    def get_unlock(self, obj):
        """Convert the boolean field to 0 or 1."""
        return 1 if obj.unlock else 0


from .models import Site

class SubAdminSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['name']  # Adjust fields as needed
