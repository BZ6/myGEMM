# Исследовательский проект по изучению зависимости времени умножения квадратных матриц на GPU от параметров (размер рабочей группы, ядро)

Проект исследует, как различные параметры (размер рабочей группы и ядра с некоторой оптимизацией) влияют на
время выполнения программы для умножения квадратных матриц на GPU на одноплатном мини-компьютере BananaPi с
архитектурой RISC-V.

## Цель

Найти оптимальную конфигурацию для максимально быстрого выполнения вычислений.

## Платформа

- BananaPi на RISC-v архитектуре
- Был использован проект [myGEMM](https://github.com/CNugteren/myGEMM) с малыми измененниями

## Общие сведения для понимания проекта

- Используется многопоточность по данным (SIMD), то есть выполнение одной и той же инструкции для множества
  данных одновременно
- Ядро (kernel) в контексте графических процессоров (GPU) — это небольшая программа или функция, которая
  выполняется на одном из множества вычислительных блоков
- Рабочая группа (work-group) в контексте вычислений на графических процессорах (GPU) — это набор
  потоков (threads), которые выполняют одно и то же ядро параллельно и совместно обрабатывают данные
- Размер рабочей группы определяет количество потоков, которые выполняются параллельно внутри одной рабочей
  группы

## Результаты исследования

![image](https://github.com/user-attachments/assets/0159d49b-fbb8-418d-b5e6-67b12e3a491a)

- Успел провести только по 50 измерений для первых 5 ядер и 3 разных размеров рабочих групп: 8, 16, 32 (данный
  размер не дает скомпилировать 1 и 2 ядро на исследуемой платформе, поэтому данные на графике отсутсвуют).
- В моем маленьком исследовании по графику можно судить, что в среднем лучшей конфигурацией оказалось 4 ядро с
  размером рабочей группы 32.
- С увеличением порядкового номера ядра наблюдается уменьшение времени выполнения, что соответствует ожиданиям,
  так как с каждым новым ядром улучшается его оптимизация. Однако, для 5-го ядра это правило не выполняется.
  Вероятно, за прошедшие примерно 10 лет с момента написания myGEMM произошли изменения в архитектуре
  графических ускорителей, из-за чего оптимизация, использованная в 5-м ядре, стала менее эффективной.

## Инструкция по работе с проектом

### Общие требования

- Наличие компилятора C++
- Наличие make
- Наличие OpenCL (можно проверить наличие с помощью ввода в консоль clinfo)
- Наличие clBLAS

#### Установка компилятора C++

```bash
sudo apt install g++
```

#### Установка make

```bash
sudo apt install make
```

#### Установка OpenCL

- К сожалению все зависит от вендора, но можно проверить наличие командой `clinfo`,
  если он не распознал или вывел 0 платформ, то приедется установить самые свежие драйвера и
  поискать подходящий SDK от вендора

#### Установка clBLAS

```bash
sudo apt install libclblas-dev
```

### При наличии графического ускорителя c CUDA ядрами

- Нужно становить cuBLAS
- Нужно зайти в Makefile и поменять значение ENABLE_CUDA с 0 на 1, этот параметр показывает
  испсользуется ли CUDA-специфичные функции и ядра

### Вывод программы

| backend   | kernel  | work group size | opencl standart | matrix size | work time(sec)  |
| ------    | ------  | ------          | ------          | ------      | ------          |
| myGEMM.cl | 1       | 8               | -cl-std=CL1.2   | 256         | 0.08002         |

### Инструкция по использованию

- Если хочется просто запустить, то достаточно написать `make`
- Если хочется провести иследования, то нужно работать с файлами:
  - research.py (с помощью него происходит автоматичекий запуск и перенаправление всего вывода в файл):
    можно ислледовать вас интересующие ядра(kernels) и размеры рабочих групп(work_groups)
  - src/common.h:
    можно ислледовать вас интересующие размеры матрицы, которые начинаются с MINSIZE и заканчиваются MAXSIZE
    с шагом x2
  - src/settings.h (тут находятся параметры связанные с ядрами):
    можно исследовать различные ядра(KERNELS) и размеры рабочих групп(TS), но лучше не менять их руками, а
    использовать research.py, еще есть параметры компиляции ядер(COMPILER_OPTIONS), в которые можно через
    пробел указывать различные флаги, например быстрая математика, и параметры, например стандарт
  - filter.py (фильтрует данные из выходного файла программы, который больше выполняет функцию логирования):
    можно указывать файлы, который хотим отфильтровать(input_file) и в который хотим записать экспериментальные
    данные(output_file)
