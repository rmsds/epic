import pytest
from collections import OrderedDict

import pandas as pd
from io import StringIO


from epic.merge.merge import merge_matrixes
from epic.merge.merge_helpers import add_new_enriched_bins_matrixes


@pytest.fixture
def regions(tmpdir):

    fs = []
    for i, c in enumerate(["""chr1    10000   10599   2.2761062711783457e-05  67.49046260339546       .
chr1    72000   91599   2.4770408905838545e-226 235.4664881299362       .""",
           """chr1    9800    15199   0.0048446172754557214   33.652547110032025      .
chr1    40000   41199   2.187570707966001e-08   1000.0  .""",
           """chr1    9800    10599   3.239383152206723e-79   204.30687218918862      .
chr1    38800   40799   2.4798100382025985e-11  1000.0  ."""]):

        name = str(i)
        f = tmpdir.mkdir(name).join(name)
        f.write(c)
        fs.append(str(f))

    return fs


@pytest.fixture
def dfs():

    od = OrderedDict()

    for n, c in [("fibroblast.matrix.gz","""Chromosome Bin Enriched_fibroblast chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/ChIP_3_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz chrX/Input_3_fibroblast.bed.gz
chr1 10000 1 4 14 13 2 4 14
chr1 10200 1 17 24 14 9 9 16
chr1 10400 1 3 1 1 1 0 2
chr1 11400 1 0 0 1 0 0 0
chr1 11600 1 0 0 0 0 0 0
chr1 11800 1 1 0 1 0 0 0
chr1 12000 1 0 0 0 0 0 0
chr1 12200 1 0 0 1 0 0 0
chr1 12400 1 0 0 0 0 0 0
chr1 12600 1 0 0 0 1 0 0
chr1 12800 1 0 0 0 0 0 0
chr1 13000 1 3 6 4 1 3 2
chr1 13200 1 0 1 0 1 1 0
chr1 13400 1 7 4 5 1 1 3
chr1 13600 1 0 0 0 0 0 0
chr1 13800 1 0 0 1 0 0 0
chr1 14000 1 0 0 0 0 0 0
chr1 14200 1 0 0 0 0 0 0
chr1 14400 1 0 0 0 0 0 0"""),
("keratinocyte.matrix.gz", """Chromosome Bin Enriched_keratinocyte chrX/ChIP_1_keratinocyte.bed.gz chrX/ChIP_2_keratinocyte.bed.gz chrX/ChIP_3_keratinocyte.bed.gz chrX/Input_1_keratinocyte.bed.gz chrX/Input_2_keratinocyte.bed.gz chrX/Input_3_keratinocyte.bed.gz
chr1 9800 1 1 0 0 2 0 0
chr1 10000 1 13 15 17 11 2 17
chr1 10200 1 13 25 23 16 2 24
chr1 10400 1 2 0 2 10 0 3
chr1 10600 1 0 0 0 0 0 0
chr1 10800 1 0 0 1 0 0 0
chr1 11000 1 0 0 0 0 0 0
chr1 11200 1 0 0 0 0 0 0
chr1 11400 1 0 0 0 0 0 0
chr1 11600 1 0 0 1 0 0 0
chr1 11800 1 0 0 0 0 0 0
chr1 12000 1 0 0 2 0 0 0
chr1 12200 1 0 0 0 0 0 0
chr1 12400 1 0 0 0 0 0 0
chr1 12600 1 0 0 0 0 0 1
chr1 12800 1 0 1 1 0 0 0
chr1 13000 1 0 0 6 7 1 3
chr1 13200 1 0 2 0 2 1 1
chr1 13400 1 1 1 6 4 0 2"""),
        ("melanocyte.matrix.gz", """Chromosome Bin Enriched_melanocyte chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/ChIP_3_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz chrX/Input_3_melanocyte.bed.gz
chr1 9800 1 0 0 2 0 0 0
chr1 10000 1 13 3 128 2 2 21
chr1 10200 1 15 8 96 5 3 23
chr1 10400 1 3 0 4 3 0 7
chr1 11800 0 1 0 0 0 0 0
chr1 12000 0 0 0 0 0 0 4
chr1 12200 0 0 0 0 0 0 1
chr1 12400 0 0 1 0 0 0 1
chr1 12600 0 1 0 0 0 0 0
chr1 13000 0 5 3 1 0 0 2
chr1 13200 0 1 3 0 0 0 1
chr1 13400 0 3 0 3 1 0 3
chr1 13800 0 1 0 0 0 0 0
chr1 14600 0 1 0 1 0 0 0
chr1 14800 0 1 0 4 1 0 4
chr1 15000 0 1 0 1 1 0 2
chr1 15600 0 0 1 0 0 0 1
chr1 15800 0 1 0 0 0 0 0
chr1 16000 0 1 1 2 1 2 2""")]:
        df = pd.read_table(StringIO(c), sep="\s+", header=0, index_col=[0, 1])
        od[n] = df

    return od


def test_add_regions(regions, dfs, expected_result):

    result = add_new_enriched_bins_matrixes(regions, dfs, 200)

    for (kr, vr), (kx, vx) in zip(result.items(), expected_result.items()):
        print(kr, kx)
        print(vr.to_csv(sep=" "))
        print(vx.to_csv(sep=" "))

        assert vr.equals(vx)



@pytest.fixture
def simple_dfs():

    od = OrderedDict()

    for n, c in [("melanocyte.matrix", """Chromosome Bin Enriched_melano chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz
chr1 800 1 0 2 0 0
chr1 1200 1 13 128 2 2"""),
                 ("fibroblast.matrix", """Chromosome Bin Enriched_fibro chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz
chr1 800 1 0 2 0 0
chr1 1200 1 13 128 2 2""")]:

        df = pd.read_table(StringIO(c), sep="\s+", header=0, index_col=[0, 1])
        od[n] = df

    return od


@pytest.fixture
def simple_regions(tmpdir):

    fs = []
    for n, c in zip(["melanocyte", "fibroblast"],
            ["""chr1	600	1200	2.2761062711783457e-05	67.49046260339546	.""",
            """chr1	200	1600	0.0048446172754557214	33.652547110032025	."""]):

        name = n
        f = tmpdir.mkdir(name).join(name)
        f.write(c)
        fs.append(str(f))

    return fs


@pytest.fixture
def simple_expected_result():

    melano = """Chromosome Bin chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz Enriched_melanocyte
chr1 200 0.0 0.0 0.0 0.0 0.0
chr1 400 0.0 0.0 0.0 0.0 0.0
chr1 600 0.0 0.0 0.0 0.0 1.0
chr1 800 0.0 2.0 0.0 0.0 1.0
chr1 1000 0.0 0.0 0.0 0.0 1.0
chr1 1200 13.0 128.0 2.0 2.0 1.0
chr1 1400 0.0 0.0 0.0 0.0 0.0
chr1 1600 0.0 0.0 0.0 0.0 0.0"""

    fibro = """Chromosome Bin chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz Enriched_fibroblast
chr1 200 0.0 0.0 0.0 0.0 1
chr1 400 0.0 0.0 0.0 0.0 1
chr1 600 0.0 0.0 0.0 0.0 1
chr1 800 0.0 2.0 0.0 0.0 1
chr1 1000 0.0 0.0 0.0 0.0 1
chr1 1200 13.0 128.0 2.0 2.0 1
chr1 1400 0.0 0.0 0.0 0.0 1
chr1 1600 0.0 0.0 0.0 0.0 1"""

    od = OrderedDict()
    od["melano"] = pd.read_table(StringIO(melano), sep="\s+", index_col=[0, 1])

    od["fibro"] = pd.read_table(StringIO(fibro), sep="\s+", index_col=[0, 1])

    return od


def test_simple_add_regions(simple_dfs, simple_regions, simple_expected_result):

    result = add_new_enriched_bins_matrixes(simple_regions, simple_dfs, 200)

    for (k, v), (k2, x) in zip(result.items(), simple_expected_result.items()):
        print(k, k2)
        print(x.to_csv(sep=" "))
        print(v.to_csv(sep=" "))

        assert x.equals(v)


@pytest.fixture
def expected_melano():

    c = """Chromosome Bin chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/ChIP_3_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz chrX/Input_3_melanocyte.bed.gz Enriched_2
chr1 9800 0.0 0.0 2.0 0.0 0.0 0.0 1.0
chr1 10000 13.0 3.0 128.0 2.0 2.0 21.0 1.0
chr1 10200 15.0 8.0 96.0 5.0 3.0 23.0 1.0
chr1 10400 3.0 0.0 4.0 3.0 0.0 7.0 1.0
chr1 10600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 10800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11800 1.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12000 0.0 0.0 0.0 0.0 0.0 4.0 0.0
chr1 12200 0.0 0.0 0.0 0.0 0.0 1.0 0.0
chr1 12400 0.0 1.0 0.0 0.0 0.0 1.0 0.0
chr1 12600 1.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13000 5.0 3.0 1.0 0.0 0.0 2.0 0.0
chr1 13200 1.0 3.0 0.0 0.0 0.0 1.0 0.0
chr1 13400 3.0 0.0 3.0 1.0 0.0 3.0 0.0
chr1 13600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13800 1.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14600 1.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 14800 1.0 0.0 4.0 1.0 0.0 4.0 0.0
chr1 15000 1.0 0.0 1.0 1.0 0.0 2.0 0.0
chr1 15600 0.0 1.0 0.0 0.0 0.0 1.0 0.0
chr1 15800 1.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 16000 1.0 1.0 2.0 1.0 2.0 2.0 0.0
chr1 38800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 39000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 39200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 39400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 39600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 39800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 41000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91400 0.0 0.0 0.0 0.0 0.0 0.0 0.0"""

    return pd.read_table(StringIO(c), sep=" ", index_col=[0, 1])

@pytest.fixture
def expected_keratino():

    c = """Chromosome Bin chrX/ChIP_1_keratinocyte.bed.gz chrX/ChIP_2_keratinocyte.bed.gz chrX/ChIP_3_keratinocyte.bed.gz chrX/Input_1_keratinocyte.bed.gz chrX/Input_2_keratinocyte.bed.gz chrX/Input_3_keratinocyte.bed.gz Enriched_1
chr1 9800 1.0 0.0 0.0 2.0 0.0 0.0 1.0
chr1 10000 13.0 15.0 17.0 11.0 2.0 17.0 1.0
chr1 10200 13.0 25.0 23.0 16.0 2.0 24.0 1.0
chr1 10400 2.0 0.0 2.0 10.0 0.0 3.0 1.0
chr1 10600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 10800 0.0 0.0 1.0 0.0 0.0 0.0 1.0
chr1 11000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 11200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 11400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 11600 0.0 0.0 1.0 0.0 0.0 0.0 1.0
chr1 11800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 12000 0.0 0.0 2.0 0.0 0.0 0.0 1.0
chr1 12200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 12400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 12600 0.0 0.0 0.0 0.0 0.0 1.0 1.0
chr1 12800 0.0 1.0 1.0 0.0 0.0 0.0 1.0
chr1 13000 0.0 0.0 6.0 7.0 1.0 3.0 1.0
chr1 13200 0.0 2.0 0.0 2.0 1.0 1.0 1.0
chr1 13400 1.0 1.0 6.0 4.0 0.0 2.0 1.0
chr1 13600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 13800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 14000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 14200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 14400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 14600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 14800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 15000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 38800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 40800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 41000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 72000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 73800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 74800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 75800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 76800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 77800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 78800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 79800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 80800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 81800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 82800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 83800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 84800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 85800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 86800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 87800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 88800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 89800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 90800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 91400 0.0 0.0 0.0 0.0 0.0 0.0 0.0"""

    return pd.read_table(StringIO(c), sep=" ", index_col=[0, 1])

@pytest.fixture
def expected_fibro():

    c = """Chromosome Bin chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/ChIP_3_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz chrX/Input_3_fibroblast.bed.gz Enriched_0
chr1 9800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 10000 4.0 14.0 13.0 2.0 4.0 14.0 1.0
chr1 10200 17.0 24.0 14.0 9.0 9.0 16.0 1.0
chr1 10400 3.0 1.0 1.0 1.0 0.0 2.0 1.0
chr1 10600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 10800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11400 0.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 11600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11800 1.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 12000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12200 0.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 12400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12600 0.0 0.0 0.0 1.0 0.0 0.0 0.0
chr1 12800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13000 3.0 6.0 4.0 1.0 3.0 2.0 0.0
chr1 13200 0.0 1.0 0.0 1.0 1.0 0.0 0.0
chr1 13400 7.0 4.0 5.0 1.0 1.0 3.0 0.0
chr1 13600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13800 0.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 14000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 15000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 38800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 39800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40200 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40400 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40600 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 40800 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 41000 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 72000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 72200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 72400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 72600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 72800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 73000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 73200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 73400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 73600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 73800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 74000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 74200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 74400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 74600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 74800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 75000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 75200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 75400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 75600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 75800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 76000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 76200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 76400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 76600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 76800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 77000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 77200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 77400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 77600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 77800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 78000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 78200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 78400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 78600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 78800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 79000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 79200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 79400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 79600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 79800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 80000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 80200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 80400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 80600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 80800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 81000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 81200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 81400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 81600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 81800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 82000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 82200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 82400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 82600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 82800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 83000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 83200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 83400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 83600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 83800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 84000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 84200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 84400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 84600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 84800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 85000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 85200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 85400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 85600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 85800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 86000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 86200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 86400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 86600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 86800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 87000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 87200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 87400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 87600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 87800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 88000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 88200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 88400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 88600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 88800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 89000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 89200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 89400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 89600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 89800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 90000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 90200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 90400 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 90600 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 90800 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 91000 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 91200 0.0 0.0 0.0 0.0 0.0 0.0 1.0
chr1 91400 0.0 0.0 0.0 0.0 0.0 0.0 1.0"""

    return pd.read_table(StringIO(c), sep=" ", index_col=[0, 1])


@pytest.fixture
def expected_result(expected_fibro, expected_keratino, expected_melano):

    od = OrderedDict()

    od["fibro"] = expected_fibro
    od["keratino"] = expected_keratino
    od["melano"] = expected_melano

    return od
