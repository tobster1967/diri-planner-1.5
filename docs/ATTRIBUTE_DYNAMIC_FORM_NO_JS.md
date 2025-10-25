# Attribute Admin Dynamic Forms (No JavaScript)

## Overview

The Attribute admin interface uses `django-dynamic-admin-forms` to dynamically change form fields based on user selection **without requiring any JavaScript**. This is a pure server-side solution that provides a seamless user experience.

## How It Works

### 1. Django Dynamic Admin Forms Package

The implementation relies on the [`django-dynamic-admin-forms`](https://github.com/EmilStenstrom/django-dynamic-admin-forms) package which:

- Works entirely server-side (no JavaScript required)
- Automatically reloads the form when a monitored field changes
- Preserves all form data during reloads

### 2. Implementation in AttributeAdmin

The [`AttributeAdmin`](../core/admin/attribute_admin.py) class:

```python
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

@admin.register(Attribute)
class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # CRITICAL: Tell django-dynamic-admin-forms which field to watch
    dynamic_fields = ['data_type']
    
    # ... admin configuration ...
    
    def get_dynamic_fields(self, instance, data):
        """
        This method is called by django-dynamic-admin-forms whenever
        the form needs to be rebuilt (e.g., when data_type changes)
        """
        fields = {}
        
        # Get the current data_type value
        data_type = None
        if data and 'data_type' in data:
            data_type = data['data_type']
        elif instance and instance.pk:
            data_type = instance.data_type
        
        # Return different field definitions based on data_type
        if data_type == 'boolean':
            fields['value'] = forms.BooleanField(...)
        elif data_type == 'integer':
            fields['value'] = forms.CharField(widget=forms.NumberInput(...))
        # ... etc
        
        return fields
```

### 3. Data Type Specific Fields

When the user selects a `data_type`, the form automatically reloads with the appropriate field:

| Data Type | Field Type | Widget | Description |
|-----------|------------|--------|-------------|
| `boolean` | BooleanField | Checkbox | True/False checkbox |
| `integer` | CharField | NumberInput (step=1) | Integer input |
| `float` | CharField | NumberInput (step=any) | Decimal input |
| `date` | CharField | DateInput | Date picker |
| `datetime` | CharField | DateTimeInput | DateTime picker |
| `string` | CharField | Textarea | Multi-line text |
| `json` | CharField | Textarea | JSON content |

### 4. Form Submission and Saving

The [`save_model`](../core/admin/attribute_admin.py:134) method handles special conversion for boolean values:

```python
def save_model(self, request, obj, form, change):
    """Convert boolean checkbox value to string before saving."""
    if obj.data_type == 'boolean':
        value = form.cleaned_data.get('value')
        obj.value = 'true' if value else 'false'
    
    super().save_model(request, obj, form, change)
```

## User Experience

1. User selects a `data_type` from the dropdown
2. Form automatically reloads (full page refresh)
3. The `value` field changes to match the selected type
4. User enters the value using the appropriate input
5. Form is submitted and saved

**No JavaScript is involved** - this is all handled by the Django form system with automatic page reloads.

## Configuration Requirements

### 1. Package Installation

Ensure `django-dynamic-admin-forms` is in [`pyproject.toml`](../pyproject.toml):

```toml
dependencies = [
    "django-dynamic-admin-forms>=3.2.10",
    # ... other dependencies
]
```

### 2. INSTALLED_APPS

Add to [`config/settings.py`](../config/settings.py):

```python
INSTALLED_APPS = [
    # ...
    "django_dynamic_admin_forms",
    # ...
]
```

### 3. Admin Registration

The admin class must inherit from `DynamicModelAdminMixin` and specify which fields to watch:

```python
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # CRITICAL: Specify which field triggers dynamic behavior
    dynamic_fields = ['data_type']
    
    def get_dynamic_fields(self, instance, data):
        # Return the fields that should change based on dynamic_fields
        # ...
```

**Important**: The `dynamic_fields` attribute tells the library which fields to monitor for changes. When any of these fields change, the form is reloaded and `get_dynamic_fields` is called to rebuild the form.

## Benefits

✅ **No JavaScript**: Works in all browsers, even with JavaScript disabled
✅ **Simple**: Pure Django/Python implementation
✅ **Reliable**: No client-side state management
✅ **Maintainable**: Easy to understand and modify
✅ **Accessible**: Works with screen readers and assistive technologies

## Limitations

⚠️ **Full page reloads**: Each change triggers a complete form reload
⚠️ **Network dependent**: Requires server round-trip for each change

These limitations are acceptable trade-offs for the simplicity and reliability of a JavaScript-free solution.

## Testing

To test the dynamic form behavior:

1. Navigate to the Django admin
2. Go to Attributes → Add Attribute
3. Change the `data_type` dropdown
4. Observe the `value` field change to match the type
5. Enter a value and save

The form should work correctly without any JavaScript errors or console warnings.