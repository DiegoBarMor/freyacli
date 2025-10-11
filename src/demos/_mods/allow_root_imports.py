### simulate having "freyacli" installed as a package
### this way it's not necessary to install the repo to run these demos
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
