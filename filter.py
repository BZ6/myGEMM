import re

def filter_lines_by_pattern(input_file, output_file, pattern):
    # Компилируем регулярное выражение
    regex = re.compile(pattern)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Если строка соответствует шаблону, записываем её в выходной файл
            if regex.match(line):
                outfile.write(line)

# Пример использования
input_file = 'RISCV1math.csv'
output_file = 'RISC_V_4_BZ.csv'
# Шаблон для строк, соответствующих формату ваших данных
pattern = r'^\s*\w+\.?\w*,\s*\d+,\s*\d+,\s*-cl-std=CL\d\.\d -cl-fast-relaxed-math,\s*\d+,\s*\d+\.\d+\s*$'

filter_lines_by_pattern(input_file, output_file, pattern)
