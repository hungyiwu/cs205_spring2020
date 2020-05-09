#!/bin/sh
time spark-submit speed_test.py ./fake_1e2 2>/dev/null 1>/dev/null
time spark-submit speed_test.py ./fake_1e3 2>/dev/null 1>/dev/null
time spark-submit speed_test.py ./fake_1e4 2>/dev/null 1>/dev/null
