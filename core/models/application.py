from django.db import models
from treenode.models import TreeNodeModel

from .attribute import Attribute
from .base import Base
from .organisation import Organisation


class Application(TreeNodeModel, Base):
    """
    Hierarchical application model using django-fast-treenode for efficient tree queries.
    Applications can have parent-child relationships forming a tree structure.

    Tree fields provided by django-fast-treenode:
    - parent: The parent node (ForeignKey to self)
    - _depth: The depth level in the tree (0 for root nodes)
    - _path: Path for efficient tree queries
    - _left: Left value for MPPT
    - _right: Right value for MPPT
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the application.",
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed description of the application.",
    )

    properties = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional properties for extensibility.",
    )

    attributes = models.ManyToManyField(
        Attribute,
        blank=True,
        related_name="applications",
        help_text="Attributes associated with this application.",
    )

    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        related_name="applications",
        help_text="Organisations associated with this application.",
    )

    class Meta:
        ordering = ["_path"]
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        # Add visual indentation for tree display using em dash like in admin
        indent = "—" * self._depth
        name_with_indent = f"{indent} {self.name}" if indent else self.name
        parent_name = self.parent.name if self.parent else ""
        return f"{name_with_indent} ({parent_name})" if parent_name else name_with_indent

    def get_full_path(self):
        """Get the full path of the application in the tree."""
        if self.parent:
            return f"{self.parent.get_full_path()}.{self.slug}"
        return self.slug

    @property
    def level(self):
        """Get the level of this application in the tree (0 for root)."""
        return self._depth

    def get_descendants_count(self):
        """Get the number of descendants."""
        return self.get_descendants().count()

    def get_children_count(self):
        """Get the number of direct children."""
        return self.get_children().count()
