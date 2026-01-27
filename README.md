[![N|Solid](https://repository-images.githubusercontent.com/324334992/6016fe00-4882-11eb-8824-68c825521965)](https://github.com/hnimminh/human-readable-id)


<p align="center">
  <strong>HRID: Human Readable Identifier</strong>
  <br>
  <code>The Human Readable ID Generator Library For Python3</code>
  <br>
</p>

## Usage

Install
```
pip3 install hrid
```

Basic usage
```python
from hrid import HRID

hrid = HRID()
print(hrid.generate())  # e.g., "calm-apple-hop-quietly"
```

### Custom Elements

```python
from hrid import HRID

# Use different word types
hrid = HRID(elements=('adjective', 'animal', 'verb'))
print(hrid.generate())  # e.g., "brave-tiger-jump"

# Use custom delimiter
hrid = HRID(delimiter='_')
print(hrid.generate())  # e.g., "bright_sunrise_dance_quickly"

# Use a seed for reproducibility
hrid = HRID(seed=42)
print(hrid.generate())  # Same output every time with same seed
```

### Nice Word Lists

Use curated word lists containing only positive/neutral words - ideal for user-facing IDs where you don't want potentially offensive or embarrassing combinations.

```python
from hrid import HRID, NICE_WORD_LISTS

hrid = HRID(word_lists=NICE_WORD_LISTS)
print(hrid.generate())  # e.g., "cheerful-maple-smile-gently"

# Nice word lists include additional categories
hrid = HRID(
    elements=('weather', 'fabric', 'place'),
    word_lists=NICE_WORD_LISTS
)
print(hrid.generate())  # e.g., "aurora-velvet-meadow"
```

### Available Word Types

**Standard word lists:**
| Type | Examples |
|------|----------|
| `adjective` | calm, bright, swift |
| `noun` | apple, river, mountain |
| `verb` | jump, dance, fly |
| `adverb` | quickly, gently, boldly |
| `animal` | tiger, eagle, dolphin |
| `flower` | rose, lily, daisy |
| `number` | 10-99 |

**Additional types in NICE_WORD_LISTS:**
| Type | Count | Examples |
|------|-------|----------|
| `place` | 158 | meadow, lighthouse, cottage, canyon |
| `tree` | 80 | oak, maple, willow, cedar, redwood |
| `weather` | 52 | aurora, rainbow, breeze, snowflake |
| `fabric` | 75 | velvet, cashmere, denim, silk |
| `mood` | 291 | cheerful, serene, enthusiastic |

### Custom Word Lists

You can provide your own word lists:

```python
from hrid import HRID

custom_lists = {
    'color': ['red', 'blue', 'green'],
    'size': ['big', 'small', 'tiny'],
    'animal': ['cat', 'dog', 'bird'],
}

hrid = HRID(
    elements=('color', 'size', 'animal'),
    word_lists=custom_lists
)
print(hrid.generate())  # e.g., "blue-tiny-cat"
```

## Why HRID?

* **Human friendly**: Comparing to UUID, hrid is extremely easy to remember. `red-bird-fly-crazily` versus `206dbaab-526b-41cd-aa6f-7febd82e83ab`
* **Low collision**: Over 800 billion combinations by default. With large numbers of IDs, this library has a very slim chance of collision.
* **Customizable**: Configure word types, delimiters, and even provide your own word lists.
* **Safe options**: Use `NICE_WORD_LISTS` for user-facing IDs to avoid awkward or offensive combinations.

## Requirements

Python 3.12+

## Credit
* [Dictionary Source](https://github.com/dariusk/corpora)
* [Inspired by Google API Design](https://cloud.google.com/blog/products/gcp/api-design-choosing-between-names-and-identifiers-in-urls)

## License

[MIT](./LICENSE)
