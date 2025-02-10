from contextlib import nullcontext  # Для создания заглушки контекстного менеджера
from typing import Union

from fastapi import WebSocket
from opentelemetry import trace

from ..models.responses import CommandResponse, EndPlanResponse
from ..models.types import CommandPlan
from ..logger.logger import CustomLogger


class WebSocketServer:
    def __init__(self, logger: CustomLogger, jaeger_enable: bool = False):
        self.websocket: Union[WebSocket, None] = None
        self.logger = logger
        self.tracer = trace.get_tracer(__name__) if jaeger_enable else None
        self.jaeger_enable = jaeger_enable

    def start_span(self, name: str):
        """Возвращает контекстный менеджер для span или заглушку, если Jaeger выключен."""
        return self.tracer.start_as_current_span(name) if self.jaeger_enable else nullcontext()

    async def connect(self, websocket: WebSocket):
        with self.start_span("WebSocket connect"):
            await websocket.accept()
            self.websocket = websocket
            await self.logger.info("Client connected")

    async def disconnect(self):
        with self.start_span("WebSocket disconnect"):
            if self.websocket:
                await self.websocket.close()
            self.websocket = None
            await self.logger.info("Client disconnected")

    async def receive_command(self):
        with self.start_span("Receive command"):
            request = await self.websocket.receive_json()
            data = CommandPlan.model_validate(request)
            await self.logger.info(f"Received plan: {data}")
            return data

    async def send_response(self, response: Union[CommandResponse, EndPlanResponse]):
        with self.start_span("Send response"):
            if self.websocket:
                await self.websocket.send_json(response.model_dump(mode="json", exclude_none=True))
                await self.logger.info(f"Response sent to AGS: {response.model_dump(exclude_none=True)}")
            else:
                await self.logger.error(
                    f"Client not connected. Command not sent\n{response.model_dump(mode='json', exclude_none=True)}"
                )
