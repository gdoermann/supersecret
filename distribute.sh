#!/bin/bash

# Upload to pypi
# Usage: ./distribute.sh

python -m build && \
twine upload --repository pypi dist/*