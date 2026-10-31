# Задание 9

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
    # Исходное сообщение из задания
    text = "ABCADE"
    freq = Counter(text)

    # Построение дерева и кодирование сообщения
    tree, codes = build_huffman(freq)
    bits = encode(text, codes)

    # Расчёт характеристик кода
    _, entropy, avg_len, efficiency, redundancy = calculate_metrics(text, codes)

    print("ЗАДАНИЕ 9. ПРОГРАММНАЯ РЕАЛИЗАЦИЯ")
    print("Исходное сообщение:", text)

    print("\\nТАБЛИЦА КОДОВ")
    print_code_table(freq, codes)

    print("\\nКОДИРОВАНИЕ И ДЕКОДИРОВАНИЕ")
    print("Закодированная строка:", bits)
    print("Длина битовой строки:", len(bits), "бит")
    print("Декодированное сообщение:", decode(bits, tree))

    print("\\nХАРАКТЕРИСТИКИ")
    print("Энтропия H(X):", round(entropy, 4), "бит/символ")
    print("Средняя длина L:", round(avg_len, 4), "бит/символ")
    print("Эффективность:", round(efficiency, 2), "%")
    print("Избыточность:", round(redundancy, 2), "%")

    # Проверка правильности восстановления исходного сообщения
    assert decode(bits, tree) == text
    print("\\nПроверка decode(encode(text)) == text пройдена.")

    # Проверка специального случая: только один уникальный символ
    one_text = "AAAAA"
    one_tree, one_codes = build_huffman(Counter(one_text))
    one_bits = encode(one_text, one_codes)

    print("\\nПРОВЕРКА ОДНОГО УНИКАЛЬНОГО СИМВОЛА")
    print("Исходный текст:", one_text)
    print("Код символа A:", one_codes["A"])
    print("Закодированная строка:", one_bits)
    print("Декодирование:", decode(one_bits, one_tree))

    assert one_codes["A"] == "0"
    assert decode(one_bits, one_tree) == one_text
    print("Проверка одного символа пройдена.")


if __name__ == "__main__":
    main()
