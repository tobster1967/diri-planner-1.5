from django.db import models
from .base_model import BaseModel

class Application(BaseModel):
    """
    Application model representing an application entity with unique identification,
    descriptive attributes, and extensible properties.
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the application.",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the application.",
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent application for hierarchical structure.",
    )
    properties = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional properties for extensibility.",
    )

    def __str__(self):
        return self.name