from django import forms
from .models import Meep,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProfilePicForm(forms.ModelForm):
    profile_img = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile-Bio'}))
    homepage_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HomePage Link'}))
    facebook_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}))
    instagram_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}))
    github_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Link'}))
    linkedin_link = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Linkedin Link'}))
    class Meta:
        model = Profile
        fields = ('profile_img','profile_bio','homepage_link','facebook_link','instagram_link','github_link','linkedin_link')


class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder":"Enter your mascur meep",
                                   "class":"form-control",
                               }
                           ),
                           label="",
                           )
    class Meta:
        model = Meep
        exclude=("user","likes")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    first_name = forms.CharField(label="",max_length=100,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))

    last_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter UserName'
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


