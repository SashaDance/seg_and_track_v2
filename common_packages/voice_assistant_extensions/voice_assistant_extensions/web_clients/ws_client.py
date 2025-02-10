import asyncio
import websockets
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from websockets.exceptions import InvalidURI, InvalidHandshake, WebSocketException

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import inject
from opentelemetry.trace import StatusCode, Status
from opentelemetry.sdk.resources import Resource

from ..models.responses import CommandResponse
from ..models.types import CommandPlan, PlanType
from ..logger.logger import CustomLogger


class WebSocketClient:
    def __init__(
        self,
        robot_entry: str,
        logger: CustomLogger,
        service_name: str,
        jaeger_enable: bool = False,
        jaeger_host: str = "localhost",
        jaeger_port: int = 6831,
    ):
        self.robot_entry = robot_entry
        self.logger = logger
        self.websocket = None
        self.listen_task = None
        self.response_callback = None
        self.reconnect_delay = 3  # Задержка перед повторным подключением в секундах
        self.connect_timeout = 3  # Тайм-аут для подключения в секундах
        self.jaeger_enable = jaeger_enable
        self.service_name = service_name
        self.jaeger_host = jaeger_host
        self.jaeger_port = jaeger_port

        # Настройка трейсинга, если включен Jaeger
        if self.jaeger_enable:
            self._setup_tracing()
        else:
            self.tracer = None

    def _setup_tracing(self):
        """Настройка провайдера трейсинга и экспортера Jaeger"""
        if trace.get_tracer_provider() is None or not isinstance(trace.get_tracer_provider(), TracerProvider):
            # Настраиваем нового провайдера, если его нет
            resource = Resource.create({"service.name": self.service_name})
            provider = TracerProvider(resource=resource)

            # Устанавливаем нового провайдера
            trace.set_tracer_provider(provider)
        else:
            # Используем существующий провайдер
            provider = trace.get_tracer_provider()

        jaeger_exporter = JaegerExporter(
            collector_endpoint=f"http://{self.jaeger_host}:{self.jaeger_port}/api/traces", timeout=10
        )

        # Добавляем BatchSpanProcessor для отправки спанов в Jaeger
        span_processor = BatchSpanProcessor(jaeger_exporter)
        provider.add_span_processor(span_processor)

        # Получаем трейсер
        self.tracer = trace.get_tracer(__name__)

    def set_response_callback(self, callback):
        self.response_callback = callback

    async def connect(self):
        while True:
            try:
                await self.logger.info("Attempting to connect to WebSocket...")
                # Начинаем новый спан для подключения, если Jaeger включен
                if self.jaeger_enable and self.tracer:
                    with self.tracer.start_as_current_span("WebSocket Connect") as span:
                        inject_headers = {}  # Заголовки для контекста
                        inject(inject_headers)  # Внедряем контекст Jaeger в заголовки
                        self.websocket = await websockets.connect(self.robot_entry)
                        span.set_status(Status(status_code=StatusCode.OK))
                        await self.logger.info("WebSocket connection established.")
                else:
                    # Если Jaeger не включен, просто выполняем подключение
                    self.websocket = await websockets.connect(self.robot_entry)
                    await self.logger.info("WebSocket connection established.")
            except (
                BaseException,
                asyncio.TimeoutError,
                ConnectionRefusedError,
                InvalidURI,
                InvalidHandshake,
                WebSocketException,
                TimeoutError,
            ) as e:
                if self.jaeger_enable and self.tracer:
                    with self.tracer.start_as_current_span("WebSocket connection failed") as span:
                        span.set_status(Status(status_code=StatusCode.ERROR, description=str(e)))
                        span.record_exception(e)
                await self.logger.error(
                    f"WebSocket connection failed: {e}. Retrying in {self.reconnect_delay} seconds..."
                )
                await asyncio.sleep(self.reconnect_delay)
            else:
                self.listen_task = asyncio.create_task(self.listen_for_responses())
                break  # Выйти из цикла при успешном подключении

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            await self.logger.info("WebSocket connection closed.")

    async def send_plan(self, plan: PlanType):
        if not self.websocket:
            raise Exception("WebSocket connection is not established. Call connect() first.")

        plan_model = CommandPlan(plan=plan)
        json_plan = plan_model.model_dump_json(exclude_none=True)

        # Создаем спан для отправки данных, если Jaeger включен
        if self.jaeger_enable and self.tracer:
            with self.tracer.start_as_current_span("WebSocket Send Plan") as span:
                span.set_attribute("websocket.message", json_plan)
                inject_headers = {}
                inject(inject_headers)  # Внедряем контекст в заголовки
                await self.websocket.send(json_plan)
                await self.logger.info("Sent plan:", plan=json_plan)
        else:
            await self.websocket.send(json_plan)
            await self.logger.info("Sent plan:", plan=json_plan)

    async def listen_for_responses(self):
        try:
            while True:
                response_data = await self.websocket.recv()
                response = CommandResponse.model_validate_json(response_data)

                # Создаем спан для получения сообщения, если Jaeger включен
                if self.jaeger_enable and self.tracer:
                    with self.tracer.start_as_current_span("WebSocket Receive Response") as span:
                        span.set_attribute("websocket.response", response_data)
                        if self.response_callback:
                            await self.response_callback(response)
                else:
                    if self.response_callback:
                        await self.response_callback(response)
        except websockets.ConnectionClosed:
            await self.logger.warning("WebSocket connection closed. Attempting to reconnect...")
            await self.reconnect()
        except Exception as e:
            await self.logger.error(f"Error in WebSocket connection: {e}")
            await self.reconnect()

    async def reconnect(self):
        await self.disconnect()
        await self.logger.info("Starting reconnection process...")
        await self.connect()
