from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='faculty')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Caurse(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.name