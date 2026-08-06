class CacheKeys:
    @staticmethod
    def recipe_list(**kwargs) -> str:
        params = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None)
        return f"recipe:list:{params}" if params else "recipes:list"

    @staticmethod
    def recipe_detail(recipe_id: int) -> str:
        return f"recipe:detail:{recipe_id}"

    @staticmethod
    def cuisine_list() -> str:
        return f"cuisines:list"
