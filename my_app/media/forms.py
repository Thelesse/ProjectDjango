from django import forms

#here is ready method in django to create form instead of making form by html
#for doing that you need to make a class for every form that you want to pass in html
#here we have form for register, sign-in, posting ....
class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=40, label="user name",required=True)
    name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(max_length=100, required=True)


class SignIn(forms.Form):
    user_name = forms.CharField(max_length=40, label="user name", required=True)
    password = forms.CharField(max_length=100, required=True)


class Posting(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    text = forms.CharField(max_length=400, required=True)


class Commenting(forms.Form):
    text = forms.CharField(max_length=400, required=True)


class SearchForm(forms.Form):
    start_date = forms.DateTimeField()
    finish_date = forms.DateTimeField()
    user = forms.CharField(max_length=40)