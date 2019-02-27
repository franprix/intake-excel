import pandas as pd
import numpy as np
import pytest

df = pd.DataFrame({
    'a': np.random.rand(100),
    'b': np.random.randint(100),
    'c': np.random.choice(['a', 'b', 'c', 'd'], size=100)
})
df.index.name = 'p'


@pytest.fixture(scope='module')
def temp_plain_excel():
    filename = 'temp_plain_excel.xlsx'
    df.to_excel(filename)
