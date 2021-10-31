from posixpath import dirname
from mafio import MAFReader
from os.path import join
import pytest


class TestMAFReader:
    @pytest.fixture(autouse=True)
    def filespath(self):
        return {
            "gzip": join(dirname(__file__), "data", "test_data.maf.gz"),
            "default": join(dirname(__file__), "data", "test_data.maf")
        }

    def test_compressed(self, filespath):
        iter = MAFReader(filespath["gzip"], compression="gzip").read()
        data = next(iter)
        assert len(data) == 6
        assert len(data[0]) == 114

    def test_decompressed(self, filespath):
        iter = MAFReader(filespath["default"], compression=None).read()
        data = next(iter)
        assert len(data) == 6
        assert len(data[0]) == 114

    def test_chunk_read(self, filespath):
        CHUNK = 4
        iter = MAFReader(filespath["gzip"], compression="gzip").read(CHUNK)
        assert len(next(iter)) == 4
        assert len(next(iter)) == 2
        with pytest.raises(StopIteration):
            next(iter)
    def test_single_chunk_read(self, filespath):
        CHUNK = 1
        iter = MAFReader(filespath["gzip"], compression="gzip").read(CHUNK)
        [next(iter) for _ in range(6)]
        with pytest.raises(StopIteration):
            next(iter)

    def test_chunk_cols_read(self, filespath):
        CHUNK = 4
        cols = ["Hugo_Symbol", "Entrez_Gene_Id", "CENTERS", "NCALLERS"]
        iter = MAFReader(filespath["gzip"],
                         compression="gzip").read(CHUNK, cols)
        assert len(next(iter)[0]) == len(cols)
        assert len(next(iter)[0]) == len(cols)

    def test_bulk_read(self, filespath):
        iter = MAFReader(filespath["gzip"], compression="gzip").read()
        assert len(next(iter)) == 6

    def test_bulk_cols_read(self, filespath):
        cols = ["Hugo_Symbol", "Entrez_Gene_Id", "CENTERS", "NCALLERS"]
        iter = MAFReader(filespath["gzip"],
                         compression="gzip").read(use_cols=cols)
        assert len(next(iter)[0]) == len(cols)
