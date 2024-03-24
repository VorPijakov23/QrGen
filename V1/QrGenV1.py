def get_name(filename):
    name = input("write file name >>>")
    if not name.strip():
        name = filename
    return '{}.png'.format(name)


def get_data(def_data):
    data = input('write data >>>')
    """while not data.strip():
        data = input('wrote data again >>>')"""
    if not data.strip():
        data = def_data
    return data


def main():
    try:
        import qrcode
        from dotenv import load_dotenv
        from os import getenv, path
        from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
        load_dotenv()
    except ImportError:
        print("Ошибка в импорте библиотек")
        return
    if not path.isfile('.env'):
        print('Файл .env не найден')
        return
    data = get_data(getenv('default_data'))  # Дефолтная информация для кодировки
    name = get_name(getenv('default_file_name'))  # Дефолтное название файла
    version = getenv('qr_version')  # Версия QR кода (по умолчанию 1) версии 1-9, версии 10-26 и версии 27-40
    box_size = int(getenv('box_size'))  # Размер QR-кода (по умолчанию 10)
    border = int(getenv('border'))  # Количество пустого пространства (по умолчанию 4)
    fill_color = getenv('fill_color')  # Цвет для самого QR кода (по умолчанию black)
    back_color = getenv('back_color')  # Цвет фона (по умолчанию white)
    error_correction = getenv('error_correction').upper()  # 4 различных уровня восстановления ошибок (L, M, Q, H)
    dep = {
        'L': ERROR_CORRECT_L,
        'M': ERROR_CORRECT_M,
        'Q': ERROR_CORRECT_Q,
        'H': ERROR_CORRECT_H
    }
    qr = qrcode.main.QRCode(
        version=version,
        error_correction=dep[error_correction],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make()

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    img.save(name)
    absp = path.abspath(name)
    print(f"Путь QR-кода > {absp}\n"
          f"1) Кодированный текст > {data}\n"
          f"2) Название файла > {name}\n"
          f"3) Версия QR-кода > {version}\n"
          f"4) Размер QR-кода > {box_size}\n"
          f"5) Количество пустого пространства > {border}\n"
          f"6) Цвет QR-кода > {fill_color}\n"
          f"7) Цвет фона > {back_color}\n"
          f"8) Уровень восстановления ошибок (L, M, Q, H) > {error_correction}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit')
    except EOFError:
        print("EOFError")
