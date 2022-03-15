"""Add src to sys path"""
import pathlib
import sys
DIR_MODULE = pathlib.Path(__file__).parents[1] / "src"
sys.path.append(str(DIR_MODULE))