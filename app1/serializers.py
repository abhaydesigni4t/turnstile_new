from rest_framework import serializers
from .models import UserEnrolled,Asset,Site,Notification,Upload_File,Turnstile_S,Orientation,PreShift,ToolBox



class ActionStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AssetSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=True)
    footage = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Asset
        fields = ['asset_id', 'picture', 'asset_name', 'tag_id', 'footage', 'description', 'asset_category', 'status']
    def validate(self, data):
        # Perform any additional validation here if needed
        return data
    
    

class UserEnrolledSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    class Meta:
        model = UserEnrolled
        exclude = ['sr','password','site']

    def get_picture(self, obj):
        request = self.context.get('request')
        user_folder = os.path.join(settings.MEDIA_ROOT, 'facial_data', obj.get_folder_name())
        if os.path.exists(user_folder):
            user_images = [f for f in os.listdir(user_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]
            if user_images:
                image_path = os.path.join('facial_data', obj.get_folder_name(), user_images[0])
                image_url = request.build_absolute_uri(settings.MEDIA_URL + image_path)
                return image_url
        return None
    
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
    


class PreShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreShift
        fields = ['document', 'date']

class ToolBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolBox
        fields = ['document', 'date']


from rest_framework import serializers

class FacialImageDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    facial_data = serializers.ListField(child=serializers.ImageField())


# serializers.py
from rest_framework import serializers
from .models import UserEnrolled

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserEnrolled
        fields = ['name', 'company_name', 'job_role', 'mycompany_id', 'job_location', 'email']
       
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

class OnSiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnSiteUser
        fields = ['name', 'tag_id', 'status']


class OnsiteGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnSiteUser
        fields = ['name', 'tag_id', 'status', 'timestamp']


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
        
        
        
class UpdateEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        exclude = ['password']
        
    
class BulkUpdateByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    status = serializers.ChoiceField(choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ])
    
    
    

