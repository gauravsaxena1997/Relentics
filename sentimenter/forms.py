from django import forms

class userinput(forms.Form):
    q=forms.CharField(required=True,max_length=25,label='Input #Hashtag')