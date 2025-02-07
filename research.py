import subprocess
import os

def run_command(command, output_file):
    """Выполняет команду и записывает вывод в файл."""
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)

    # Записываем стандартный вывод и стандартный поток ошибок в файл
    with open(output_file, 'a') as file:
        # file.write(f'Command: {command}\n')
        # file.write(f'Standard Output:\n')
        file.write(f'{result.stdout}\n')

    return result

def run_scenarios(scenarios, output_file):
    """Выполняет сценарии по очереди и записывает вывод в файл."""
    for scenario in scenarios:
        print(f'Выполнение сценария: {scenario}')
        run_command(scenario, output_file)

def cartesian_product_concat(str, set1):
    result = []
    for s1 in set1:
        result.append(str + s1)
    return result

def all(kernel_replaces, work_groups_replaces, scenarios_to_run):
    result = []
    for s1 in kernel_replaces:
        for s2 in work_groups_replaces:
            result.append(s1)
            result.append(s2)
            for s3 in scenarios:
                result.append(s3)
    return result

if __name__ == "__main__":
    output_file = 'RISCV_res.csv'  # Файл для записи вывода

    # Рабочие kernels: 1, 2, 4, 10
    # kernels = [
    #     '1"',
    #     '2"',
    #     '4"',
    #     '10"'
    # ]
    # work_groups = [
    #     '2"',
    #     '4"',
    #     '8"',
    #     '16"',
    #     '32"'  
    # ]

    kernels = [
        '1"',
        '2"',
        '3"',
        '4"',
        '5"'
    ]
    work_groups = [
        '8"',
        '16"',
        '32"'
    ]

    replaces = [
        'python3 replace_line.py ./src/settings.h 17 "#define KERNEL ',
        'python3 replace_line.py ./src/settings.h 20 "#define TS '
    ]
    scenarios = [
        'make',
#        './bin/myGEMM'
    ]

#    for i in range(8):
#        scenarios.append(scenarios[1])

    # Сценарии для выполнения
    kernel_replaces = cartesian_product_concat(replaces[0], kernels)
    work_groups_replaces = cartesian_product_concat(replaces[1], work_groups)

    scenarios_to_run = []

    # scenarios_to_run.append(all(kernel_replaces, work_groups_replaces, scenarios))

    scenarios_to_run.extend(all(kernel_replaces[0:2], work_groups_replaces[0:2], scenarios))
    scenarios_to_run.extend(all(kernel_replaces[2:], work_groups_replaces, scenarios))

    # Выполнение сценариев
    run_scenarios(scenarios_to_run, output_file)
