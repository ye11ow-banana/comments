# Generated by Django 4.2.1 on 2023-05-13 12:35

import comments.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comments", "0002_alter_comment_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commentfile",
            name="title",
        ),
        migrations.AlterField(
            model_name="commentfile",
            name="file",
            field=models.FileField(
                upload_to="comments/%Y/%m/%d",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ("jpg", "gif", "png", "txt")
                    ),
                    comments.validators.MaxDimensionsValidator(
                        max_height=240, max_width=320
                    ),
                    comments.validators.MaxFileSizeValidator(max_size=100),
                ],
            ),
        ),
    ]
