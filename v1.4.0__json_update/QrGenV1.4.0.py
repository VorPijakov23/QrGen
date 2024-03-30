"""
Модуль для создания QR-кодов.

Этот модуль позволяет создавать QR-коды с настраиваемыми параметрами,
которые загружаются из JSON-файла.
"""

import json
from os import path
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


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
        self.data = config['default_data']
        self.name = config['default_file_name']  # Дефолтное название файла
        self.version = int(config['qr_version'])  # Версия QR кода
        self.box_size = int(config['box_size'])  # Размер QR-кода
        self.border = int(config['border'])  # Количество пустого пространства
        self.fill_color = config['fill_color']  # Цвет для самого QR кода
        self.back_color = config['back_color']  # Цвет фона
        # уровни восстановления ошибок
        self.error_correction = config['error_correction'].upper()
        self.dep = {
            'L': ERROR_CORRECT_L,
            'M': ERROR_CORRECT_M,
            'Q': ERROR_CORRECT_Q,
            'H': ERROR_CORRECT_H
        }

    def _get_name(self):
        name = input('Write file name >>> ')
        if not name.strip():
            name = self.name
        return f'{name}.png'

    def _get_data(self):
        data = input('Write data >>> ')
        if not data.strip():
            data = self.data
        return data

    def run(self):
        """
        Основной метод для запуска программы.

        Этот метод запускает процесс создания QR-кода с использованием
        настроек, загруженных из JSON-файла.
        """
        try:
            name = self._get_name()
            data = self._get_data()
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
            abs_path = path.abspath(name)
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
    cur.run()


if __name__ == "__main__":
    main()
