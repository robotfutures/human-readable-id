from hrid.word_lists.nice_adjectives import ADJECTIVES, MOODS
from hrid.word_lists.nice_adverbs import ADVERBS
from hrid.word_lists.nice_nouns import ANIMALS, FLOWERS, NOUNS, PLACES, TREES, WEATHER, FABRICS
from hrid.word_lists.nice_verbs import VERBS

WORD_LISTS = {
    'adjective': ADJECTIVES,
    'mood': MOODS,
    'noun': NOUNS,
    'verb': VERBS,
    'adverb': ADVERBS,
    'animal': ANIMALS,
    'flower': FLOWERS,
    'place': PLACES,
    'tree': TREES,
    'weather': WEATHER,
    'fabric': FABRICS,
    'number': [str(number) for number in range(10, 99)],
}
