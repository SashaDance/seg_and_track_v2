from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format
from fastapi import FastAPI


def add_jaeger_tracing(app: FastAPI, service_name: str, jaeger_host: str, jaeger_port: int) -> FastAPI:
    # Проверяем, установлен ли уже TracerProvider
    if trace.get_tracer_provider() is None or not isinstance(trace.get_tracer_provider(), TracerProvider):
        tracer_provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
        trace.set_tracer_provider(tracer_provider)
    else:
        # Если TracerProvider уже существует, просто получаем его
        tracer_provider = trace.get_tracer_provider()

    jaeger_exporter = JaegerExporter(collector_endpoint=f"http://{jaeger_host}:{jaeger_port}/api/traces", timeout=10)

    # Добавляем BatchSpanProcessor для отправки спанов в Jaeger
    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Устанавливаем глобальный формат для трассировки
    set_global_textmap(B3Format())

    # Инструментируем FastAPI приложение до его запуска
    FastAPIInstrumentor().instrument_app(app)

    return app
