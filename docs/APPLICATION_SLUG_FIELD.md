# Application Slug Field

## Overview

The Application model includes a slug field that provides URL-friendly identifiers for applications. Slugs are automatically generated from the application name and are guaranteed to be unique.

## Features

- **Automatic Generation**: Slugs are auto-generated from the `name` field using Django's `slugify()` function
- **Uniqueness**: The slug field has a unique constraint to prevent duplicates
- **Collision Handling**: If a generated slug already exists, a counter is appended (e.g., "test-app", "test-app-1", "test-app-2")
- **Manual Override**: While slugs are auto-generated, they can be manually set if needed
- **Read-only in Admin**: The slug field is displayed but read-only in the Django admin interface

## Implementation Details

### Model Field

```python
slug = models.SlugField(
    max_length=255,
    unique=True,
    blank=True
)
```

### Auto-generation Logic

The `save()` method includes logic to generate unique slugs:

```python
def save(self, *args, **kwargs):
    if not self.slug:
        from django.utils.text import slugify
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
        # Handle collisions by appending counter
        while Application.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        self.slug = slug
    super().save(*args, **kwargs)
```

## Usage Examples

### Creating Applications

```python
from core.models import Application

# Slug is auto-generated from name
app1 = Application.objects.create(name="My Application")
print(app1.slug)  # Output: my-application

# Duplicate names get unique slugs with counter
app2 = Application.objects.create(name="My Application")
print(app2.slug)  # Output: my-application-1

app3 = Application.objects.create(name="My Application")
print(app3.slug)  # Output: my-application-2
```

### Using Slugs in URLs

Slugs are perfect for creating clean, readable URLs:

```python
from django.urls import path
from core.views import ApplicationDetailView

urlpatterns = [
    path('app/<slug:slug>/', ApplicationDetailView.as_view(), name='app_detail'),
]
```

### Querying by Slug

```python
# Get application by slug
app = Application.objects.get(slug='my-application')

# Filter by slug
apps = Application.objects.filter(slug__startswith='test-')
```

## Admin Interface

In the Django admin:
- The slug field is displayed in the list view
- It's read-only to prevent manual conflicts
- New applications automatically get slugs when saved through the model's `save()` method
- The slug appears after saving the application

## Migration History

The slug field was added through a multi-step migration process:

1. **Migration 0003**: Added nullable slug field
2. **Data Migration**: Populated slugs for existing records
3. **Migration 0004**: Added unique constraint

This approach prevented data integrity issues with existing records.

## Best Practices

1. **Don't Modify Slugs**: Once an application is created and potentially referenced elsewhere, avoid changing its slug to maintain consistency
2. **Use Slugs in URLs**: Always use slugs instead of IDs in public-facing URLs for better SEO and readability
3. **Index Considerations**: The unique constraint automatically creates an index for efficient lookups
4. **Name Changes**: If an application name changes, the slug remains unchanged (by design) to maintain URL stability

## Troubleshooting

### Issue: Duplicate Slug Error

If you manually set a slug that already exists:
```python
IntegrityError: duplicate key value violates unique constraint "core_application_slug_key"
```

**Solution**: Let the system auto-generate the slug or choose a different slug manually.

### Issue: Slug Not Generated

If a slug isn't auto-generated, ensure:
- The `name` field is set before saving
- You're not explicitly setting `slug` to `None` or empty string
- The `save()` method is being called (bulk operations may bypass it)

## Related Documentation

- [`core/models/application.py`](../core/models/application.py) - Application model definition
- [`core/admin/application_admin.py`](../core/admin/application_admin.py) - Admin configuration
- [Django SlugField Documentation](https://docs.djangoproject.com/en/5.2/ref/models/fields/#slugfield)