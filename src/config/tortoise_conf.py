from src.config import settings

TORTOISE_ORM = {
    "connections": {"default": "sqlite://blog.db"},
    "apps": {
        "models": {
            "models": settings.APPS_MODELS,
            "default_connection": "default",
        },
    },
}
