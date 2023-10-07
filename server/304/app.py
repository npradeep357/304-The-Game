"""
Fast API app
"""

import logging
import uuid
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .store import SESSIONS
from .game import Game


log = logging.getLogger(__name__)


class App:
    """
    App class
    """

    def __init__(
        self,
        host: str,
        port: int,
        version: str,
        loglevel: str = "info",
    ) -> None:
        log.info("Initializing app...")

        fast_app = FastAPI(docs_url="/", title="304", version=version)

        origins = ["*", "304"]

        fast_app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @fast_app.exception_handler(Exception)
        async def exception_handler(request, err):
            base_error_message = f"Failed to execute: {request.method}: {request.url}"
            log.error(base_error_message)
            return JSONResponse(
                status_code=500,
                content={
                    "message": f"{err}",
                },
            )

        @fast_app.get("/game", status_code=200)
        def get_new_game_session():
            sid = str(uuid.uuid4())
            SESSIONS[sid] = Game(sid)
            return {"id": sid}

        config = uvicorn.Config(fast_app, host=host, port=port, log_level=loglevel)
        server = uvicorn.Server(config)
        server.run()

        log.info("stopping 304 server...")
