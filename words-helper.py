#!/usr/bin/env python3

import re
import argparse
import itertools


def get_words() -> list[str]:
    """Читает файл в кодировке CP1251, разбивает в список слов и возвращает её

    Returns:
        list[str]: Список всевозможных слов хранимый в файле
    """
    with open("russian-words/russian.txt", "r", encoding="CP1251") as f:
        return f.read().split("\n")


def get_all_combinations(symbols: str) -> set[str]:
    """Функция формирует всевозможные уникальные комбинации из входной строки.
    Минимальная длина уникальной комбинации равен 4 символам.

    Args:
        symbols (str): Принимает буквы из которого формируется комбинации,
        букв должно быть не менее 4, иначе вернется пустой set

    Returns:
        set[str]: Уникальные комбинации, которые сформировался из входного параметра symbols
    """
    unique_symbols = set()
    if len(symbols) < 4:
        return unique_symbols
    for index in range(4, len(symbols) + 1):
        _unique = set(("".join(x) for x in itertools.permutations(symbols, index)))
        unique_symbols |= _unique
    return unique_symbols


def find_words(symbols: str) -> list[str]:
    """Функция, который находит всевозможные слова, которые можно сформировать из
    предоставленных букв (минимальная длина слова 4 буквы)

    Args:
        symbols (str): буквы из которых требуется сформировать всевозможные слова

    Returns:
        list[str]: Список всевозможных слов, который можно сформировать из входных букв
    """
    length = len(symbols)
    all_words = set((x for x in get_words() if len(x) <= length))
    unique_combinations = get_all_combinations(symbols)
    commons_words = unique_combinations & all_words
    return sorted(commons_words, key=lambda s: (-len(s), s))


def get_need_words(words: list[str], length: int | None = None, **kwargs):
    """Возвращает только те слова из списка, которые соответствует входным параметрам

    Args:
        words (list[str]): Список слов, которые на фильтровать по дополнительным параметрам
        length (int | None, optional): Возвращает только те слова, которые соответствует указанной длине. По умолчанию None.
        kwargs: параметры по которым дополнительно фильтруется, то есть если указать в параметрах `й=3`,
        то будет возвращаться только те слова у которых 3 буква равен `й`. Можно указывать неограниченное количество таких параметров

    Yields:
        str: Возвращает слово в случае соответствии с входными фильтрами
    """
    for word in words:
        if length and len(word) != length:
            continue
        is_good = True
        for k, v in kwargs.items():
            if word[int(v) - 1] != k:
                is_good = False
                break
        if is_good:
            yield word


def parse_kwargs(unknown_args: list[str]) -> dict[str, int]:
    """Парсит дополнительные параметры kwargs, которые пришли из argparse.ArgumentParse

    Args:
        unknown_args (list[str]): Принимает значение пришедшие из ArgumentParse().parse_known_args(), которые не удалось распарсить

    Raises:
        ValueError: В случае если входные параметры указаны некорректно

    Returns:
        dict[str, int]: дополнительные параметры для фильтрации слов
    """
    kwargs = {}
    pattern = re.compile(r"^([\wа-яА-ЯёЁ])=(\d+)$", re.UNICODE)

    for arg in unknown_args:
        _match = pattern.match(arg)
        if not _match:
            raise ValueError(
                f"Некорректный формат аргумента: {arg}. Ожидается формат ключ=целое число (пример: п=1)"
            )
        key, value = _match.groups()
        kwargs[key] = value
    return kwargs


def main():
    parser = argparse.ArgumentParser(
        description="CLI: буквы (позиционно или через --word), длина, и kwargs с кириллическими ключами и целыми значениями (ключ буква, значение позиция в слове)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("word", nargs="?", help="Буквы (позиционно)")
    group.add_argument("-w", "--word", help="Буквы (через ключ)")

    parser.add_argument("-l", "--length", type=int, help="Опциональная длина")
    args, unknown = parser.parse_known_args()
    word = args.word
    try:
        kwargs = parse_kwargs(unknown)
    except ValueError as e:
        parser.error(str(e))
    words = find_words(word)
    for w in get_need_words(words, args.length, **kwargs):
        print(w)


if __name__ == "__main__":
    main()
