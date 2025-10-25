# Attribute Dynamic Form

## Overview

The Attribute admin interface uses **django-dynamic-admin-forms** to automatically adapt the value field based on the selected `data_type`. This provides a better user experience with appropriate input widgets for each data type.

## Features

### Dynamic Field Types

The value field automatically changes based on the data_type:

| Data Type | Input Widget | Description |
|-----------|-------------|-------------|
| **boolean** | Checkbox | Simple checked/unchecked for true/false values |
| **integer** | Number input (step=1) | Integer values only |
| **float** | Number input (step=any) | Decimal values allowed |
| **date** | Date picker | Format: YYYY-MM-DD |
| **datetime** | DateTime picker | Format: YYYY-MM-DD HH:MM:SS |
| **string** | Text area | Regular text input |
| **json** | Text area | JSON formatted text |

### Boolean Handling

When `data_type` is set to **boolean**:
- The value field becomes a checkbox (after save/reload)
- Checked = `true`, Unchecked = `false`
- Values are stored as strings ("true" or "false") in the database
- Existing boolean values ("true", "1", "yes", "on") are recognized and displayed correctly

## Implementation

### Using django-dynamic-admin-forms

This feature is powered by the **django-dynamic-admin-forms** package, which provides dynamic form capabilities in Django admin.

**Package**: `django-dynamic-admin-forms==3.2.10`

### Admin Configuration ([`core/admin/attribute_admin.py`](../core/admin/attribute_admin.py))

The admin class extends `DynamicModelAdminMixin` and implements `get_dynamic_fields()`:

```python
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    def get_dynamic_fields(self, instance, data):
        """Dynamically change the value field based on data_type"""
        fields = {}
        
        # Get current data_type
        data_type = instance.data_type if instance and instance.pk else data.get('data_type', 'string')
        
        # Create appropriate field widget
        if data_type == 'boolean':
            fields['value'] = forms.BooleanField(
                required=False,
                initial=self._get_boolean_value(instance),
                help_text='Check for True, uncheck for False'
            )
        # ... other types
        
        return fields
```

### Settings Configuration

The package is added to `INSTALLED_APPS` in [`config/settings.py`](../config/settings.py):

```python
INSTALLED_APPS = [
    # ...
    "django_dynamic_admin_forms",
    # ...
]
```

## Usage

### Creating a Boolean Attribute

1. Navigate to Django Admin → Attributes → Add Attribute
2. Enter attribute name (e.g., "Is Active")
3. Select `data_type`: **boolean**
4. **Save the form** (the field will still be a text input initially)
5. After saving, open the attribute again
6. The value field is now a checkbox
7. Check or uncheck as needed
8. Save

### Converting Existing Attribute to Boolean

1. Open an existing attribute
2. Change `data_type` to **boolean**
3. Save the form
4. Reopen the attribute
5. The value field is now a checkbox showing the current value
6. Modify if needed and save

### Working with Other Types

**Integer Example:**
```
Name: Max Retries
Data Type: integer
Value: 3
```

**Float Example:**
```
Name: Discount Rate
Data Type: float
Value: 0.15
```

**Date Example:**
```
Name: Start Date
Data Type: date
Value: 2024-01-15
```

## Value Storage

All values are stored as strings in the database:

| Data Type | Example Input | Stored Value |
|-----------|--------------|--------------|
| boolean | ✓ (checked) | "true" |
| boolean | ☐ (unchecked) | "false" |
| integer | 42 | "42" |
| float | 3.14 | "3.14" |
| date | 2024-01-15 | "2024-01-15" |
| datetime | 2024-01-15 14:30 | "2024-01-15 14:30:00" |
| string | Hello | "Hello" |
| json | {"key": "value"} | "{\"key\": \"value\"}" |

## How It Works

### Dynamic Form Flow

1. **Initial Load**: Admin displays form with default field types
2. **Type Selection**: User selects or changes `data_type`
3. **Save**: Form is saved to the database
4. **Reload**: Page reloads with the attribute
5. **Dynamic Fields**: `get_dynamic_fields()` is called
6. **Widget Update**: Appropriate widget is rendered based on `data_type`

### Boolean Conversion in save_model

When saving a boolean attribute, the checkbox value is converted to string:

```python
def save_model(self, request, obj, form, change):
    if obj.data_type == 'boolean':
        value = form.cleaned_data.get('value')
        obj.value = 'true' if value else 'false'
    super().save_model(request, obj, form, change)
```

## Best Practices

1. **Choose Data Type First**: Always select the data_type before entering values
2. **Save Before Using Checkbox**: For boolean attributes, save once to enable the checkbox widget
3. **Consistent Boolean Values**: The system normalizes boolean strings to "true" or "false"
4. **Date Formats**: Always use ISO format (YYYY-MM-DD) for dates
5. **JSON Validation**: Ensure JSON is valid before saving

## Troubleshooting

### Checkbox Not Appearing

**Problem**: After changing to boolean type, still seeing text input

**Solution**: 
1. Save the form first
2. Close and reopen the attribute
3. The checkbox will now appear

### Dynamic Changes Not Working

**Problem**: Form doesn't update when changing data_type

**Solution**: 
1. Ensure `dynamic_admin_forms` is in `INSTALLED_APPS`
2. Clear browser cache
3. Check browser console for JavaScript errors
4. Verify the package is properly installed: `uv list | grep dynamic`

### Boolean Values Not Saving Correctly

**Problem**: Boolean values showing as text or empty

**Solution**: 
1. Check that `save_model()` method is converting values
2. Ensure the value field is returned from `get_dynamic_fields()`
3. Verify data_type is set to 'boolean' in the database

## Package Information

### django-dynamic-admin-forms

**Version**: 3.2.10  
**Documentation**: [PyPI Package](https://pypi.org/project/django-dynamic-admin-forms/)  
**GitHub**: [django-dynamic-admin-forms](https://github.com/voronind/django-dynamic-admin-forms)

### Key Features Used

- `DynamicModelAdminMixin`: Mixin class for admin
- `get_dynamic_fields()`: Method to define dynamic fields
- Automatic form rebuilding on field changes
- Support for all Django form field types

## Related Files

- [`core/admin/attribute_admin.py`](../core/admin/attribute_admin.py) - Admin configuration with dynamic forms
- [`core/models/attribute.py`](../core/models/attribute.py) - Attribute model definition
- [`config/settings.py`](../config/settings.py) - Django settings with installed apps

## Dependencies

```toml
[project]
dependencies = [
    "django>=5.2.7",
    "django-dynamic-admin-forms>=3.2.10",
    # ... other dependencies
]
```

## Future Enhancements

Potential improvements:
- Add color picker for color attributes
- Add file upload for file/image attributes
- Add rich text editor for HTML content
- Add multi-select for array/list types
- Add custom validation rules per data type
- Add inline help based on data_type