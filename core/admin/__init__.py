"""
Admin interface registration for core app models.
All admin classes should be imported here to be automatically registered with Django.
"""

from .application_admin import ApplicationAdmin

__all__ = ['ApplicationAdmin']