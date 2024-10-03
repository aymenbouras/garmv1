from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Utilitaire pour générer des slugs uniques
def unique_slugify(instance, slug_field, name_field):
    slug = slugify(getattr(instance, name_field))
    model_class = instance.__class__
    unique_slug = slug
    num = 1
    while model_class.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

# Modèle pour les cours de certification
class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Généré automatiquement
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Durée estimée en heures")
    cover_image = models.ImageField(upload_to='course_covers/', blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='courses')
    certification_exam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def pre_save_course_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slugify(instance, 'slug', 'name')

pre_save.connect(pre_save_course_slug, sender=Course)

# Modèle pour les chapitres
class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()
    estimated_time = models.PositiveIntegerField(help_text="Temps estimé pour compléter ce chapitre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.name}"

def pre_save_chapter_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slugify(instance, 'slug', 'name')

pre_save.connect(pre_save_chapter_slug, sender=Chapter)

# Modèle pour les sous-chapitres
class SubChapter(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='subchapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()
    media_file = models.FileField(upload_to='subchapter_media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.name} - {self.name}"

def pre_save_subchapter_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slugify(instance, 'slug', 'name')

pre_save.connect(pre_save_subchapter_slug, sender=SubChapter)


class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('image', 'Image'),
    )
    chapter = models.ForeignKey(Chapter, related_name='media', on_delete=models.CASCADE, blank=True, null=True)
    subchapter = models.ForeignKey(SubChapter, related_name='media', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media_files/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.media_type}"

def pre_save_media_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slugify(instance, 'slug', 'name')

pre_save.connect(pre_save_media_slug, sender=Media)
