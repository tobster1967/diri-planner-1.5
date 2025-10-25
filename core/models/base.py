import uuid
from django.db import models
from django.utils.text import slugify

class Base(models.Model):
    """
    Base model providing common fields for all application models:
    - UUID primary key for better security and distributed systems
    - Automatic timestamp tracking (created_at, updated_at)
    - Automatic slug generation from name field
    - Default ordering by creation date (newest first)
    
    All models in the application should inherit from this base class.
    
    To use automatic slug generation, models must have a 'name' field.
    Models can override SLUG_FIELD to use a different field for slug generation.
    """
    
    # Class attribute to specify which field to use for slug generation
    # Override this in child models if needed
    SLUG_FIELD = 'name'
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this record"
    )
    
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Unique slug identifier (auto-generated from name)",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from SLUG_FIELD if not provided."""
        if not self.slug:
            # Get the field value to generate slug from
            slug_source = getattr(self, self.SLUG_FIELD, None)
            if slug_source:
                base_slug = slugify(slug_source)
                slug = base_slug
                counter = 1
                
                # Get the model class for querying
                model_class = self.__class__
                
                # Ensure uniqueness
                while model_class.objects.filter(slug=slug).exclude(id=self.id).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                self.slug = slug
        
        super().save(*args, **kwargs)