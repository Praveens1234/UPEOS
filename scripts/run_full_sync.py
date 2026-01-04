#!/usr/bin/env python3
"""
Runner script for full sync
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from upeos.scripts.full_sync import main

if __name__ == "__main__":
    main()