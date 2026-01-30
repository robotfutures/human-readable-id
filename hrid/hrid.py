import math
import random
from typing import Iterable

from hrid.word_lists import WORD_LISTS as DEFAULT_WORD_LISTS


def _mod_inverse(a: int, m: int) -> int:
    """Compute modular multiplicative inverse using extended Euclidean algorithm."""
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1

    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m


class HRID:
    DEFAULT_ELEMENTS = ('adjective', 'noun', 'verb', 'adverb')

    def __init__(
        self,
        delimiter: str = '-',
        elements: Iterable[str] | None = None,
        seed: int | float | str | bytes | bytearray | None = None,
        word_lists: dict[str, list[str]] | None = None,
        scramble: bool = True,
        scramble_seed: str | None = None,
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
        :param scramble: If True, scramble sequential numbers to produce varied IDs.
                         Uses multiplicative scrambling to spread consecutive inputs
                         across the ID space. Useful when encoding sequential IDs.
        :param scramble_seed: Seed for deterministic scramble multiplier selection.
                              Different seeds produce different scrambling patterns.
                              Useful for per-model uniqueness (e.g., use model name).

        :return: None
        """
        self.delimiter = delimiter
        self.random = random.Random(seed)
        self.word_lists = word_lists or DEFAULT_WORD_LISTS
        elements = elements or self.DEFAULT_ELEMENTS
        self._elements = [self._transform_element(e) for e in elements]
        self._scramble = scramble
        self._scramble_seed = scramble_seed

        # Compute total space size and scrambling parameters
        self._space_size = math.prod(len(e) for e in self._elements)
        # Choose a scramble multiplier coprime to space_size
        self._scramble_multiplier = self._find_coprime(self._space_size, scramble_seed)
        self._scramble_inverse = _mod_inverse(self._scramble_multiplier, self._space_size)

    def _find_coprime(self, n: int, seed: str | None = None) -> int:
        """Find a number coprime to n for scrambling distribution.

        If seed is provided, uses it to deterministically select a coprime,
        ensuring different seeds produce different scrambling patterns.
        """
        if seed is not None:
            # Use seed to generate a deterministic coprime
            rng = random.Random(seed)
            # Try random candidates until we find a coprime
            for _ in range(1000):
                candidate = rng.randint(n // 3, n - 1)
                if math.gcd(candidate, n) == 1:
                    return candidate

        # Default: use well-known constants (golden ratio-derived primes)
        candidates = [2654435769, 1640531527, 2166136261, 16777619]
        for c in candidates:
            if math.gcd(c, n) == 1:
                return c
        # Fallback: find any coprime
        for c in range(n // 2, n):
            if math.gcd(c, n) == 1:
                return c
        return 1  # Should never happen unless n=1

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

    @property
    def max_value(self) -> int:
        """Return the maximum encodable value (space_size - 1)."""
        return self._space_size - 1

    def encode(self, n: int) -> str:
        """
        Encode an integer into a human-readable ID.

        The encoding uses a mixed-radix number system where each word list
        represents a digit. If scramble=True was set during initialization,
        consecutive integers will produce visually distinct IDs.

        :param n: The integer to encode (must be 0 <= n < space_size)
        :return: A human-readable ID string
        :raises ValueError: If n is out of range
        """
        if not 0 <= n < self._space_size:
            raise ValueError(
                f"Value {n} out of range. Must be 0 <= n < {self._space_size}"
            )

        # Apply scrambling if enabled
        if self._scramble:
            n = (n * self._scramble_multiplier) % self._space_size

        # Convert to mixed-radix representation
        parts = []
        for words in reversed(self._elements):
            base = len(words)
            parts.append(words[n % base])
            n //= base
        return self.delimiter.join(reversed(parts))

    def decode(self, hrid: str) -> int:
        """
        Decode a human-readable ID back to an integer.

        :param hrid: The human-readable ID string to decode
        :return: The original integer
        :raises ValueError: If any word in the ID is not found in the corresponding word list
        """
        parts = hrid.split(self.delimiter)
        if len(parts) != len(self._elements):
            raise ValueError(
                f"Expected {len(self._elements)} parts, got {len(parts)}"
            )

        # Convert from mixed-radix representation
        n = 0
        for part, words in zip(parts, self._elements):
            try:
                idx = words.index(part)
            except ValueError:
                raise ValueError(f"Word '{part}' not found in word list") from None
            n = n * len(words) + idx

        # Reverse scrambling if enabled
        if self._scramble:
            n = (n * self._scramble_inverse) % self._space_size

        return n
