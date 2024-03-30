from qrcode.main import QRCode
from os import path
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


class CreateQR:
    def __init__(self):
        self.data = self._get_data()
        self.name = self._get_name()
        self.version = self._get_version()
        self.box_size = self._get_box_size()
        self.border = self._get_border()
        self.fill_color = 'black'
        self.back_color = 'white'
        self.error_correction = self._get_type_qr()
        self.dep = {
            'L': ERROR_CORRECT_L,
            'M': ERROR_CORRECT_M,
            'Q': ERROR_CORRECT_Q,
            'H': ERROR_CORRECT_H
        }

    def _get_input(self, prompt, default):
        value = input(prompt).strip()
        return value if value else default

    def _get_name(self):
        return self._get_input('Write file name >>> ', 'qrcode.png')

    def _get_data(self):
        return self._get_input('Write data >>> ', 'hello')

    def _get_version(self):
        version = self._get_input('Write qr version (1-9, 10-26, 27-40) >>> ', '1')
        return int(version) if version.isdigit() and 1 <= int(version) <= 40 else 1

    def _get_box_size(self):
        size = self._get_input('Write image size >>> ', '10')
        return int(size) if size.isdigit() else 10

    def _get_border(self):
        border = self._get_input('Write amount of empty space >>> ', '2')
        return int(border) if border.isdigit() else 2

    def _get_type_qr(self):
        while True:
            type_qr = self._get_input('Write error recovery levels (L, M, Q, H) >>> ', 'M').upper()
            if type_qr in ['L', 'M', 'Q', 'H']:
                return type_qr
            print("Invalid error. Try again")

    def run(self):
        try:
            qr = QRCode(
                version=self.version,
                error_correction=self.dep[self.error_correction],
                box_size=self.box_size,
                border=self.border
            )

            qr.add_data(self.data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
            img.save(self.name)
            absp = path.abspath(self.name)
            print(f"QR code path > {absp}\n"
                  f"1) Encoded text > {self.data}\n"
                  f"2) File name > {self.name}\n"
                  f"3) QR code version > {self.version}\n"
                  f"4) QR code size > {self.box_size}\n"
                  f"5) Amount of empty space > {self.border}\n"
                  f"6) QR code color > {self.fill_color}\n"
                  f"7) Background color > {self.back_color}\n"
                  f"8) Error recovery level (L, M, Q, H) > {self.error_correction}")
        except ImportError:
            print("Error in importing libraries")
        except KeyboardInterrupt:
            print('\nExit')
        except EOFError:
            print("EOFError")


cur = CreateQR()
cur.run()
