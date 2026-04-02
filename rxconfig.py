import reflex as rx
from reflex.constants import LogLevel

config = rx.Config(
    app_name="ai_ecom",
    db_url=None,
    telemetry_enabled=False,
    use_bun=False,
    loglevel=LogLevel.DEBUG,
)