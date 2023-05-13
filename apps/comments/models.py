from django_bleach.models import BleachField

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL
from django.core.validators import FileExtensionValidator
from django.db import models

from .validators import MaxDimensionsValidator, MaxFileSizeValidator


class Group(models.Model):
    """
    Represents a group of comments.

    Can be instead of video, article, post etc.
    """

    class Meta:
        db_table = "group"

    def __str__(self) -> str:
        return f"Group: {self.pk}"


class Comment(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User that wrote this comment"),
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Group a comment belongs to"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        verbose_name=_("Reply for a comment"),
        null=True,
        blank=True,
    )
    username = models.CharField(
        _("Username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        blank=True,
    )
    email = models.EmailField(_("Email address"), blank=True)
    text = BleachField(_("Message text"), max_length=4096)
    created = models.DateTimeField(
        _("Comment creation date and time"),
        auto_now_add=True,
        blank=True,
    )

    class Meta:
        db_table = "comment"

    def __str__(self) -> str:
        return f"Comment: {self.pk}"

    def save(self, *args, **kwargs) -> None:
        if self.author is not None:
            self.username = self.author.username
            self.email = self.author.email
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.author is None and (not self.username or not self.email):
            raise ValidationError(
                _(
                    "Either `author` field or (`username` "
                    "and `email`) fields must be defined"
                )
            )
        if self.parent is not None:
            parent_id = self.parent.id
            if parent_id not in self.group.comments.values_list(
                "id", flat=True
            ):
                raise ValidationError(
                    _("Comment %(value)s is not a group comment"),
                    params={"value": parent_id},
                )


class CommentFile(models.Model):
    """
    File that is related to a comment.
    """

    file = models.FileField(
        upload_to="comments/%Y/%m/%d",
        validators=[
            FileExtensionValidator(("jpg", "jpeg", "gif", "png", "txt")),
            MaxDimensionsValidator(max_width=320, max_height=240),
            MaxFileSizeValidator(max_size=100),
        ],
    )
    comment = models.OneToOneField(
        Comment,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("Comment that contains this file"),
    )

    class Meta:
        db_table = "comment_file"

    def __str__(self) -> str:
        return f"File: {self.pk}"
