import uvicorn

from api.cfg import settings
from api.app import app

uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
