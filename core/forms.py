from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import UserProfile, Grade

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'})
    )
    school = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maktab'})
    )
    grade = forms.ChoiceField(
        choices=[(str(i), f"{i}-sinf") for i in range(8, 12)],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class_group = forms.ChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            try:
                # O'quvchi sinfini olish
                grade_number = int(self.cleaned_data['grade'])
                grade_obj = Grade.objects.get_or_create(number=grade_number)[0]
                
                # Agar profil mavjud bo'lsa, yangilaymiz
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'grade': grade_obj,
                        'school': self.cleaned_data['school'],
                        'class_group': self.cleaned_data['class_group']
                    }
                )
            except Exception as e:
                # Xatolik bo'lsa userni o'chiramiz
                user.delete()
                raise e
            
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('school', 'grade', 'class_group', 'phone', 'address', 'bio', 'avatar', 
                  'website', 'github', 'twitter', 'instagram')