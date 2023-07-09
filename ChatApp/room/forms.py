from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'slug', 'psswd']

class deleteRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['psswd']

class enterRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['psswd']