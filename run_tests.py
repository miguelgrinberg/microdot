import sys

sys.path.insert(0, 'src')
sys.path.insert(2, 'libs/common')
sys.path.insert(3, 'libs/micropython')

import unittest

if not unittest.main('tests').wasSuccessful():
    sys.exit(1)
