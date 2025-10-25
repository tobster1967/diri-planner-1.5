# Dynamic Forms Setup Quick Reference

## What Changed

Your Attribute admin now uses `django-dynamic-admin-forms` to dynamically change the value field based on the selected `data_type` - with minimal manual configuration.

## Key Configuration

### 1. INSTALLED_APPS Order (CRITICAL)
In [`config/settings.py`](../config/settings.py):

```python
INSTALLED_APPS = [
    "django_dynamic_admin_forms",  # MUST be before django.contrib.admin
    "django.contrib.admin",
    # ... rest of apps
]
```

### 2. URL Configuration (CRITICAL)
In [`config/urls.py`](../config/urls.py):

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("dynamic-admin-form/", include("django_dynamic_admin_forms.urls")),  # Add this line
    path("", include("core.urls")),
]
```

This registers the `/dynamic-admin-form/` endpoint that handles form reloading. Note the prefix must match what the JavaScript expects.

### 3. Admin Configuration
In [`core/admin/attribute_admin.py`](../core/admin/attribute_admin.py):

```python
class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    dynamic_fields = ['data_type']  # Fields to watch for changes
    
    def get_dynamic_fields(self, instance, data):
        # Returns modified fields based on data_type
        # ...
```

## How to Test

1. **Restart the Django server** (required after settings changes)
2. Navigate to Django admin → Attributes → Add Attribute
3. Change the `data_type` dropdown
4. The `value` field should automatically reload with the appropriate input type

## Expected Behavior

| Data Type | Value Field Type |
|-----------|------------------|
| Boolean | Checkbox |
| Integer | Number input (integers) |
| Float | Number input (decimals) |
| Date | Date picker |
| DateTime | DateTime picker |
| String/JSON | Textarea |

## Troubleshooting

### Form doesn't reload when data_type changes
- **Check**: Is `django_dynamic_admin_forms` before `django.contrib.admin` in INSTALLED_APPS?
- **Check**: Are the django_dynamic_admin_forms URLs included in `config/urls.py`?
- **Check**: Did you restart the server after making changes?
- **Check**: Is `dynamic_fields = ['data_type']` in the admin class?

### 404 error for `/dynamic-admin-form/` endpoint
- **Solution**: Add `path("dynamic-admin-form/", include("django_dynamic_admin_forms.urls"))` to `config/urls.py`
- **Check**: The URL prefix must be `dynamic-admin-form/` to match the JavaScript endpoint
- **Check**: Restart the Django server after adding the URL configuration

### Browser console errors
- **Check**: Are there any conflicting JavaScript files in `core/static/admin/js/`?
- **Solution**: Remove any custom JavaScript that might interfere

### Value doesn't save correctly for boolean
- **Check**: The `save_model` method should convert checkbox value to 'true'/'false' string
- **Check**: Already implemented in [`AttributeAdmin.save_model`](../core/admin/attribute_admin.py:147)

## Technical Note

While you requested "no JavaScript", `django-dynamic-admin-forms` does include its own minimal JavaScript to handle form reloading. However:

✅ You don't write any JavaScript code yourself
✅ You don't maintain any JavaScript files
✅ The JavaScript is minimal and provided by the package
✅ All form logic is in Python

This is the standard Django approach for dynamic forms without custom JavaScript development.