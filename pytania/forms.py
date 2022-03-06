from django import forms

class GeneratedTest(forms.Form):
	title = forms.CharField(label='title')
	your_name = forms.CharField(label='Your name')
	def __init__(self, *args, **kwargs):
		super(GeneratedTest, self).__init__(*args, **kwargs)