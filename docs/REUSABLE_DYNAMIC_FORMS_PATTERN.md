# Reusable Dynamic Forms Pattern

## Overview

The `django-dynamic-admin-forms` package provides a reusable pattern for creating dynamic forms in Django admin. You simply specify which fields should trigger form reloads, and the package handles the rest.

## How to Mark Fields for Dynamic Behavior

### Step 1: Add the Mixin
```python
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

class YourModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # Your admin configuration
```

### Step 2: Register Dynamic Fields
```python
class YourModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # List the field names that should trigger form reloads when changed
    dynamic_fields = ['field1', 'field2', 'field3']
```

### Step 3: Override get_form() to Modify Fields
```python
def get_form(self, request, obj=None, change=False, **kwargs):
    form = super().get_form(request, obj, change=change, **kwargs)
    
    # Read values from POST (for dynamic updates) or object (for editing)
    if request.method == 'POST':
        trigger_value = request.POST.get('field1')
    elif obj:
        trigger_value = obj.field1
    else:
        trigger_value = 'default'
    
    # Modify form fields based on the trigger value
    match trigger_value:
        case 'option1':
            form.base_fields['dependent_field'].widget = ...
        case 'option2':
            form.base_fields['dependent_field'].widget = ...
    
    return form
```

## Complete Example: Attribute Admin

Here's how the Attribute admin implements this pattern:

```python
@admin.register(Attribute)
class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # Mark data_type as the trigger field
    dynamic_fields = ['data_type']
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change=change, **kwargs)
        
        # Get the trigger field value
        data_type = None
        if request.method == 'POST' and 'data_type' in request.POST:
            data_type = request.POST.get('data_type')
        elif obj and obj.pk:
            data_type = obj.data_type
        
        if not data_type:
            data_type = 'string'
        
        # Modify the dependent field (value) based on data_type
        match data_type:
            case 'boolean':
                form.base_fields['value'] = forms.BooleanField(...)
            case 'integer':
                form.base_fields['value'].widget = forms.NumberInput(...)
            # ... etc
        
        return form
```

## How It Works Under the Hood

1. **JavaScript monitors** fields listed in `dynamic_fields`
2. **On change**, JavaScript:
   - Serializes the entire form
   - POSTs to `/dynamic-admin-form/` endpoint
   - Receives updated HTML for dependent fields
   - Replaces the old HTML with new HTML
3. **Server-side** Django:
   - Receives POST with all form data
   - Calls `get_form()` with POST data in request
   - Your code modifies `form.base_fields` based on POST values
   - Returns rendered HTML for modified fields

## Extending to Other Admin Forms

### Example: Product Admin with Category-Based Fields

```python
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin

@admin.register(Product)
class ProductAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # Trigger reload when category changes
    dynamic_fields = ['category']
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change=change, **kwargs)
        
        # Get category from POST or object
        category = None
        if request.method == 'POST':
            category = request.POST.get('category')
        elif obj:
            category = obj.category
        
        # Show different fields based on category
        match category:
            case 'electronics':
                form.base_fields['warranty_period'].widget = forms.NumberInput()
                form.base_fields['voltage'].widget = forms.TextInput()
            case 'clothing':
                form.base_fields['size'].widget = forms.Select(
                    choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
                )
                form.base_fields['material'].widget = forms.TextInput()
            case _:
                # Default fields
                pass
        
        return form
```

### Example: Multi-Field Dependencies

```python
@admin.register(Order)
class OrderAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    # Multiple fields can trigger reloads
    dynamic_fields = ['country', 'shipping_method']
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change=change, **kwargs)
        
        # Get values
        country = request.POST.get('country') if request.POST else (obj.country if obj else None)
        shipping = request.POST.get('shipping_method') if request.POST else (obj.shipping_method if obj else None)
        
        # Modify fields based on both values
        if country == 'US':
            form.base_fields['state'].widget = forms.Select(choices=US_STATES)
        elif country == 'CA':
            form.base_fields['state'].widget = forms.Select(choices=CA_PROVINCES)
        
        if shipping == 'express':
            form.base_fields['delivery_date'].help_text = '2-3 business days'
        elif shipping == 'standard':
            form.base_fields['delivery_date'].help_text = '5-7 business days'
        
        return form
```

## Benefits

✅ **Declarative**: Just list field names in `dynamic_fields`
✅ **Reusable**: Same pattern works for any model
✅ **Maintainable**: All logic in Python, minimal JavaScript
✅ **Flexible**: Can depend on multiple fields
✅ **Type-safe**: Full Python type checking

## Requirements

1. **Package installed**: `django-dynamic-admin-forms>=3.2.10`
2. **App order**: `django_dynamic_admin_forms` before `django.contrib.admin` in INSTALLED_APPS
3. **URLs configured**: `path("dynamic-admin-form/", include("django_dynamic_admin_forms.urls"))`

## Best Practices

1. **Keep it simple**: Only mark fields that truly need dynamic behavior
2. **Performance**: The form is regenerated on each change, so keep logic fast
3. **User experience**: Too many dynamic fields can make forms feel sluggish
4. **Validation**: Remember to handle validation for dynamically changed fields
5. **Testing**: Test all combinations of trigger field values

## Common Patterns

### Pattern 1: Show/Hide Fields
```python
match trigger_value:
    case 'show':
        form.base_fields['hidden_field'].widget = forms.TextInput()
    case 'hide':
        form.base_fields['hidden_field'].widget = forms.HiddenInput()
```

### Pattern 2: Change Widget Type
```python
match data_type:
    case 'text':
        form.base_fields['value'].widget = forms.Textarea()
    case 'number':
        form.base_fields['value'].widget = forms.NumberInput()
```

### Pattern 3: Dynamic Choices
```python
if category == 'electronics':
    form.base_fields['subcategory'].widget.choices = ELECTRONICS_CHOICES
elif category == 'clothing':
    form.base_fields['subcategory'].widget.choices = CLOTHING_CHOICES
```

### Pattern 4: Conditional Validation
```python
match field_type:
    case 'required':
        form.base_fields['dependent_field'].required = True
    case 'optional':
        form.base_fields['dependent_field'].required = False
```

## Troubleshooting

**Form doesn't reload:**
- Check `dynamic_fields` includes the trigger field
- Verify URLs are configured correctly
- Check browser console for JavaScript errors

**Wrong field state after reload:**
- Ensure you're reading from `request.POST` for dynamic updates
- Check the field name matches exactly
- Verify POST data contains the field

**Performance issues:**
- Limit number of dynamic fields
- Optimize `get_form()` logic
- Consider caching expensive operations