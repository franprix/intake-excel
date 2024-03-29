from intake.source import base

class ExcelSource(base.DataSource):
    """Read Excel files into dataframes

    Prototype of sources reading dataframe data

    """
    name = 'excel'
    version = '0.0.1'
    container = 'dataframe'
    partition_access = False

    def __init__(self, urlpath, compression_method=None, excel_kwargs=None, metadata=None):
        """
        Parameters
        ----------
        urlpath : str or iterable, location of data
            May be a local path, or remote path if including a protocol specifier
            such as ``'s3://'``. May include glob wildcards or format pattern strings.
        compression_method : str
            Either 'zip' or 'gzip' if data is compressed. At the moment Excel files
            in zipped archives are concatenated in a single dataframe.
        excel_kwargs : dict
            Any further arguments to pass to pandas read_excel
        """
        self.urlpath = urlpath
        self._compression_method = compression_method
        self._excel_kwargs = excel_kwargs or {}
        self._dataframe = None

        super(ExcelSource, self).__init__(metadata=metadata)

    def _open_dataset(self, urlpath):
        """Decompress if necessary and open dataset using pandas
        """
        import pandas as pd

        if self._compression_method in ('gzip', 'zlib', 'bz2'):
            self._dataframe = self._read_single_compressed(urlpath)
        elif self._compression_method == 'zip':
            self._dataframe = self._read_zip(urlpath)
        elif self._compression_method == None:
            self._dataframe = pd.read_excel(urlpath, **self._excel_kwargs)
        else:
            raise KeyError("Unsupported compression method {}".format(self._compression_method))

    def _get_schema(self):
        urlpath = self._get_cache(self.urlpath)[0]

        if self._dataframe is None:
            self._open_dataset(urlpath)

        dtypes = self._dataframe.dtypes.to_dict()
        dtypes = {n: str(t) for (n, t) in dtypes.items()}
        return base.Schema(datashape=None,
                           dtype=dtypes,
                           shape=(None, len(dtypes)),
                           npartitions=1,
                           extra_metadata={})

    def _get_partition(self, _):
        if self._dataframe is None:
            self._load_metadata()
        return self._dataframe

    def read(self):
        return self._get_partition(None)

    def _close(self):
        self._dataframe = None
  
    def _read_zip(self, urlpath):
        from zipfile import ZipFile
        from io import StringIO, BytesIO
        from urllib.request import urlopen
        import pandas as pd
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        resp = urlopen(urlpath, context=ctx)
        zipfile = ZipFile(BytesIO(resp.read()))

        lst = list()

        for name in zipfile.namelist():
            foofile = zipfile.open(name)
            df_ = pd.read_excel(foofile, **self._excel_kwargs)
            lst.append(df_)

        df = pd.concat(lst)

        return df

    def _read_gzip(self, urlpath):
        import pandas as pd

        resp = urlopen(urlpath)
        gzipfile = gzip.open(BytesIO(resp.read()))

        df = pd.read_excel(gzipfile.read(), **self._excel_kwargs)

        return df
