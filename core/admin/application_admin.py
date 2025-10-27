from django.contrib import admin

from core.models import Application, Attribute, Organisation


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for Application model with tree hierarchy support
    """

    list_display = ("indented_name", "parent_name", "slug", "created_at", "updated_at")
    list_filter = ("parent", "created_at")
    search_fields = ("name", "slug", "description")
    readonly_fields = ("id", "slug", "created_at", "updated_at", "tree_info")
    list_per_page = 50
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "parent", "description")}),
        (
            "Tree Information",
            {
                "fields": ("tree_info",),
                "classes": ("collapse",),
            },
        ),
        (
            "Attributes",
            {
                "fields": ("attributes",),
                "description": "Select attributes to associate with this application. Attributes are shown in tree structure with indentation.",
            },
        ),
        (
            "Organisations",
            {
                "fields": ("organisations",),
                "description": "Select organisations to associate with this application. Organisations are shown in tree structure with indentation.",
            },
        ),
        (
            "Additional Properties",
            {
                "fields": ("properties",),
                "classes": ("collapse",),
            },
        ),
        (
            "System Information",
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    filter_horizontal = ("attributes", "organisations")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Order parent field dropdown by tree path to show tree structure."""
        if db_field.name == "parent":
            kwargs["queryset"] = Application.objects.all().order_by("_path")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Customize the display of M2M widgets to show tree structure.
        Orders by _path field which maintains tree hierarchy.
        """
        if db_field.name == "attributes":
            # Order by _path to get proper tree order (parent before children)
            kwargs["queryset"] = Attribute.objects.all().order_by("_path")
        elif db_field.name == "organisations":
            # Order by _path to get proper tree order (parent before children)
            kwargs["queryset"] = Organisation.objects.all().order_by("_path")

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def indented_name(self, obj):
        """Display name with indentation based on tree depth."""
        indent = "—" * obj._depth
        return f"{indent} {obj.name}" if indent else obj.name

    indented_name.short_description = "Name"

    def parent_name(self, obj):
        """Display the parent name."""
        if obj.parent:
            return obj.parent.name
        return "-"

    parent_name.short_description = "Parent"
    parent_name.admin_order_field = "parent__name"

    def tree_info(self, obj):
        """Display tree information for django-fast-treenode."""
        ancestors = obj.get_ancestors()
        path = " > ".join([a.name for a in ancestors] + [obj.name])
        return f"Level: {obj._depth}, Path: {path}, Left: {obj._left}, Right: {obj._right}"

    tree_info.short_description = "Tree Info"

    def get_form(self, request, obj=None, **kwargs):
        """
        Override to provide additional context for tree display
        """
        form = super().get_form(request, obj, **kwargs)

        # Add help text about tree structure for attributes
        if "attributes" in form.base_fields:
            form.base_fields["attributes"].help_text = (
                "Select attributes to associate with this application. "
                'Attributes are shown in tree structure with "—" indicating child levels.'
            )

        # Add help text about tree structure for organisations
        if "organisations" in form.base_fields:
            form.base_fields["organisations"].help_text = (
                "Select organisations to associate with this application. "
                'Organisations are shown in tree structure with "—" indicating child levels.'
            )

        return form

    def save_model(self, request, obj, form, change):
        """Save the model and update tree structure."""
        super().save_model(request, obj, form, change)

        # Rebuild tree structure after saving to ensure proper ordering
        # This is necessary when parent relationships change
        Application.update_tree()
