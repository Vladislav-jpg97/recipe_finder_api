from enum import StrEnum

class SortEnum(StrEnum):
    rating = "rating"
    cooking_time = "cooking_time"
    calories = "calories"

class CuisineEnum(StrEnum):
    ITALIAN = "italian"
    THAI = "thai"
    GEORGIAN = "georgian"
    JAPANESE = "japanese"
    MEXICAN = "mexican"
    GREEK = "greek"
    FRENCH = "french"

