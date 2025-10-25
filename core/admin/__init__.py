"""
Admin interface registration for core app models.
All admin classes should be imported here to be automatically registered with Django.
"""

from .application_admin import ApplicationAdmin
from .attribute_admin import AttributeAdmin
from .organisation_admin import OrganisationAdmin

__all__ = ['ApplicationAdmin', 'AttributeAdmin', 'OrganisationAdmin']