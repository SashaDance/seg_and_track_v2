import asyncio

from aiohttp import ClientSession, ClientResponse, ClientTimeout, ClientError
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode
from voice_assistant_extensions.logger.logger import CustomLogger

# Импортируем необходимые модули для трейсинга
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.propagate import inject


class HTTPClient:
    def __init__(
        self,
        logger: CustomLogger,
        service_name: str,
        timeout: int = 10,
        retries: int = 3,
        retry_delay: float = 1.0,
        jaeger_enable: bool = False,
        jaeger_host: str = "localhost",
        jaeger_port: int = 6831,
    ):
        self.logger = logger
        self.session = None
        self.timeout = ClientTimeout(total=timeout)
        self.retries = retries
        self.retry_delay = retry_delay

        self.jaeger_enable = jaeger_enable
        self.jaeger_host = jaeger_host
        self.jaeger_port = jaeger_port
        self.service_name = service_name

        # Настройка трассировки, если включена
        if self.jaeger_enable:
            self._setup_tracing()
        else:
            self.tracer = None

    def _setup_tracing(self):
        """Настройка провайдера трейсинга и экспортера Jaeger"""
        # Проверяем, существует ли уже TracerProvider
        if trace.get_tracer_provider() is None or not isinstance(trace.get_tracer_provider(), TracerProvider):
            # Настраиваем нового провайдера, если его нет
            resource = Resource.create({"service.name": self.service_name})
            provider = TracerProvider(resource=resource)

            # Устанавливаем нового провайдера
            trace.set_tracer_provider(provider)
        else:
            # Используем существующий провайдер
            provider = trace.get_tracer_provider()

        # Настраиваем экспортера Jaeger
        jaeger_exporter = JaegerExporter(
            collector_endpoint=f"http://{self.jaeger_host}:{self.jaeger_port}/api/traces", timeout=10
        )

        # Добавляем BatchSpanProcessor для отправки спанов в Jaeger
        span_processor = BatchSpanProcessor(jaeger_exporter)
        provider.add_span_processor(span_processor)

        # Получаем трейсер
        self.tracer = trace.get_tracer(__name__)

    async def open(self):
        self.session = ClientSession(timeout=self.timeout)

    async def _make_request(self, method: str, url: str, **kwargs) -> ClientResponse:
        headers = kwargs.get("headers", {})

        # Если Jaeger включен, начинаем спан и внедряем контекст в заголовки
        if self.jaeger_enable and self.tracer:
            with self.tracer.start_as_current_span(f"{method} {url}") as span:
                inject(headers)  # Внедряем контекст трассировки в заголовки
                kwargs["headers"] = headers
                return await self._attempt_request(method, url, span, **kwargs)
        else:
            # Если Jaeger не включен, просто выполняем запрос без спанов
            return await self._attempt_request(method, url, None, **kwargs)

    async def _attempt_request(self, method: str, url: str, span, **kwargs) -> ClientResponse:
        attempt = 0
        while attempt < self.retries:
            try:
                await self.logger.info(f"Outgoing request: {method} {url}", **kwargs)

                # Выполняем запрос
                response = await self.session.request(method, url, **kwargs)
                response_body = await response.json()

                await self.logger.info(
                    f"Response received from {method} {url}",
                    status_code=response.status,
                    headers=dict(response.headers),
                    **response_body,
                )

                # Если Jaeger включен, записываем информацию о статусе
                if span:
                    span.set_attribute("http.status_code", response.status)
                    span.set_attribute("http.url", url)
                    span.set_status(Status(status_code=StatusCode.OK))

                return response

            except (ClientError, asyncio.TimeoutError) as e:
                attempt += 1
                await self.logger.error(
                    f"Error occurred during {method} request to {url}: {str(e)}. Attempt {attempt}/{self.retries}"
                )

                # Если Jaeger включен, обновляем статус спана при ошибке
                if span:
                    span.set_status(Status(status_code=StatusCode.ERROR, description=f"Request failed: {e}"))
                    span.record_exception(e)

                # Пауза перед повторной попыткой
                if attempt < self.retries:
                    await asyncio.sleep(self.retry_delay)

        raise ClientError(f"Failed to {method} {url} after {self.retries} attempts.")

    async def get(self, url: str, **kwargs) -> ClientResponse:
        return await self._make_request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> ClientResponse:
        return await self._make_request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> ClientResponse:
        return await self._make_request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> ClientResponse:
        return await self._make_request("DELETE", url, **kwargs)

    async def close(self):
        if self.session:
            await self.session.close()
