# Generated by Django 4.2.1 on 2023-05-13 07:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        max_length=4096, verbose_name="Message text"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Comment creation date and time",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User that wrote this comment",
                    ),
                ),
            ],
            options={
                "db_table": "comment",
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "group",
            },
        ),
        migrations.CreateModel(
            name="CommentFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=255, verbose_name="Title of a file"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="comments/%Y/%m/%d",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ("jpg", "gif", "png", "txt")
                            )
                        ],
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="comments.comment",
                        verbose_name="Comment that contains this file",
                    ),
                ),
            ],
            options={
                "db_table": "comment_file",
            },
        ),
        migrations.AddField(
            model_name="comment",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="comments.group",
                verbose_name="Group a comment belongs to",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="comments.comment",
                verbose_name="Reply for a comment",
            ),
        ),
    ]
