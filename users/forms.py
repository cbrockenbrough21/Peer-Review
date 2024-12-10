from django import forms
from .models import Upload
from .models import Project, Prompt, PromptResponse, UserProfile
from django.contrib.auth.models import User


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['name', 'file', 'description', 'keywords']
    
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)  # Pass project from view to the form
        super(FileUploadForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Ensure 'project' is provided
        if not self.project:
            raise forms.ValidationError("Project is required to validate uniqueness.")

        # Check if a file with the same name exists in the project
        if Upload.objects.filter(name=name, project=self.project).exists():
            raise forms.ValidationError("An upload with this name already exists in the project.")
        
        return name

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)  # Pop the owner argument
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.project_instance = kwargs.get('instance', None)

        if self.project_instance:
            self.fields['name'].disabled = True
           

    def clean_name(self):
        name = self.cleaned_data['name']

        # Check if a project with the same name exists for the user
        if Project.objects.filter(name=name, owner=self.owner).exists():
            raise forms.ValidationError("A project with this name already exists in your account. Please choose a different name.")

        return name
    def clean_number_of_reviewers(self):
        number_of_reviewers = self.cleaned_data.get('number_of_reviewers')

        if self.project_instance:
            # Calculate the number of current members
            current_members_count = self.project_instance.members.count()
            # Ensure number of reviewers is greater than current members count
            if number_of_reviewers <= current_members_count - 1:
                raise forms.ValidationError(
                    f'The number of reviewers must be greater than or equal to the current number of non-owner members ({current_members_count - 1}).'
                )

        return number_of_reviewers

    class Meta:
        model = Project
        fields = ['name', 'description','rubric', 'review_guidelines', 'due_date', 'category', 'number_of_reviewers', 'is_private']
        labels = {
            'number_of_reviewers': 'Number of Reviewers',
            'is_private': 'Private Project',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'number_of_reviewers': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)  # Pop the owner argument
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        self.project_instance = kwargs.get('instance', None)

        if self.project_instance:
            self.fields['name'].disabled = True
           

    def clean_name(self):
        name = self.cleaned_data['name']

        # Check if a project with the same name exists for the user
        if Project.objects.filter(name=name, owner=self.owner).exists():
            raise forms.ValidationError("A project with this name already exists in your account. Please choose a different name.")

        return name
    def clean_number_of_reviewers(self):
        number_of_reviewers = self.cleaned_data.get('number_of_reviewers')

        if self.project_instance:
            # Calculate the number of current members
            current_members_count = self.project_instance.members.count()
            # Ensure number of reviewers is greater than current members count
            if number_of_reviewers < current_members_count - 1:
                raise forms.ValidationError(
                    f'The number of reviewers must be greater than or equal to the current number of non-owner members ({current_members_count - 1}).'
                )

        return number_of_reviewers

    class Meta:
        model = Project
        fields = ['name', 'description', 'due_date', 'category', 'number_of_reviewers', 'is_private']
        labels = {
            'number_of_reviewers': 'Number of Reviewers',
            'is_private': 'Private Project',
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'number_of_reviewers': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your prompt here...',
                'rows': 3,   # Adjust the number of rows as needed
                'cols': 50,  # Adjust the number of columns as needed
                'style': 'width: 100%; max-width: 100%;',  # Ensures it’s responsive
            }),
        }

class PromptResponseForm(forms.ModelForm):
    class Meta:
        model = PromptResponse
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your response...',
                'rows': 5,   # Adjust the number of rows as needed
                'cols': 80,  # Adjust the number of columns as needed
                'style': 'width: 100%; max-width: 100%;',  # Ensures it’s responsive
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'specializations', 'linkedin', 'github', 'twitter']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short bio about yourself',
                'rows': 3,
            }),
            'specializations': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your specializations',
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your LinkedIn profile URL',
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your GitHub profile URL',
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Twitter profile URL',
            }),
        }

class UploadMetaDataForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['name', 'description', 'keywords']
        
import re
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        }
        help_texts = {
            'username': None,  # Remove the default help text for the username field
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Ensure the username is unique, excluding the current user's username
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f'Username "{username}" is not available.')

        # Restrict characters to letters and numbers only
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError("Username can only contain letters and numbers.")

        return username