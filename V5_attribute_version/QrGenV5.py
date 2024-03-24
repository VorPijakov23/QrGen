from qrcode.main import QRCode
from os import path
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


class CreateQR:
    def __init__(self, data='hello', name='qrcode',
                 version='1',
                 box_size=10,
                 border=2,
                 fill_color='black',
                 back_color='white',
                 error_correction='M'):
        self.data = data  # Дефолтная информация для кодировки
        self.name = name  # Дефолтное название файла
        self.version = version  # Версия QR кода (по умолчанию 1) версии 1-9, версии 10-26 и версии 27-40
        self.box_size = int(box_size)  # Размер QR-кода (по умолчанию 10)
        self.border = int(border)  # Количество пустого пространства (по умолчанию 4)
        self.fill_color = fill_color  # Цвет для самого QR кода (по умолчанию black)
        self.back_color = back_color  # Цвет фона (по умолчанию white)
        self.error_correction = error_correction.upper()  # уровни восстановления ошибок (L, M, Q, H)
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
        return '{}.png'.format(name)

    def _get_data(self):
        data = input('Write data >>> ')
        if not data.strip():
            data = self.data
        return data

    def run(self):
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

            img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
            img.save(name)
            absp = path.abspath(name)
            print(f"Путь QR-кода > {absp}\n"
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


cur = CreateQR(data='hi', name='file', version='6', box_size=15, border=5, error_correction='H')
cur.run()
