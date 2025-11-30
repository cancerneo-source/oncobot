# Простейшая реализация модуля imghdr для Python 3.13+
# Нужна только для того, чтобы библиотеки, которые делают `import imghdr`,
# не падали с ошибкой.

import os
from typing import Optional, Union, BinaryIO


def _read_header(file: Union[str, os.PathLike, BinaryIO], length: int = 32) -> bytes:
    """Читаем первые `length` байт файла или потока."""
    if hasattr(file, "read"):
        # file-like объект
        pos = file.tell()
        data = file.read(length)
        file.seek(pos)
        return data
    else:
        # путь к файлу
        with open(file, "rb") as f:
            return f.read(length)


def what(file, h: Optional[bytes] = None) -> Optional[str]:
    """
    Упрощённый аналог imghdr.what(file, h)

    Определяем только самые частые форматы:
    - jpeg
    - png
    - gif

    Этого более чем достаточно для работы телеграм-бота.
    """
    if h is None:
        h = _read_header(file)

    if h.startswith(b"\xff\xd8"):
        return "jpeg"
    if h.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if h[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"

    return None
