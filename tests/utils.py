import pandas as pd
import numpy as np
import pytest

df = pd.DataFrame({
    'a': np.random.rand(100),
    'b': np.random.randint(100),
    'c': np.random.choice(['a', 'b', 'c', 'd'], size=100)
})
# There is a floating point precision loss when writing a dataframe
# to an Excel file. To be able to properly test the package we
# round all floating point values to 6 decimals.
df.a = df.a.round(6)


@pytest.fixture(scope='module')
def temp_plain_excel():
    filename = 'temp_plain_excel.xlsx'
    df.to_excel(filename, float_format='%.6f', index=False)
