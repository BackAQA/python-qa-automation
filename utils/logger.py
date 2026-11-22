
import logging
import os
from pathlib import Path


# Определяем корневую папку проекта
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Создаём папку для журналов
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Для параллельного запуска используем отдельный файл каждого процесса
WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "main")
LOG_FILE = LOG_DIR / f"automation-{WORKER_ID}.log"


def get_logger(name: str = "python_qa_automation") -> logging.Logger:
    """Создаёт и настраивает журналирование проекта."""

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Не добавляем обработчики повторно
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Вывод сообщений в терминал
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Запись сообщений в файл
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Общий журнал проекта
logger = get_logger()
