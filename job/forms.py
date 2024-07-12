from django import forms
from django.contrib.auth.models import User
from .models import StudentUser

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password does not match")

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = ['mobile', 'image', 'gender','skill_list']

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    image = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(StudentUserForm, self).__init__(*args, **kwargs)
        self.fields['mobile'].required = True

class JobSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Jobs')


# forms.py

from django import forms
from .models import Apply

from django import forms
from .models import Apply

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Apply.STATUS_CHOICES)
        }

