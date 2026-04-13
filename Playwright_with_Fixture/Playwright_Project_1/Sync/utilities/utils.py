import logging

import logging
import os
import datetime
from colorama import Fore, Style, init


# ============================================================
# 🎨 Цвета для консоли
# ============================================================
init(autoreset=True)

# ============================================================
# 📁 Путь к логам
# ============================================================

# abc_path = r''
# LOG_DIR = os.path.join(abc_path, "logs")

current_dir = os.getcwd()
# Папка LOG_DIR находится на уровне выше текущей директории:
path_dir = os.path.abspath(os.path.join(current_dir, "logs"))
os.makedirs(path_dir, exist_ok=True)
LOG_DIR = path_dir
# или, если корневая точка — корень проекта:
# LOG_DIR = "logs"




# Имя файла по дате
today = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_DIR, f"{today}_project_log.txt")

# ============================================================
# ⚙️ Настройка логгера
# ============================================================
logger = logging.getLogger("project")

if not logger.handlers:
    # Формат логов для файла
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Обработчик для файла (запись “молча”)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(file_format)

    # Добавляем только файловый хендлер — консоль не логируется!
    logger.addHandler(file_handler)

    # Уровень логирования
    logger.setLevel(logging.INFO)

# ============================================================
# 🧩 Функции логирования (печатают только цветом, пишут только в файл)
# ============================================================

def log_message(message: str) -> None:
    """Обычное сообщение (INFO)"""
    logger.info(message)
    print(Style.BRIGHT + message + Style.RESET_ALL)


def step(message: str) -> None:
    """Шаг (синий)"""
    logger.info(message)
    print(f"{Fore.CYAN}➡️ {message}{Style.RESET_ALL}")


def success(message: str) -> None:
    """Успех (зелёный)"""
    logger.info(message)
    print(f"\t{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def warning(message: str) -> None:
    """Предупреждение (жёлтый)"""
    logger.warning(message)
    print(f"{Fore.YELLOW}⚠️ {message}{Style.RESET_ALL}")


def error(message: str) -> None:
    """Ошибка (красный)"""
    logger.error(message)
    print(f"\t{Fore.RED}❌ {message}{Style.RESET_ALL}")



# def get_users(driver, wait):
#     """
#     Возвращает список пользователей со страницы.
#     Если wait передан — ждёт появления блока, иначе ищет сразу.
#     """
#     try:
#         if wait:
#             wait.until(EC.presence_of_element_located((By.ID, 'login_credentials')))
#         user_div = driver.find_element(By.ID, 'login_credentials')
#         lines = user_div.text.splitlines()
#         if 'Accepted usernames are:' in lines:
#             lines.remove('Accepted usernames are:')
#         return lines
#     except NoSuchElementException:
#         return None