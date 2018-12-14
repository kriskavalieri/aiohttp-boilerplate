import base64
from pathlib import Path

import aiohttp_jinja2
import aiohttp_session
import jinja2
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .settings import Settings
from .views import index


THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent


def setup_routes(app):
    app.router.add_get('/', index, name='index')


async def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        name='task-checker',
        settings=settings
    )

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    aiohttp_jinja2.setup(app, loader=jinja2_loader)

    secret_key = base64.urlsafe_b64decode(settings.COOKIE_SECRET)
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))

    setup_routes(app)
    return app
