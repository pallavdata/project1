from django import forms
import re
from .models import Job,Apply,Login_Accounts,Mcq
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import UserCreationForm


class adddata(forms.ModelForm):
    question = forms.CharField(max_length=1200)
    answer = forms.CharField(max_length=240)
    option2 = forms.CharField(max_length=240)
    option3 = forms.CharField(max_length=240)
    option4 = forms.CharField(max_length=240)
    class Meta:
        model = Mcq
        fields = ['question','answer','option2','option3','option4']

class login_form(forms.ModelForm):
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Login_Accounts
        fields = ['email','password']

        


class RegForm(UserCreationForm):
    username = forms.CharField(min_length=4,max_length=255,label="Username", widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255,label="Email Id", widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(min_length=8,max_length=16,label="Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(min_length=8,max_length=16,label="Re Enter Password", widget = forms.PasswordInput(attrs={'class': 'form-control'}), help_text = "Enter the same password as above, for verification.")

    class Meta:
        model = Login_Accounts
        fields = ['username','email','password1','password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


    def clean(self):
        super(RegForm, self).clean()
        # print ("here is " + str(self.cleaned_data))
        password = self.cleaned_data['password1']
        try:
            pass2 = self.cleaned_data['password2']
        except:
            pass2 = ""


        pattern = re.compile('[A-Z]')
        pattern2 = re.compile('[a-z]')
        pattern3 = re.compile('[0-9]')
        pattern4 = re.compile('[!@#$%^&*(),.?":{}|<>]')

        if not pattern.search(password) or not pattern2.search(password) or not pattern3.search(password) or not pattern4.search(password):
                list = ['should contain at least one upper case','should contain at least one lower case','should contain at least one digit','should contain at least one Special character']
                self.add_error('password1',list)
                try:
                    del self._errors['password2']
                except:
                    pass

        else:
            if password != pass2:
                error_message = 'Password did not matched. Enter the same password as above'
                field = 'password2'
                # if self._errors['password2']:
                #     del self._errors['password2']
                try:
                    del self._errors['password2']
                except:
                    pass
                self.add_error(field,error_message)
        return self.cleaned_data




    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Login_Accounts.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")
        

    def clean_username(self):
        username = self.cleaned_data['username']
        print("username "+ str(username))
        try:
            user_name = Login_Accounts.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")



# LOCATION_COICES = [ ( "AN", "Andaman and Nicobar Islands" ), ( "AP", "Andhra Pradesh" ),
# ( "AR", "Arunachal Pradesh" ), ( "AS", "Assam" ), ( "BR", "Bihar" ), ( "CG", "Chandigarh" ),
# ( "CH", "Chhattisgarh" ), ( "DH", "Dadra and Nagar Haveli" ), ( "DD", "Daman and Diu" ),
# ( "DL", "Delhi" ), ( "GA", "Goa" ), ( "GJ", "Gujarat" ), ( "HR", "Haryana" ),
# ( "HP", "Himachal Pradesh" ), ( "JK", "Jammu and Kashmir" ), ( "JH", "Jharkhand" ),
# ( "KA", "Karnataka" ), ( "KL", "Kerala" ), ( "LD", "Lakshadweep" ), ( "MP", "Madhya Pradesh" ),
# ( "MH", "Maharashtra" ), ( "MN", "Manipur" ), ( "ML", "Meghalaya" ), ( "MZ", "Mizoram" ),
# ( "NL", "Nagaland" ), ( "OR", "Odisha" ), ( "PY", "Puducherry" ), ( "PB", "Punjab" ),
# ( "RJ", "Rajasthan" ), ( "SK", "Sikkim" ), ( "TN", "Tamil Nadu" ), ( "TS", "Telangana" ),
# ( "TR", "Tripura" ), ( "UK", "Uttar Pradesh" ), ( "UP", "Uttarakhand" ),("WB","West Bengal") ]
##admin file
class jobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['creation_date','skills','location']
class Apply_form(forms.ModelForm):
    resume = forms.FileField(validators=[FileExtensionValidator( ['pdf'] ) ])
    class Meta:
        model = Apply
        fields = ['gender','email_id','edu_year','edu_collage_name','edu_marks','internship','img','resume']
    # def __init__(self, *args, **kwargs):
    #     super(Apply_form, self).__init__(*args, **kwargs)
    #     self.fields['internship'].required = False
    

        