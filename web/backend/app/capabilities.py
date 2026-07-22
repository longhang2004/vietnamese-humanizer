from fastapi import HTTPException

from app.config import Settings, settings

_DISABLED_DETAIL = "Capability is disabled."
_ADMIN_KEY_PLACEHOLDER_MARKERS = (
    "changethis",
    "changeme",
    "placeholder",
    "replaceme",
    "replacewith",
    "youradminapikey",
)


def _has_value(value: str | None) -> bool:
    return bool(value and value.strip())


def validate_capability_settings(config: Settings | None = None) -> None:
    if config is None:
        config = settings

    if config.REWRITE_ENABLED and not _has_value(config.GEMINI_API_KEY):
        raise ValueError("GEMINI_API_KEY is required when REWRITE_ENABLED is true.")

    if config.ADMIN_API_ENABLED:
        admin_key = (config.ADMIN_API_KEY or "").strip()
        normalized_key = "".join(character for character in admin_key.lower() if character.isalnum())
        is_placeholder = any(
            marker in normalized_key for marker in _ADMIN_KEY_PLACEHOLDER_MARKERS
        )
        if len(admin_key) < 32 or is_placeholder:
            raise ValueError(
                "ADMIN_API_KEY must be non-placeholder and at least 32 characters "
                "when ADMIN_API_ENABLED is true."
            )


def require_rewrite_enabled() -> None:
    if not settings.REWRITE_ENABLED:
        raise HTTPException(status_code=503, detail=_DISABLED_DETAIL)


def require_contributions_enabled() -> None:
    if not settings.CONTRIBUTIONS_ENABLED:
        raise HTTPException(status_code=503, detail=_DISABLED_DETAIL)


def require_admin_enabled() -> None:
    if not settings.ADMIN_API_ENABLED:
        raise HTTPException(status_code=503, detail=_DISABLED_DETAIL)


def public_capabilities() -> dict[str, bool]:
    return {
        "rewrite": settings.REWRITE_ENABLED and _has_value(settings.GEMINI_API_KEY),
        "contributions": settings.CONTRIBUTIONS_ENABLED,
    }
