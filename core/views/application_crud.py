from django.shortcuts import redirect
from iommi import Page, html
from iommi.action import Action
from iommi.asset import Asset
from iommi.form import Field, Form
from iommi.table import Table

from core.models import Application

# Define local assets to override CDN dependencies
LOCAL_ASSETS = dict(
    jquery=Asset.js(attrs=dict(src="/static/js/jquery-3.4.1.min.js")),
    popper_js=Asset.js(attrs=dict(src="/static/js/popper.min.js")),
    css=Asset.css(attrs=dict(href="/static/css/bootstrap.min.css")),
    js=Asset.js(attrs=dict(src="/static/js/bootstrap.bundle.min.js")),
    icons=Asset.css(attrs=dict(href="/static/css/bootstrap-icons.css")),
)


class ApplicationCRUD:
    """
    iommi CRUD views for Application model with hierarchical tree support.
    """

    @staticmethod
    def list_view(request):
        """List view with table displaying all applications."""
        return Page(
            title="Applications",
            assets=LOCAL_ASSETS,
            parts__table=Table(
                auto__model=Application,
                page_size=50,
                columns__name=dict(
                    cell__url=lambda row, **_: f"/application/{row.pk}/edit/",
                ),
                columns__description=dict(),
                columns__parent__cell__format=lambda row, **_: row.parent.name if row.parent else "-",
                columns__level=dict(
                    attr="_depth",
                    display_name="Level",
                ),
                columns__slug=dict(
                    cell__url=lambda row, **_: f"/application/{row.pk}/edit/",
                ),
                actions__create=Action(
                    attrs__href="/application/create/",
                    display_name="Create New Application",
                ),
            ),
        )

    @staticmethod
    def create_view(request):
        """Create view for new applications."""

        def on_save(form, **_):
            if not form.is_valid():
                return
            form.instance.save()
            return redirect(f"/application/{form.instance.pk}/edit/")

        return Page(
            title="Create Application",
            assets=LOCAL_ASSETS,
            parts__form=Form(
                auto__model=Application,
                fields__name=Field.text(required=True),
                fields__description=Field.textarea(required=False),
                fields__parent=dict(
                    required=False,
                ),
                fields__slug=Field.text(required=True),
                actions__submit__post_handler=on_save,
                actions__cancel=Action(
                    display_name="Cancel",
                    attrs__href="/application/",
                ),
            ),
        )

    @staticmethod
    def edit_view(request, pk):
        """Edit view for existing applications."""
        try:
            instance = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            from django.http import Http404

            raise Http404("Application not found")

        def on_save(form, **_):
            if not form.is_valid():
                return
            form.instance.save()
            return redirect("/application/")

        def on_delete(form, **_):
            form.instance.delete()
            return redirect("/application/")

        return Page(
            title=f"Edit Application: {instance.name}",
            assets=LOCAL_ASSETS,
            parts__info=html.div(
                html.p(f"ID: {instance.id}"),
                html.p(f"Created: {instance.created_at}"),
                html.p(f"Updated: {instance.updated_at}"),
                html.p(f"Full Path: {instance.get_full_path()}"),
            ),
            parts__form=Form(
                auto__model=Application,
                auto__instance=instance,
                fields__name=Field.text(required=True),
                fields__description=Field.textarea(required=False),
                fields__parent=dict(
                    required=False,
                ),
                fields__slug=Field.text(required=True),
                fields__attributes=dict(
                    required=False,
                ),
                fields__organisations=dict(
                    required=False,
                ),
                actions__submit__post_handler=on_save,
                actions__delete=Action(
                    display_name="Delete",
                    post_handler=on_delete,
                    attrs__class__btn_danger=True,
                ),
                actions__cancel=Action(
                    display_name="Cancel",
                    attrs__href="/application/",
                ),
            ),
        )
