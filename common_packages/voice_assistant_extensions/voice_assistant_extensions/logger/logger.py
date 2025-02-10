import json
import sys

from logstash_async.transport import HttpTransport
from loguru import logger
from sentry_sdk import init as sentry_init, capture_exception
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter


class CustomLogstashFormatter(LogstashFormatter):
    def format(self, record):
        # Форматируем запись лога с помощью стандартного форматтера Logstash
        log_record = json.loads(super().format(record))

        # Переносим все поля из extra на верхний уровень
        if "extra" in log_record:
            extra_data = log_record.pop("extra")
            if isinstance(extra_data, dict):
                log_record.update(extra_data)

        return json.dumps(log_record)


class CustomLogger:
    def __init__(
        self,
        service_name: str,
        logstash_host="93.175.29.226",
        logstash_port=24224,
        sentry_dsn="https://example@sentry.io/123",
        logstash_enable: bool = False,
        sentry_enable: bool = False,
        max_length: int = 500,
    ):
        self.logger = logger
        self.logstash_enable = logstash_enable
        self.sentry_enable = sentry_enable
        self.max_length = max_length
        self.service_name = service_name

        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level}</level> | "
            "<level>{message}</level>",
            colorize=True,
            level="DEBUG",
            filter=lambda record: "extra" not in record or not record["extra"],
        )

        # Обработчик для логов с extra
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level}</level> | "
            "<level>{message}</level> | "
            "<level>{extra}</level>",
            colorize=True,
            level="DEBUG",
            filter=lambda record: "extra" in record and record["extra"],
        )

        if logstash_enable:
            # Настройка Logstash
            transport = HttpTransport(
                host=logstash_host,
                port=logstash_port,
                ssl_verify=False,
                ssl_enable=False,
                timeout=5.0,
            )
            # Создаем форматтер, добавляя service_name
            formatter = CustomLogstashFormatter(extra={"service_name": service_name}, extra_prefix=None)
            logstash_handler = AsynchronousLogstashHandler(
                host=logstash_host,
                port=logstash_port,
                transport=transport,
                database_path=None,
            )
            logstash_handler.setFormatter(formatter)

            self.logger.add(
                logstash_handler,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level}</level> | "
                "<level>{message}</level>",
                level="INFO",
            )
        if sentry_enable:
            # Настройка Sentry
            sentry_init(dsn=sentry_dsn)

    def trim_large_data(self, data):
        # Попытка десериализовать строку как JSON
        if isinstance(data, str):
            try:
                data_dict = json.loads(data)
                if isinstance(data_dict, dict):
                    return self.trim_large_data(data_dict)  # Рекурсивная обработка десериализованного словаря
            except json.JSONDecodeError:
                pass

            # Если это не JSON, обрезаем как строку
            if len(data) > self.max_length:
                return f"{data[:self.max_length]}... (truncated)"

        # Обрезка байтов
        if isinstance(data, bytes) and len(data) > self.max_length:
            return f"{data[:self.max_length].decode('utf-8', 'ignore')}... (truncated)"

        # Рекурсивная обработка словаря
        if isinstance(data, dict):
            return {k: self.trim_large_data(v) for k, v in data.items()}

        # Рекурсивная обработка списка
        if isinstance(data, list):
            return [self.trim_large_data(item) for item in data]

        # Если тип данных не строка, байты, словарь или список, вернуть как есть
        return data

    async def log(self, log_func, message: str, **kwargs):
        trimmed_kwargs = {k: self.trim_large_data(v) for k, v in kwargs.items()}
        if trimmed_kwargs:
            log_func(message, **trimmed_kwargs)
        else:
            log_func(message)

    async def info(self, message: str, **kwargs):
        await self.log(self.logger.info, message, **kwargs)

    async def error(self, message: str, **kwargs):
        await self.log(self.logger.error, message, **kwargs)
        if self.sentry_enable:
            capture_exception(Exception(message))

    async def debug(self, message: str, **kwargs):
        await self.log(self.logger.debug, message, **kwargs)

    async def warning(self, message: str, **kwargs):
        await self.log(self.logger.warning, message, **kwargs)

    async def exception(self, message: str, **kwargs):
        await self.log(self.logger.exception, message, **kwargs)
        if self.sentry_enable:
            capture_exception(Exception(message))

    async def critical(self, message: str, **kwargs):
        await self.log(self.logger.critical, message, **kwargs)
        if self.sentry_enable:
            capture_exception(Exception(message))
