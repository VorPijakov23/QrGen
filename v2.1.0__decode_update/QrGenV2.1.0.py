"""
Модуль для создания QR-кодов.

Этот модуль позволяет создавать QR-коды с настраиваемыми параметрами,
которые загружаются из JSON-файла.
"""

import json
from os import path, remove
import re
import logging
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from pyzbar.pyzbar import decode
from PIL import Image
import requests
from io import BytesIO


class CreateQR:
    """
    Класс для создания QR-кодов.

    Этот класс позволяет создавать QR-коды с настраиваемыми параметрами,
    которые загружаются из JSON-файла.
    """

    def __init__(self):
        # Загружаем данные из JSON-файла
        with open("conf.json", "r", encoding='utf-8') as f:
            config = json.load(f)

        # Дефолтная информация для кодирования
        self.data: str = config['default_data']
        # Дефолтное название файла
        self.name: str = f"{config['default_file_name']}.png"
        self.version: int = int(config['qr_version'])  # Версия QR кода
        self.box_size: int = int(config['box_size'])  # Размер QR-кода
        self.border: int = int(config['border'])  # Количество пустого пространства
        self.fill_color: str = config['fill_color']  # Цвет для самого QR кода
        self.back_color: str = config['back_color']  # Цвет фона
        self.temp_file_name: str = config['download_temp_file_name']
        # уровни восстановления ошибок
        self.error_correction: str = config['error_correction'].upper()
        self.dep: dict = {
            'L': ERROR_CORRECT_L,
            'M': ERROR_CORRECT_M,
            'Q': ERROR_CORRECT_Q,
            'H': ERROR_CORRECT_H
        }
        self.url_or_path: str = config["url_or_path"]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _download_image(self, url: str) -> None:
        # Отправляем GET-запрос на URL-адрес изображения
        response = requests.get(url)
        name: str = self.temp_file_name

        # Проверяем, что запрос был успешным
        if response.status_code == 200:
            # Пытаемся открыть изображение с помощью Pillow
            try:
                image = Image.open(BytesIO(response.content))
                # Сохраняем изображение
                image.save(name)
                self.logger.info(f"Изображение успешно сохранено в {name}")
            except IOError:
                self.logger.error("Не удалось открыть изображение. Возможно, оно не является изображением.")
        else:
            self.logger.error(f"Ошибка при загрузке изображения: статус код {response.status_code}")

    def _dec(self, image_path: str) -> str:
        """Инкапсулированный метод для расшифровки сохранённого QR-кода"""
        try:
            img = Image.open(image_path)
            res = '\n\n'.join([i.data.decode('utf-8') for i in decode(img)])
            return f"Расшифрованные QR-Коды:\n {res}"
        except FileNotFoundError:
            return "Файл не найден, проверьте конфигурацию"
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

    def decode_qrcode(self) -> str:
        """
        Основной метод для расшифровки QR-кода
        """
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        path_pattern = re.compile(
            r'^(/[^/ ]*)+/?$'
        )
        file_name_pattern = re.compile(
            r'^[\w,\s-]+\.[A-Za-z]{3}$'
        )
        u_or_p = self.url_or_path

        # Проверка соответствия шаблонам
        if url_pattern.match(u_or_p):
            self._download_image(u_or_p)
            res = self._dec(self.temp_file_name)
            remove(self.temp_file_name)
            return res
        elif path_pattern.match(u_or_p) or file_name_pattern.match(u_or_p):
            res = self._dec(u_or_p)
            return res
        else:
            return "Некорректное имя файла"

    def get_qrcode(self) -> None:
        """
        Метод для создания QR-кода.

        Этот метод запускает процесс создания QR-кода с использованием
        настроек, загруженных из JSON-файла.
        """
        data: str = self.data
        name: str = self.name
        try:
            qr = QRCode(
                version=self.version,
                error_correction=self.dep[self.error_correction],
                box_size=self.box_size,
                border=self.border
            )

            qr.add_data(data)
            qr.make()

            img = qr.make_image(fill_color=self.fill_color,
                                back_color=self.back_color)
            img.save(name)
            abs_path: str = path.abspath(name)
            print(f"Путь QR-кода > {abs_path}\n"
                  f"1) Кодированный текст > {data}\n"
                  f"2) Название файла > {name}\n"
                  f"3) Версия QR-кода > {self.version}\n"
                  f"4) Размер QR-кода > {self.box_size}\n"
                  f"5) Количество пустого пространства > {self.border}\n"
                  f"6) Цвет QR-кода > {self.fill_color}\n"
                  f"7) Цвет фона > {self.back_color}\n"
                  f"8) Уровень восстановления ошибок (L, M, Q, H) > {self.error_correction}")
        except ImportError:
            print("Ошибка в импорте библиотек")
        except KeyboardInterrupt:
            print('\nExit')
        except EOFError:
            print("EOFError")


def main() -> None:
    """Главная функция"""
    cur = CreateQR()
    print(cur.decode_qrcode())


if __name__ == "__main__":
    """Точка входа в программу"""
    main()
