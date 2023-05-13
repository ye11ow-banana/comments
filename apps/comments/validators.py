from typing import TypeAlias

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.db.models.fields.files import FieldFile
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

kilobyte: TypeAlias = int


@deconstructible
class MaxDimensionsValidator:
    def __init__(self, *, max_width: int, max_height: int) -> None:
        self._max_width = max_width
        self._max_height = max_height

    def __call__(self, picture: FieldFile) -> None:
        w, h = get_image_dimensions(picture)
        if w is None or h is None:
            return
        if w > self._max_width or h > self._max_height:
            raise ValidationError(
                _("Maximum dimension is %(w)sx%(h)s"),
                params={"w": self._max_width, "h": self._max_height},
            )


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, *, max_size: kilobyte) -> None:
        self._max_size = max_size

    def __call__(self, picture: FieldFile) -> None:
        if picture.size > self._max_size * 1000:
            raise ValidationError(
                _("Maximum size is %(size)s KB"),
                params={"size": self._max_size},
            )
