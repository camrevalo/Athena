from django import forms
from users.models import UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model =UserProfile
		fields = ('firstName', 'lastName', 'school', 'picture', 'isTeacher')

class EditProfileForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        profile = kwargs.pop('profile')
        super(EditProfileForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].initial=profile.firstName
        self.fields['last_name'].initial=profile.lastName
        self.fields['picture'].initial=profile.picture
        self.fields['school'].initial=profile.school

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    picture = forms.CharField(required=True)
    school = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ('school', 'picture',)

    def clean_pic(self):
        picture = self.cleaned_data.get('picture')
        return picture

    def clean_firstname(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    def clean_lastname(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name

    def clean_school(self):
        school = self.cleaned_data.get('school')
        return school

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.userprofile.picture = self.cleaned_data['picture']
        user.userprofile.firstName = self.cleaned_data['first_name']
        user.userprofile.lastName = self.cleaned_data['last_name']
        user.userprofile.school = self.cleaned_data['school']
        if commit:
            user.save()
            user.userprofile.save()

        return user
