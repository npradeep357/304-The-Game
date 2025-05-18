"""
Fast API app
"""

import logging
import uuid
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Request
from starlette.staticfiles import StaticFiles
from fastapi.responses import JSONResponse



log = logging.getLogger(__name__)



def add_exception_handlers(fast_app):
    """adding exception handlers"""

    @app.exception_handler(Error)
    async def error_handler(
        request: Request,
        exc: Error,
    ) -> JSONResponse:
        if len(exc.args) > 0:
            return JSONResponse(
                status_code=400,
                content={"message": exc.args[0]},
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"message": "Internal server error. Check logs"},
            )


def add_routes(fast_app):

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
    def get_game_session(request):
        user_id = request.headers["X-User-ID"]
        if user_id not in SESSIONS:
            sid = str(uuid.uuid4())
            SESSIONS[user_id] = Game(sid)
            return {"id": sid}
        return {"id": SESSIONS[user_id].id}

    @fast_app.websocket("/ws/{session_id}")
    async def websocket_endpoint(websocket: WebSocket, session_id: str):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                print(f"Received message: {data}")
                await websocket.send_text(f"Message received: {data}")
        except WebSocketDisconnect:
            print("Client disconnected")

    @fast_app.get("/", response_class=HTMLResponse)
    async def read_root():
        with open("client/index.html") as f:
            return HTMLResponse(content=f.read())




def get_app(config: dict) -> FastAPI:
    """Returns FastAPI app instance"""
    log.info("starting server API...")
    log.debug(f"config - {str(config)}")

    prefix = config.get("basepath", "/v1")
    docs_url = config.get("docs_url", "/swagger-ui/index.html")
    openapi_url = config.get("openapi_url", "/apidocs")
    version = config.get("version", "SNAPSHOT")

    origins = ["*"]

    fast_app = FastAPI(
        title="304",
        version=version,
        root_path=f"{prefix}",
        docs_url=docs_url,
        openapi_url=openapi_url,
    )

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(fast_app=fast_app)

    fast_app.mount("/client", StaticFiles(directory="client"), name="client")

    add_routes(fast_app=fast_app)

    return fast_app

