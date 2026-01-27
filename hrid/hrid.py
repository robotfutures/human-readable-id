import random
from typing import Iterable

from hrid.word_lists import WORD_LISTS as DEFAULT_WORD_LISTS


class HRID:
    DEFAULT_ELEMENTS = ('adjective', 'noun', 'verb', 'adverb')

    def __init__(
        self,
        delimiter: str = '-',
        elements: Iterable[str] | None = None,
        seed: int | float | str | bytes | bytearray | None = None,
        word_lists: dict[str, list[str]] | None = None,
    ) -> None:
        """
        Initializes the HRID instance with a specified delimiter, elements, and random seed.

        :param delimiter: The string used to join the elements of the generated ID.
        :param elements: An iterable of strings specifying the types of words to include in the ID.
                         If not specified, DEFAULT_ELEMENTS will be used.
        :param seed: An optional seed for the random number generator to ensure reproducibility.
                     Accepts int, float, str, bytes, or bytearray.
        :param word_lists: An optional dictionary mapping element names to word lists.
                           If not specified, the default WORD_LISTS will be used.
                           Use NICE_WORD_LISTS for curated positive/neutral words.

        :return: None
        """
        self.delimiter = delimiter
        self.random = random.Random(seed)
        self.word_lists = word_lists or DEFAULT_WORD_LISTS
        elements = elements or self.DEFAULT_ELEMENTS
        self._elements = [self._transform_element(e) for e in elements]

    def _transform_element(self, element: str | list[str]) -> list[str]:
        """
        Transforms an element into a list of words.

        If the element is a string present in word_lists, it will be replaced by the list of words
        associated with that string.

        If the element is a string, it will be wrapped in a list.

        Otherwise, the element is returned unchanged.

        :param element: The element to transform.
        :return: A list of words.
        """
        if isinstance(element, str):
            if element in self.word_lists:
                return self.word_lists[element]
            return [element]
        return element

    def generate(self):
        """
        Generates a human-readable ID by randomly selecting one word from each of the elements.

        The elements are specified during initialization, and each element is transformed into a list of
        words by the _transform_element method. The words are then joined together with the delimiter
        specified during initialization.

        :return: A string representing a human-readable ID
        """
        words = [self.random.choice(e) for e in self._elements]
        return self.delimiter.join(words)
