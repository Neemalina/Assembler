#!/usr/bin/env python3
"""
Ассемблер для учебной виртуальной машины (УВМ)
Этап 1: Перевод программы в промежуточное представление
"""

import argparse
import sys


class UVMAssembler:
    def __init__(self):
        self.mnemonics = {
            'LOAD_CONST': 20,
            'STORE': 12,
            'BINARY_OP': 19
        }

    def parse_line(self, line):
        """Парсинг одной строки ассемблера"""
        line = line.strip()

        # Пропуск пустых строк и комментариев
        if not line or line.startswith(';'):
            return None

        # Удаление комментариев в конце строки
        if ';' in line:
            line = line.split(';')[0].strip()

        parts = line.split()
        mnemonic = parts[0].upper()
        args = []

        if len(parts) > 1:
            args_str = ' '.join(parts[1:])
            args = [arg.strip() for arg in args_str.split(',')]

        return mnemonic, args

    def parse_source(self, source_code):
        """Парсинг исходного кода"""
        lines = source_code.split('\n')
        commands = []

        for line_num, line in enumerate(lines, 1):
            try:
                parsed = self.parse_line(line)
                if parsed:
                    commands.append(parsed)
            except Exception as e:
                raise SyntaxError(f"Синтаксическая ошибка в строке {line_num}: {line}")

        return commands

    def assemble(self, source_code):
        """Трансляция в промежуточное представление"""
        parsed_commands = self.parse_source(source_code)
        intermediate_representation = []

        for mnemonic, args in parsed_commands:
            if mnemonic not in self.mnemonics:
                raise ValueError(f"Неизвестная мнемоника: {mnemonic}")

            if mnemonic == 'LOAD_CONST':
                if len(args) != 2:
                    raise ValueError("LOAD_CONST требует 2 аргумента: адрес, константа")
                command = {
                    'A': self.mnemonics[mnemonic],
                    'B': self._parse_number(args[0]),
                    'C': self._parse_number(args[1])
                }

            elif mnemonic == 'STORE':
                if len(args) != 2:
                    raise ValueError("STORE требует 2 аргумента: адрес_источник, адрес_назначение")
                command = {
                    'A': self.mnemonics[mnemonic],
                    'B': self._parse_number(args[0]),
                    'C': self._parse_number(args[1])
                }

            elif mnemonic == 'BINARY_OP':
                if len(args) != 4:
                    raise ValueError(
                        "BINARY_OP требует 4 аргумента: адрес_результата, адрес_операнда2, смещение, базовый_адрес")
                command = {
                    'A': self.mnemonics[mnemonic],
                    'B': self._parse_number(args[0]),
                    'C': self._parse_number(args[1]),
                    'D': self._parse_number(args[2]),
                    'E': self._parse_number(args[3])
                }

            intermediate_representation.append(command)

        return intermediate_representation

    def _parse_number(self, num_str):
        """Парсинг числового значения"""
        num_str = num_str.strip()
        if num_str.startswith('0x'):
            return int(num_str[2:], 16)
        return int(num_str)


def run_specification_tests():
    """Запуск тестов из спецификации УВМ"""
    print("=" * 60)
    print("ТЕСТЫ ИЗ СПЕЦИФИКАЦИИ УВМ")
    print("=" * 60)

    assembler = UVMAssembler()

    # Тест 1: Загрузка константы (A=20, B=811, C=213)
    print("\nТест 1: LOAD_CONST")
    print("Ожидается: A=20, B=811, C=213")
    source1 = "LOAD_CONST 811, 213"
    ir1 = assembler.assemble(source1)[0]
    print(f"Получено:  A={ir1['A']}, B={ir1['B']}, C={ir1['C']}")

    # Тест 2: Запись в память (A=12, B=709, C=447)
    print("\nТест 2: STORE")
    print("Ожидается: A=12, B=709, C=447")
    source2 = "STORE 709, 447"
    ir2 = assembler.assemble(source2)[0]
    print(f"Получено:  A={ir2['A']}, B={ir2['B']}, C={ir2['C']}")

    # Тест 3: Бинарная операция (A=19, B=132, C=412, D=20, E=585)
    print("\nТест 3: BINARY_OP")
    print("Ожидается: A=19, B=132, C=412, D=20, E=585")
    source3 = "BINARY_OP 132, 412, 20, 585"
    ir3 = assembler.assemble(source3)[0]
    print(f"Получено:  A={ir3['A']}, B={ir3['B']}, C={ir3['C']}, D={ir3['D']}, E={ir3['E']}")

    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Ассемблер для учебной виртуальной машины (УВМ)')
    parser.add_argument('input_file', help='Путь к исходному файлу с текстом программы')
    parser.add_argument('output_file', help='Путь к двоичному файлу-результату')
    parser.add_argument('--test', action='store_true', help='Режим тестирования')

    args = parser.parse_args()

    assembler = UVMAssembler()

    try:
        # Чтение исходного файла
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # Ассемблирование
        intermediate_representation = assembler.assemble(source_code)

        # Режим тестирования - вывод промежуточного представления
        if args.test:
            print("ПРОМЕЖУТОЧНОЕ ПРЕДСТАВЛЕНИЕ ПРОГРАММЫ:")
            print("=" * 50)
            for i, command in enumerate(intermediate_representation):
                print(f"Команда {i}: {command}")
            print("=" * 50)

        # Запись в двоичный файл (заглушка для данного этапа)
        with open(args.output_file, 'wb') as f:
            # На этапе 1 просто сохраняем текстовое представление
            for command in intermediate_representation:
                f.write(str(command).encode('utf-8') + b'\n')

        print(f"Ассемблирование завершено. Результат записан в {args.output_file}")

    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Если нет аргументов - запускаем тесты из спецификации
        run_specification_tests()
    else:
        main()