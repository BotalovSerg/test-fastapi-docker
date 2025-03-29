import logging
from logging.handlers import RotatingFileHandler


# Настройка логирования
def setup_logger():
    logger = logging.getLogger("App-FastAPI")
    logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логов

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Логирование в файл
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=5 * 1024 * 1024, backupCount=3
    )  # Логи до 5 МБ, 3 резервных файла
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Логирование в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Инициализация логгера
logger = setup_logger()
