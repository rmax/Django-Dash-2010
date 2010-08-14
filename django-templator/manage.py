#!/usr/bin/env python
import os
import sys

from django.core.management import execute_manager

try:
    import templator
except ImportError:
    sys.path.insert(os.path.dirname(os.path.realpath(__file__)))

    try:
        import templator
    except ImportError:
        sys.stderr.write("Error: Can't import project 'templator'")
        sys.exit(1)

try:
    from templator.conf.local import settings
except ImportError:
    try:
        from templator.conf import settings
    except ImportError:
        sys.stderr.write("Error: Can't import 'settings'")
        sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
