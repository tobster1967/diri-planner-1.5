from django.contrib import admin

from core.models import Organisation


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """
    Admin interface for Organisation model with tree hierarchy support
    """

    list_display = ("indented_name", "parent_name", "slug", "code", "is_active", "created_at")
    list_filter = ("is_active", "parent", "created_at")
    search_fields = ("name", "slug", "code", "description", "email")
    readonly_fields = ("id", "slug", "created_at", "updated_at", "tree_info")
    list_per_page = 50
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "code", "parent", "description")}),
        (
            "Contact Information",
            {
                "fields": ("email", "phone", "address", "website"),
            },
        ),
        (
            "Tree Information",
            {
                "fields": ("tree_info",),
                "classes": ("collapse",),
            },
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Metadata",
            {
                "fields": ("metadata",),
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Order parent field dropdown by tree path to show tree structure."""
        if db_field.name == "parent":
            kwargs["queryset"] = Organisation.objects.all().order_by("_path")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    def save_model(self, request, obj, form, change):
        """Save the model and update tree structure."""
        super().save_model(request, obj, form, change)

        # Rebuild tree structure after saving to ensure proper ordering
        # This is necessary when parent relationships change
        Organisation.update_tree()
