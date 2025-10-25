from django.db import models
from treenode.models import TreeNodeModel
from .base import Base


class Attribute(TreeNodeModel, Base):
    """
    Hierarchical attribute model using django-fast-treenode for efficient tree queries.
    Attributes can have parent-child relationships forming a tree structure.
    
    Tree fields provided by django-fast-treenode:
    - tn_parent: The parent node (ForeignKey to self)
    - tn_depth: The depth level in the tree (0 for root nodes)
    - tn_left: Left value for MPTT
    - tn_right: Right value for MPTT
    - tn_priority: Priority for ordering siblings
    """
    
    name = models.CharField(
        max_length=255,
        help_text="Name of the attribute"
    )
    
    value = models.TextField(
        blank=True,
        help_text="Value of the attribute"
    )
    
    data_type = models.CharField(
        max_length=50,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('float', 'Float'),
            ('boolean', 'Boolean'),
            ('date', 'Date'),
            ('datetime', 'DateTime'),
            ('json', 'JSON'),
        ],
        default='string',
        help_text="Data type of the attribute value"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description of what this attribute represents"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this attribute is active"
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata for the attribute"
    )
    
    class Meta:
        ordering = ['_path']
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        # Add visual indentation for tree display using em dash like in admin
        indent = '—' * self._depth
        name_with_indent = f"{indent} {self.name}" if indent else self.name
        parent_name = " (" + self.parent.name + ")" if self.parent else ""
        return f"{name_with_indent}{parent_name}"
    
    def get_full_path(self):
        """Get the full path of the attribute in the tree."""
        if self.parent:
            return f"{self.parent.get_full_path()}.{self.slug}"
        return self.slug
    
    @property
    def level(self):
        """Get the level of this attribute in the tree (0 for root)."""
        return self._depth
    
    def get_descendants_count(self):
        """Get the number of descendants."""
        return self.get_descendants().count()
    
    def get_children_count(self):
        """Get the number of direct children."""
        return self.get_children().count()