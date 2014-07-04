'''
Created on 22-May-2014

@author: iqbal
'''
from django import forms
from django.contrib.auth.models import User
from eureka.models import *
   
class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text="Select a category")
    title = forms.CharField(help_text="Title")
    abstract = forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 40, 'style':'resize:none'}), help_text="Paste abstract (single paragraph)")
    keywords = forms.CharField(help_text="Keywords separated by comma")
    pdf = forms.FileField(help_text="Upload your article (format: PDF, max filesize: 10 MiB)")
    
    class Meta:
        model = Article
        fields = ('category','title','abstract','keywords','pdf')


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Enter a username")
    first_name = forms.CharField(help_text="Enter your firstname")
    last_name = forms.CharField(help_text="Enter your lastname", required=False)
    email = forms.CharField(help_text="Enter your email")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Enter a password")
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

      
class UserProfileForm(forms.ModelForm):
    
    UG_PG_CHOICES = (
                        ('','Select education level'),
                        ('UG','Undergraduate'),
                        ('PG','Postgraduate')
                     )
    
    PROF_CHOICES = (
                        ('','Select who you are'),
                        ('ST','Student'),
                        ('AL','Alumnus/alumna'),
                        ('LC','Lecturer'),
                        ('LS','Library Staff'),
                        ('AS','Administrative Staff'),
                        ('MS','Management Staff'),
                        ('OT','Other')
                    )
    
    DEPT_CHOICES = (
                        ('', 'Select department'),
                        ('CSE', 'Computer Science and Engineering'),
                        ('CS', 'Computer Science'),
                        ('ECE', 'Electronics and Communication Engineering'),
                        ('EEE', 'Electrical and Electronics Engineering'),
                        ('IT', 'Information Technology'),
                        ('EIE', 'Electronics and Instrumentation Engineering'),
                        ('MECH', 'Mechanical Engineering'),
                        ('CIV', 'Civil Engineering'),
                        ('VLSI', 'VLSI Design'),
                        ('ES', 'Embedded Systems'),
                        ('EPE', 'Electrical Power Engineering'),
                        ('WMC', 'Wireless and Mobile Communication')
                    )
    
    YEAR_CHOICES = (
                        ('','Select year'),
                        ('2003','2003'),
                        ('2004','2004'),
                        ('2005','2005'),
                        ('2006','2006'),
                        ('2007','2007'),
                        ('2008','2008'),
                        ('2009','2009'),
                        ('2010','2010'),
                        ('2011','2011'),
                        ('2012','2012'),
                        ('2013','2013'),
                        ('2014','2014'),
                        ('2015','2015')
                    )
    
    idnum = forms.CharField(help_text="Enter your ID number", max_length=12, required=False)
    isOutsider = forms.BooleanField(help_text="NOT belong to CVR?", widget = forms.CheckboxInput(attrs={'onclick' : "myFunction()"}), required=False) 
    profession = forms.ChoiceField(help_text="What is your profession?", widget=forms.Select(attrs={'onclick' : "myFunction1()"}), choices=PROF_CHOICES, required=False)
    ugorpg = forms.ChoiceField(help_text="Level of education taken in CVR", widget=forms.Select(), choices=UG_PG_CHOICES, required=False)
    dept = forms.ChoiceField(help_text="Department", widget=forms.Select(), choices=DEPT_CHOICES, required=False)
    exactprofession = forms.CharField(help_text="What is your profession?", required=False)
    place = forms.CharField(help_text="Where do you live in?", required=False)
    year = forms.ChoiceField(help_text="Left this college in", widget=forms.Select(), choices=YEAR_CHOICES, required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload", required=False)

    class Meta:
        model = UserProfile
        fields = ('idnum','isOutsider','profession','ugorpg','dept','exactprofession','place','year','picture')