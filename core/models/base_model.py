import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Base model providing common fields for all application models:
    - UUID primary key for better security and distributed systems
    - Automatic timestamp tracking (created_at, updated_at)
    - Default ordering by creation date (newest first)
    
    All models in the application should inherit from this base class.
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this record"
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