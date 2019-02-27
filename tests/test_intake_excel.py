import pandas as pd

import intake
from intake_excel import ExcelSource

from .utils import temp_plain_excel, df

def test_fixture(temp_plain_excel):
    d2 = pd.read_excel('temp_plain_excel.xlsx')
    assert df.equals(d2)

def test_simple(temp_plain_excel):
    d2 = ExcelSource('temp_plain_excel.xlsx').read()
    assert df.equals(d2)
