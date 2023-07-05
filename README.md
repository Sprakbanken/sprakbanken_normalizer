# Inverse text normalization for Norwegian ASR

Python module for inverse text normalization of Norwegian ASR output.

The module is primarily intended for internal use in Språkbanken.

## Installation
```git clone https://github.com/Sprakbanken/sprakbanken_normalizer.git

python -m pip install .```

## How to run
```
from sprakbanken_normalizer.inverse_text_normalizer import inv_normalize

print(inv_normalize("dette tallet er tre hundre tusen fire hundre og tjueto"))
```
