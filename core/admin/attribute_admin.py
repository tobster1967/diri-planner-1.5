from django.contrib import admin
from django import forms
from core.models import Attribute
from django_dynamic_admin_forms.admin import DynamicModelAdminMixin


@admin.register(Attribute)
class AttributeAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    """
    Admin interface for Attribute model with tree hierarchy support
    and dynamic form based on data_type
    """
    # Tell django-dynamic-admin-forms to:
    # - Watch for changes on data_type (triggers reload)
    # - Update the value field when data_type changes
    dynamic_fields = ['data_type', 'value']
    
    list_display = ('indented_name', 'parent_name', 'slug', 'data_type', 'value', 'is_active', 'created_at')
    list_filter = ('data_type', 'is_active', 'parent', 'created_at')
    search_fields = ('name', 'slug', 'value', 'description')
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at', 'tree_info')
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Value', {
            'fields': ('data_type', 'value', 'description')
        }),
        ('Tree Information', {
            'fields': ('tree_info',),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',),
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    date_hierarchy = 'created_at'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Order parent field dropdown by tree path to show tree structure."""
        if db_field.name == "parent":
            kwargs['queryset'] = Attribute.objects.all().order_by('_path')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def indented_name(self, obj):
        """Display name with indentation based on tree depth."""
        indent = '—' * obj._depth
        return f"{indent} {obj.name}" if indent else obj.name
    indented_name.short_description = 'Name'
    
    def parent_name(self, obj):
        """Display the parent name."""
        if obj.parent:
            return obj.parent.name
        return "-"
    parent_name.short_description = 'Parent'
    parent_name.admin_order_field = 'parent__name'
    
    def tree_info(self, obj):
        """Display tree information for django-fast-treenode."""
        ancestors = obj.get_ancestors()
        path = ' > '.join([a.name for a in ancestors] + [obj.name])
        return f"Level: {obj.tn_depth}, Path: {path}, Left: {obj.tn_left}, Right: {obj.tn_right}"
    tree_info.short_description = 'Tree Info'
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Override get_form to dynamically modify the value field based on data_type.
        IMPORTANT: Must call super() to let DynamicModelAdminMixin initialize.
        """
        # Let the mixin set up dynamic_select_fields and dynamic_input_fields
        form = super().get_form(request, obj, change=change, **kwargs)
        
        # Get data_type from POST data (for dynamic updates) or from the object (for edit)
        data_type = None
        if request.method == 'POST' and 'data_type' in request.POST:
            data_type = request.POST.get('data_type')
        elif obj and obj.pk:
            data_type = obj.data_type
        else:
            data_type = 'string'
        
        # Modify the value field based on data_type using match/case
        match data_type:
            case 'boolean':
                # For boolean type, use a checkbox
                initial = self._get_boolean_value(obj) if obj and obj.pk else False
                form.base_fields['value'] = forms.BooleanField(
                    required=False,
                    initial=initial,
                    help_text='Check for True, uncheck for False'
                )
            case 'integer':
                # For integer type, use a number input
                form.base_fields['value'].widget = forms.NumberInput(
                    attrs={'step': '1', 'class': 'vIntegerField'}
                )
                form.base_fields['value'].help_text = 'Enter an integer value'
            case 'float':
                # For float type, use a number input with decimal support
                form.base_fields['value'].widget = forms.NumberInput(
                    attrs={'step': 'any', 'class': 'vFloatField'}
                )
                form.base_fields['value'].help_text = 'Enter a decimal value'
            case 'date':
                # For date type, use a date input
                form.base_fields['value'].widget = forms.DateInput(
                    attrs={'type': 'date', 'class': 'vDateField'}
                )
                form.base_fields['value'].help_text = 'Format: YYYY-MM-DD'
            case 'datetime':
                # For datetime type, use a datetime input
                form.base_fields['value'].widget = forms.DateTimeInput(
                    attrs={'type': 'datetime-local', 'class': 'vDateTimeField'}
                )
                form.base_fields['value'].help_text = 'Format: YYYY-MM-DD HH:MM:SS'
            case _:
                # Default: text area for string and json
                form.base_fields['value'].widget = forms.Textarea(
                    attrs={'rows': 3, 'class': 'vLargeTextField'}
                )
        
        return form
    
    def _get_boolean_value(self, instance):
        """Convert the stored string value to boolean for display."""
        if instance and instance.value:
            value = instance.value.lower()
            return value in ['true', '1', 'yes', 'on']
        return False
    
    def save_model(self, request, obj, form, change):
        """Convert boolean checkbox value to string before saving and update tree structure."""
        if obj.data_type == 'boolean':
            # Get the value from the form
            value = form.cleaned_data.get('value')
            # Convert boolean to string
            obj.value = 'true' if value else 'false'
        
        super().save_model(request, obj, form, change)
        
        # Rebuild tree structure after saving to ensure proper ordering
        # This is necessary when parent relationships change
        Attribute.update_tree()