from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Group, Comment, CommentFile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("author", "parent", "text", "created")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id",)
    search_fields = ("id",)
    inlines = [
        CommentInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "group", "parent", "created")
    list_display_links = ("id", "username", "email")
    list_filter = ("username", "email", "group", "parent")
    search_fields = ("id", "username", "email")
    readonly_fields = ("created",)
    save_on_top = True
    save_as = True


@admin.register(CommentFile)
class CommentFileAdmin(admin.ModelAdmin):
    list_display = ("id", "comment")
    list_display_links = ("id",)
    search_fields = ("id", "comment__id")
    save_on_top = True
    save_as = True


admin.site.site_title = _("Comments Administration")
admin.site.site_header = _("Comments Administration")
