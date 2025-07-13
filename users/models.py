from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name
    
class GalleryImage(models.Model):
    SITE_CHOICES = [
        ('Choutuppal', 'Choutuppal'),
        ('Yacharam', 'Yacharam'),
        ('Kothur', 'Kothur'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=20, choices=SITE_CHOICES)
    image = models.ImageField(upload_to='gallery_images/')

    def __str__(self):
        return f"{self.site} - {self.title or self.image.name}"