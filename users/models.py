from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

CATEGORIES = (
    ('ARCHITECTURE', 'Architecture'),
    ('ARTWORK', 'Artwork'),
    ('BIOLOGY', 'Biology'),
    ('BUSINESS', 'Business'),
    ('CHEMISTRY', 'Chemistry'),
    ('ECONOMICS', 'Economics'),
    ('ENGINEERING', 'Engineering'),
    ('ENGLISH', 'English Literature'),
    ('HISTORY', 'History'),
    ('LAW', 'Law'),
    ('MATH', 'Math'),
    ('MEDICINE', 'Medicine'),
    ('MUSIC', 'Music'),
    ('PHILOSOPHY', 'Philosophy'),
    ('PHYSICS', 'Physics'),
    ('POLITICS', 'Politics'),
    ('PSYCHOLOGY', 'Psychology'),
    ('SCIENCE', 'Science'),
    ('SOCIOLOGY', 'Sociology'),
    ('SOFTWARE', 'Software Development'),
    ('OTHER', 'Other')

)
class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(User, related_name='projects', blank=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default='OTHER')
    due_date = models.DateField(blank=True, null = True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_reviewers = models.PositiveIntegerField(default=1)
    is_private = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    upvoters = models.ManyToManyField(User, related_name='upvoted_projects', blank=True)

    @property
    def current_reviewers_count(self):
        return self.members.count() - 1
    rubric = models.FileField(upload_to='rubrics/', blank=True, null=True)
    review_guidelines = models.FileField(upload_to='review_guidelines/', blank=True, null=True)

    def __str__(self):
        return self.name

class Upload(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files', null=False)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(default=now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='uploads')
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=200, blank=True, null=True)
    transcription_job_name = models.CharField(max_length=255, blank=True, null=True)
    output_key = models.CharField(max_length=255, blank=True, null=True)  # Add this line

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'project'], name='unique_upload_name_per_project')
        ]

    def __str__(self):
        return self.file.name

class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.status})"

class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Prompt(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='prompts')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PromptResponse(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    specializations = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class ProjectInvitation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['project', 'invited_user']

class ProjectMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} in {self.project.name} since {self.date_added}"
