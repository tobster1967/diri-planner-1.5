from django.db import models
from treenode.models import TreeNodeModel
from .base import Base


class Organisation(TreeNodeModel, Base):
    """
    Hierarchical organisation model using django-fast-treenode for efficient tree queries.
    Organisations can have parent-child relationships forming a tree structure.
    
    Tree fields provided by django-fast-treenode:
    - parent: The parent node (ForeignKey to self)
    - _depth: The depth level in the tree (0 for root nodes)
    - _path: Path for efficient tree queries
    - _left: Left value for MPPT
    - _right: Right value for MPPT
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the organisation.",
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the organisation.",
    )
    
    code = models.CharField(
        max_length=50,
        blank=True,
        help_text="Short code or abbreviation for the organisation.",
    )
    
    email = models.EmailField(
        blank=True,
        help_text="Contact email for the organisation.",
    )
    
    phone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Contact phone number for the organisation.",
    )
    
    address = models.TextField(
        blank=True,
        help_text="Physical address of the organisation.",
    )
    
    website = models.URLField(
        blank=True,
        help_text="Website URL of the organisation.",
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this organisation is active.",
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata for the organisation.",
    )
    
    class Meta:
        ordering = ['_path']
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        # Add visual indentation for tree display using em dash like in admin
        indent = '—' * self._depth
        name_with_indent = f"{indent} {self.name}" if indent else self.name
        parent_name = self.parent.name if self.parent else ""
        return f"{name_with_indent} ({parent_name})" if parent_name else name_with_indent
    
    def get_full_path(self):
        """Get the full path of the organisation in the tree."""
        if self.parent:
            return f"{self.parent.get_full_path()}.{self.slug}"
        return self.slug
    
    @property
    def level(self):
        """Get the level of this organisation in the tree (0 for root)."""
        return self._depth
    
    def get_descendants_count(self):
        """Get the number of descendants."""
        return self.get_descendants().count()
    
    def get_children_count(self):
        """Get the number of direct children."""
        return self.get_children().count()