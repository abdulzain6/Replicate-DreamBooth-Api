from ddtrace import patch_all
from ddtrace.contrib.asgi import TraceMiddleware
from fastapi.middleware import Middleware



patch_all()
dd_middleware = Middleware(TraceMiddleware)
