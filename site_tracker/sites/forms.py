from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import ConsructionSite, SiteImage


class ConsructionSiteForm(forms.ModelForm):
    class Meta:
        model = ConsructionSite
        fields = '__all__'
        labels = {
            'engineer_incharge': 'Engineer In-Charge',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Riverside Tower — Phase 2',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kochi, Kerala',
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g. 2500000',
            }),
            'engineer_incharge': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Arjun Menon',
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notes, milestones, or blockers…',
            }),
        }


class SiteImageForm(forms.ModelForm):
    class Meta:
        model = SiteImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional caption, e.g. "Foundation work — August 2026"',
            }),
        }


class StyledAuthenticationForm(AuthenticationForm):
    """
    Wraps Django's built-in login form to add Bootstrap styling,
    so the staff login page matches the rest of the site.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
