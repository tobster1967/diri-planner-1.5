# Migration from django-tree-queries to django-fast-treenode

## Overview

The Attribute model has been migrated from `django-tree-queries` to `django-fast-treenode` for better performance and built-in admin integration.

## Changes Made

### 1. Package Update

**[`pyproject.toml`](../pyproject.toml)**
```toml
# Before
"django-tree-queries>=0.19.0",

# After  
"django-fast-treenode>=1.0.0",
```

### 2. Settings Update

**[`config/settings.py`](../config/settings.py)**
```python
INSTALLED_APPS = [
    # ...
    "treenode",  # Added django-fast-treenode (package name: django-fast-treenode, module: treenode)
    # ...
]
```

### 3. Model Changes

**[`core/models/attribute.py`](../core/models/attribute.py)**

#### Before (django-tree-queries)
```python
from tree_queries.models import TreeNode

class Attribute(TreeNode, BaseModel):
    parent = models.ForeignKey('self', ...)
    # Tree methods: descendants(), ancestors(), etc.
```

#### After (django-fast-treenode)
```python
from treenode.models import TreeNodeModel

class Attribute(TreeNodeModel, BaseModel):
    # TreeNodeModel adds these fields automatically:
    # - tn_parent: ForeignKey to self (parent node)
    # - tn_depth: Integer (depth in tree, 0 for root)
    # - tn_left: Integer (MPTT left value)
    # - tn_right: Integer (MPTT right value)
    # - tn_priority: Integer (sibling ordering)
```

**Key Differences:**
- No need to define `parent` field manually - TreeNodeModel adds `tn_parent`
- Uses MPTT (Modified Preorder Tree Traversal) for efficient queries
- Tree fields are prefixed with `tn_` to avoid conflicts
- Provides `tn_priority` for explicit sibling ordering

### 4. Admin Changes

**[`core/admin/attribute_admin.py`](../core/admin/attribute_admin.py)**

#### Updated Methods
```python
def indented_name(self, obj):
    """Uses tn_depth instead of tree_depth"""
    indent = '—' * obj.tn_depth
    return f"{indent} {obj.name}" if indent else obj.name

def tree_info(self, obj):
    """Uses get_ancestors() from TreeNodeModel"""
    ancestors = obj.get_ancestors()
    path = ' > '.join([a.name for a in ancestors] + [obj.name])
    return f"Level: {obj.tn_depth}, Path: {path}"
```

#### Removed
- `get_queryset()` override - no longer needed
- `autocomplete_fields` for parent - TreeNodeModel handles this
- Custom parent field in fieldsets

### 5. Database Migration

**Complete reset was performed:**
1. Deleted all old migrations
2. Dropped and recreated database  
3. Created fresh migrations
4. Applied all migrations

## API Comparison

### Field Access

| django-tree-queries | django-fast-treenode |
|---------------------|---------------------|
| `obj.parent` | `obj.tn_parent` |
| `obj.tree_depth` | `obj.tn_depth` |
| N/A | `obj.tn_left` |
| N/A | `obj.tn_right` |
| N/A | `obj.tn_priority` |

### Tree Methods

| Method | django-tree-queries | django-fast-treenode |
|--------|---------------------|---------------------|
| Get ancestors | `obj.ancestors()` | `obj.get_ancestors()` |
| Get descendants | `obj.descendants()` | `obj.get_descendants()` |
| Get children | `obj.children.all()` | `obj.get_children()` |
| Get siblings | N/A | `obj.get_siblings()` |
| Get root | N/A | `obj.get_root()` |
| Is root | `not obj.parent` | `obj.is_root()` |
| Is leaf | `not obj.children.exists()` | `obj.is_leaf()` |

### QuerySet Methods

**django-tree-queries:**
```python
# Required with_tree_fields() for depth/path
Attribute.objects.with_tree_fields()
```

**django-fast-treenode:**
```python
# Tree fields always available
Attribute.objects.all()

# Additional methods
Attribute.objects.get_roots()
Attribute.objects.get_tree(obj)
```

## Migration Benefits

✅ **Better Performance**
- MPTT provides O(1) subtree queries
- No need for recursive CTEs

✅ **Built-in Admin Support**
- Tree display in admin
- Drag-and-drop ordering (with additional setup)

✅ **More Features**
- Sibling ordering with `tn_priority`
- More tree navigation methods
- Better queryset filtering

✅ **Active Development**
- More recent updates
- Better Django 5.x support

## Backward Compatibility

### Breaking Changes

1. **Field names changed:**
   - `parent` → `tn_parent`
   - `tree_depth` → `tn_depth`

2. **Method names changed:**
   - `ancestors()` → `get_ancestors()`
   - `descendants()` → `get_descendants()`
   - `children.all()` → `get_children()`

3. **No automatic queryset annotation:**
   - Old: `qs.with_tree_fields()` required
   - New: Fields always available

### Migration Path for Existing Code

If you have existing code using the old API:

```python
# Before
for attr in Attribute.objects.with_tree_fields():
    depth = attr.tree_depth
    parent = attr.parent
    kids = attr.children.all()

# After  
for attr in Attribute.objects.all():
    depth = attr.tn_depth
    parent = attr.tn_parent
    kids = attr.get_children()
```

## Testing

### Manual Testing Steps

1. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Test in Admin:**
   - Go to `/admin/core/attribute/`
   - Create root attribute
   - Create child attributes
   - Verify tree display with indentation
   - Test tree navigation

4. **Test Tree Methods:**
   ```python
   from core.models import Attribute
   
   # Create tree
   root = Attribute.objects.create(name="Root")
   child1 = Attribute.objects.create(name="Child 1", tn_parent=root)
   child2 = Attribute.objects.create(name="Child 2", tn_parent=root)
   grandchild = Attribute.objects.create(name="Grandchild", tn_parent=child1)
   
   # Test methods
   assert root.tn_depth == 0
   assert child1.tn_depth == 1
   assert grandchild.tn_depth == 2
   
   assert list(root.get_children()) == [child1, child2]
   assert list(grandchild.get_ancestors()) == [root, child1]
   assert root.is_root()
   assert grandchild.is_leaf()
   ```

## Resources

- [django-fast-treenode Documentation](https://github.com/fabiocaccamo/django-fast-treenode)
- [MPPT Explanation](https://en.wikipedia.org/wiki/Tree_traversal#Pre-order_(NLR))
- [Package on PyPI](https://pypi.org/project/django-fast-treenode/)

## Notes

- **Dynamic forms still work:** The value field dynamic behavior is unchanged
- **Module name vs package name:** Package is `django-fast-treenode`, but import from `treenode`
- **Database reset required:** Due to incompatible tree implementations
- **All old data lost:** This was acceptable as noted in the discovery phase