# Задание 10

import heapq
import math
from itertools import count
from collections import Counter


def build_huffman(freq):
    """Строит дерево Хаффмана и таблицу двоичных кодов."""
    if not freq:
        raise ValueError("Пустой алфавит")

    order = count()
    heap = [(weight, next(order), symbol)
            for symbol, weight in freq.items() if weight > 0]
    heapq.heapify(heap)

    if not heap:
        raise ValueError("Все частоты нулевые")

    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))

    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


def encode(text, codes):
    """Кодирует текст в последовательность битов."""
    return "".join(codes[symbol] for symbol in text)


def decode(bits, tree):
    """Декодирует последовательность битов обратно в текст."""
    if isinstance(tree, str):
        if any(bit != "0" for bit in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        if bit not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(bit)]
        if isinstance(node, str):
            result.append(node)
            node = tree

    if node is not tree:
        raise ValueError("Неполное кодовое слово")

    return "".join(result)


def calculate_metrics(text, codes):
    """Рассчитывает энтропию, среднюю длину, эффективность и избыточность."""
    freq = Counter(text)
    total = len(text)

    entropy = -sum(
        (amount / total) * math.log2(amount / total)
        for amount in freq.values()
    )
    average_length = sum(
        (freq[symbol] / total) * len(codes[symbol])
        for symbol in freq
    )
    efficiency = entropy / average_length * 100
    redundancy = 100 - efficiency

    return freq, entropy, average_length, efficiency, redundancy


def print_code_table(freq, codes):
    """Выводит таблицу символов и кодовых слов."""
    print(f"{'Символ':<12}{'Частота':<12}{'Вероятность':<16}{'Код':<16}{'Длина'}")
    total = sum(freq.values())

    for symbol in sorted(freq):
        probability = freq[symbol] / total
        print(
            f"{repr(symbol):<12}{freq[symbol]:<12}"
            f"{probability:<16.4f}{codes[symbol]:<16}{len(codes[symbol])}"
        )


def main():
    # Текст на русском языке. Учитываются пробелы, переносы строк,
    # регистр букв и знаки препинания.
    text = """
В городе Вероне жили две знатные семьи — Монтекки и Капулетти.
Между ними давно существовала сильная вражда. Никто уже не помнил,
с чего началась эта ссора, но неприязнь передавалась из поколения
в поколение. Однажды юный Ромео, принадлежавший к семье Монтекки,
оказался на празднике в доме Капулетти. Там он встретил Джульетту,
дочь главы враждующей семьи. Молодые люди сразу почувствовали
взаимную симпатию и вскоре поняли, что полюбили друг друга.

Ромео и Джульетта знали, что их родные не одобрят эту любовь.
Несмотря на опасность, они решили тайно встречаться. Им помогал
монах Лоренцо, который надеялся, что брак молодых людей сможет
примирить две семьи. Но ненависть и старые обиды продолжали
влиять на поступки окружающих. Между представителями семей
происходили ссоры, и положение становилось всё опаснее.

Влюблённые мечтали о спокойной жизни, в которой им не пришлось
бы скрывать свои чувства. Однако события развивались трагически.
Из-за недоразумений и случайностей Ромео и Джульетта потеряли
возможность быть вместе. Их история стала напоминанием о том,
к каким последствиям могут привести вражда, гордость и ненависть.
"""

    if len(text) < 300:
        raise ValueError("Текст должен содержать не менее 300 символов.")

    # Подсчёт частот и построение дерева Хаффмана
    freq = Counter(text)
    tree, codes = build_huffman(freq)
    bits = encode(text, codes)

    # Расчёт энтропии, средней длины, эффективности и избыточности
    _, entropy, avg_len, efficiency, redundancy = calculate_metrics(text, codes)

    print("ЗАДАНИЕ 10. АНАЛИЗ ТЕКСТА")
    print("Произведение: «Ромео и Джульетта»")
    print("Автор оригинала: Уильям Шекспир")
    print("Использован учебный пересказ по мотивам произведения.")
    print("Учитываются пробелы, переносы строк, регистр и пунктуация.")
    print("Количество символов:", len(text))
    print("Количество различных символов:", len(freq))

    print("\\nТАБЛИЦА ЧАСТОТ И КОДОВ")
    print_code_table(freq, codes)

    print("\\nХАРАКТЕРИСТИКИ КОДИРОВАНИЯ")
    print("Энтропия H(X):", round(entropy, 4), "бит/символ")
    print("Средняя длина L:", round(avg_len, 4), "бит/символ")
    print("Эффективность:", round(efficiency, 2), "%")
    print("Избыточность:", round(redundancy, 2), "%")
    print("Длина битового потока:", len(bits), "бит")

    # Сравнение исходного текста UTF-8 с упакованным потоком Хаффмана
    original_size = len(text.encode("utf-8"))
    compressed_size = (len(bits) + 7) // 8
    padding_bits = (8 - len(bits) % 8) % 8

    # Условная оценка таблицы кодов:
    # байты символа UTF-8 + 1 байт длины кода + байты кода.
    table_size = sum(
        len(symbol.encode("utf-8")) + 1 + (len(codes[symbol]) + 7) // 8
        for symbol in freq
    )

    total_size = compressed_size + table_size
    compression_ratio = original_size / total_size if total_size else 0
    size_change = (1 - total_size / original_size) * 100

    print("\\nСРАВНЕНИЕ ОБЪЁМА")
    print("Исходный текст UTF-8:", original_size, "байт")
    print("Упакованный поток Хаффмана:", compressed_size, "байт")
    print("Таблица кодов (оценка):", table_size, "байт")
    print("Общий объём с таблицей:", total_size, "байт")
    print("Дополнение последнего байта:", padding_bits, "бит")
    print("Коэффициент сжатия:", round(compression_ratio, 3))
    print("Изменение объёма:", round(size_change, 2), "%")

    # Проверка, что декодирование полностью восстанавливает текст
    decoded = decode(bits, tree)
    assert decoded == text
    print("\\nПроверка декодирования пройдена.")

    print("\\nВЫВОД")
    print(
        "Код Хаффмана назначает короткие коды часто встречающимся символам "
        "и более длинные коды редким символам. При оценке сжатия необходимо "
        "учитывать служебные данные — таблицу кодов и выравнивание последнего байта."
    )
    if total_size < original_size:
        print("С учётом принятой оценки таблицы сжатие выгодно.")
    else:
        print("С учётом принятой оценки таблицы сжатие не уменьшило объём.")


if __name__ == "__main__":
    main()
