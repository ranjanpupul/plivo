from django import forms

class UserExitForm(forms.Form):
	message = forms.CharField(required=True, label=('Write your Concern overhere'), )
	tonumber = forms.IntegerField(required=True, label=('To Number'))
	fromnumber= forms.IntegerField(required=True, label=('From Number'))

	def __init__(self, *args, **kwargs):
		super(UserExitForm, self).__init__(*args, **kwargs)
		self.fields['tonumber'].widget.attrs['class'] = "form-control"
		self.fields['fromnumber'].widget.attrs['class'] = "form-control"
		self.fields['message'].widget.attrs['class'] = "form-control"
		self.fields['tonumber'].widget.attrs['required'] = "true"
		self.fields['fromnumber'].widget.attrs['required'] = "true"
		self.fields['message'].widget.attrs['required'] = "true"

