from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    CASTE_CATEGORY_CHOICES = [
        ('GEN', 'General'),
        ('OBC', 'Other Backward Class'),
        ('SC', 'Scheduled Caste'),
        ('ST', 'Scheduled Tribe'),
        ('EWS', 'Economically Weaker Section'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Academic Information
    current_education_level = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=200)
    current_year = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # Personal Information
    caste_category = models.CharField(max_length=3, choices=CASTE_CATEGORY_CHOICES)
    family_income = models.DecimalField(max_digits=10, decimal_places=2, help_text="Annual family income in INR")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Additional Information
    disabilities = models.TextField(blank=True, null=True, help_text="List any disabilities (if applicable)")
    extracurricular_activities = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"


class Scholarship(models.Model):
    SCHOLARSHIP_TYPES = [
        ('MERIT', 'Merit-based'),
        ('MEANS', 'Means-based'),
        ('SPORTS', 'Sports'),
        ('MINORITY', 'Minority'),
        ('GENDER', 'Gender-specific'),
        ('DISABILITY', 'For disabled students'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    provider = models.CharField(max_length=200)
    
    # Financial Information
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Scholarship amount in INR")
    is_fully_funded = models.BooleanField(default=False, help_text="If fully funded, amount will be ignored")
    
    # Eligibility Criteria
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    eligible_education_levels = models.JSONField(default=list, help_text="List of eligible education levels")
    eligible_fields_of_study = models.JSONField(default=list, help_text="List of eligible fields of study")
    eligible_caste_categories = models.JSONField(default=list, help_text="List of eligible caste categories")
    min_family_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Minimum family income in INR (if applicable)")
    max_family_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum family income in INR (if applicable)")
    eligible_states = models.JSONField(default=list, help_text="List of eligible states (empty for all-India)")
    
    # Application Details
    application_deadline = models.DateField()
    application_link = models.URLField()
    is_active = models.BooleanField(default=True)
    
    # Metadata
    scholarship_type = models.CharField(max_length=20, choices=SCHOLARSHIP_TYPES)
    tags = models.JSONField(default=list, help_text="Tags for better categorization")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-application_deadline']


class ScholarshipMatch(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='matches')
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='matches')
    
    # Match Metrics
    eligibility_score = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    match_reason = models.TextField(help_text="AI-generated explanation of why this scholarship is a good match")
    
    # Application Status
    is_applied = models.BooleanField(default=False)
    application_date = models.DateTimeField(null=True, blank=True)
    application_status = models.CharField(
        max_length=20,
        choices=[
            ('NOT_APPLIED', 'Not Applied'),
            ('IN_PROGRESS', 'Application in Progress'),
            ('SUBMITTED', 'Submitted'),
            ('AWARDED', 'Awarded'),
            ('REJECTED', 'Rejected'),
        ],
        default='NOT_APPLIED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'scholarship')
        verbose_name_plural = 'Scholarship Matches'
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.scholarship.name} ({self.eligibility_score}%)"

