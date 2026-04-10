#!/bin/bash
set -eu

### Re-install the package locally

pip uninstall freyacli -y || true
pip install .
rm -rf build freyacli.egg-info
