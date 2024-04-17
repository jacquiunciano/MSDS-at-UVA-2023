import fitz
import pandas as pd
import sys
from collections import Counter
import os
from glob import glob

class Convert():
    '''
    Converts the collection from their source formats (F0) into a set of tables that conform to the Standard Text Analytic Data Model (F2).
    '''