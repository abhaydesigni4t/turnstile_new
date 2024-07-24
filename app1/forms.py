from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Upload_data,Asset,Site,company,UserEnrolled,Notification,timeschedule,Turnstile_S,Orientation,PreShift,ToolBox
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            from django.contrib.auth import authenticate
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data

class YourModelForm(forms.ModelForm):
    class Meta:
        model = UserEnrolled
        fields = ['name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location', 'orientation', 'facial_data', 'my_comply', 'expiry_date', 'status', 'email', 'site']
        widgets = {
            'orientation': forms.ClearableFileInput(attrs={'accept': 'application/pdf, application/msword, image/jpeg, image/jpg'}),
            'expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),  # jQuery UI datepicker
        }
        labels = {
            'orientation': 'Orientation:',
            'expiry_date': 'Expiry Date:',  # Label for expiry date
        }
    #job_role = forms.ChoiceField(choices=UserEnrolled.job_role, widget=forms.Select(attrs={'class': 'form-control'}))

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['subject', 'description', 'username']

class upload_form(forms.ModelForm):
    class Meta:
        model = Upload_data
        fields = ['uploaded_file']

class AssetForm(forms.ModelForm):
    asset_category_choices = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'), 
    ]
    asset_category = forms.ChoiceField(choices=asset_category_choices)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Asset
        fields = [ 'asset_id','picture','asset_name', 'tag_id', 'footage' , 'description', 'asset_category','status','location','site']
      
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['picture','name','location']

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.upper()

class CompanyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = '__all__'
        widgets = {
            'safety_insurance': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.jpeg,.jpg'}),
        }
        
class timescheduleForm(forms.ModelForm):
    class Meta:
        model = timeschedule
        fields = '__all__'

class TurnstileForm(forms.ModelForm):
    class Meta:
        model = Turnstile_S
        fields = ['turnstile_id','location','safety_confirmation']

class OrientationForm(forms.ModelForm):
    class Meta:
        model = Orientation
        fields = ['attachments']

class PreshitForm(forms.ModelForm):
    class Meta:
        model = PreShift
        fields = ['document','site']

class ToolboxForm(forms.ModelForm):
    class Meta:
        model = ToolBox
        fields = ['document','site']


from django import forms
from .models import UserEnrolled


class SingleFileUploadForm(forms.Form):
    facial_data = forms.ImageField(required=True)

    
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserEnrolled
        fields = ('name', 'email', 'password', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserEnrolled.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists in the authentication system.")
        return email

    def save(self, commit=True):
        user_enrolled = super(SignUpForm, self).save(commit=False)
        password = self.cleaned_data["password"]

        user_enrolled.status = 'active' 
        
        if commit:
            # Save the UserEnrolled instance
            user_enrolled.save()

            # Create a corresponding CustomUser instance
            custom_user = CustomUser(
                email=user_enrolled.email,
                first_name=user_enrolled.name
            )
            custom_user.set_password(password)
            custom_user.save()

        return user_enrolled


class SignUpForm_new(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password','company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class LoginForm_new(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    

from django import forms
from .models import CustomUser, Site

class SubAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    sites = forms.ModelMultipleChoiceField(
        queryset=Site.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'company_name', 'job_role', 'mycompany_id', 'tag_id', 'job_location', 'password', 'sites']