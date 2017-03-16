"""Adds directories to the type path
"""
import sys

from os.path import dirname, realpath, join
sys.path.insert(0, join(dirname(realpath(__file__)), r"wsdot-traffic-gp"))
