import re

from transliterate import translit


def _transliterate(text: str) -> str:
    try:
        return translit(text, reversed=True)
    except Exception:
        return text


class SlugGenerate:
    @staticmethod
    def generate(name: str) -> str:
        text = _transliterate(name)
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r"\s+","-",text)
        text = re.sub(r"^-+|-+$","",text)
        return text

    @staticmethod
    def add_suffix(slug: str, counter: int) -> str:
        return f"{slug}-{counter}"
