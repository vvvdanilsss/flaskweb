import logging
import sys


def setup_logger():
    # Создаем объект logger
    logger = logging.getLogger("my_web_service")
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler("web_service.log")
    file_handler.setLevel(logging.DEBUG)

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Создаем форматтер и добавляем его в обработчики
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики в logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
