import json

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import traceback

from .logger import CustomLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: CustomLogger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        # Логирование запроса
        method = request.method
        url = str(request.url)
        client_ip = request.client.host
        headers = dict(request.headers)
        query_params = dict(request.query_params)

        try:
            body = await request.json()
        except json.JSONDecodeError:
            body = await request.body()
            if not body:
                body = None
        except Exception:
            body = None

        await self.logger.info(
            f"Request: {method} {url} from {client_ip}",
            query_params=query_params,
            body=body,
            headers=headers,
        )

        try:
            response = await call_next(request)

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Получаем тип содержимого ответа
            content_type = response.headers.get("Content-Type", "")

            # Если это текстовый ответ, декодируем его
            if "text" in content_type or "json" in content_type:
                try:
                    response_text = response_body.decode("utf-8")
                except UnicodeDecodeError:
                    response_text = "[unable to decode as UTF-8]"
            else:
                # Если это бинарные данные, просто указываем их наличие
                response_text = "[binary data]"

            await self.logger.info(
                f"Response: {response.status_code} {method} {url} to {client_ip}",
                headers=dict(response.headers),
                body=response_text,
            )

            # Возвращаем тело ответа в исходное состояние
            async def new_body_iterator():
                yield response_body

            response.body_iterator = new_body_iterator()
            return response
        except Exception as exc:
            error_message = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            await self.logger.error(f"Error occurred: {error_message}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
