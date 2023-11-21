import os
from pathlib import Path
import pytest
import pandas as pd
from dotenv import load_dotenv
from sec_api_io.secapio_data_retriever import SecapioDataRetriever
from sec_api_io.sec_edgar_enums import DocumentType


@pytest.fixture
def url_10k():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087222000026/a-20221031.htm'

@pytest.fixture
def url_10k_wrong():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087222111111/a-20221031.htm'

@pytest.fixture
def url_10q():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087216000070/a-04302016x10q.htm'

@pytest.fixture
def url_10k_expected_html():
    with open('tests/data/A.000109087222000026.result.htm', 'r') as f:
        expected_html = f.read()
    return expected_html

@pytest.fixture
def url_10q_expected_html():
    with open('tests/data/A.000109087216000070.result.htm', 'r') as f:
        expected_html = f.read()
    return expected_html

@pytest.fixture
def test_metadata_8k():
    return pd.read_csv('tests/data/test_data_8k.csv')

@pytest.fixture
def retriever():
    return SecapioDataRetriever(api_key=os.environ['SECAPIO_API_KEY'])


def test_api_key():
    assert load_dotenv()
    assert 'SECAPIO_API_KEY' in os.environ

def test_get_report_html_10q(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q)
    assert actual_html==url_10q_expected_html

def test_get_report_html_10q_with_multithreading_and_one_worker(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True)
    assert actual_html==url_10q_expected_html

def test_get_report_html_10q_with_multithreading_and_negative_worker(retriever, url_10q, url_10q_expected_html):
    with pytest.raises(AssertionError, match='workers cannot be less than 1.'):
        actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True, workers=-1)

def test_get_report_html_10q_with_multithreading_only_worker(retriever, url_10q, url_10q_expected_html):
    with pytest.raises(AssertionError, match='when workers are greater than 1, use_multithreading must be True.'):
        actual_html = retriever.get_report_html('10-Q', url_10q, workers=4)

def test_get_report_html_10q_with_multithreading_and_custom_workers(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True, workers=11)
    assert actual_html==url_10q_expected_html

def test_get_report_html_10k(retriever, url_10k, url_10k_expected_html):
    actual_html = retriever.get_report_html('10-K', url_10k)
    assert actual_html==url_10k_expected_html

def test_get_report_html_10k_multithreading(retriever, url_10k, url_10k_expected_html):
    actual_html = retriever.get_report_html('10-K', url_10k, use_multithreading=True, workers=10)
    assert actual_html==url_10k_expected_html

def test_get_report_html_10k_wrong_url(retriever, url_10k_wrong, url_10k_expected_html):
    with pytest.raises(HTTPStatusError):
        actual_html = retriever.get_report_html('10-K', url_10k)

def test_get_report_html_8k(retriever, test_metadata_8k):
    item_col_map = {
        "Item:1.01": '1-1',
        'Item:1.02': '1-2',
        'Item:1.03': '1-3',
        'Item:1.04': '1-4',
        'Item:2.01': '2-1',
        'Item:2.02': '2-2',
        'Item:2.03': '2-3',
        'Item:2.04': '2-4',
        'Item:2.05': '2-5',
        'Item:2.06': '2-6',
        'Item:3.01': '3-1',
        'Item:3.02': '3-2',
        'Item:3.03': '3-3',
        'Item:4.01': '4-1',
        'Item:4.02': '4-2',
        'Item:5.01': '5-1',
        'Item:5.02': '5-2',
        'Item:5.03': '5-3',
        'Item:5.04': '5-4',
        'Item:5.05': '5-5',
        'Item:5.06': '5-6',
        'Item:5.07': '5-7',
        'Item:5.08': '5-8',
        'Item:6.02': '6-2',
        'Item:6.03': '6-3',
        'Item:6.04': '6-4',
        'Item:6.05': '6-5',
        'Item:7.01': '7-1',
        'Item:8.01': '8-1',
        'Item:9.01': '9-1',
    }
    item_cols = sorted(item_col_map.keys())
    for i, row in test_metadata_8k.iterrows():
        # Gather section IDs and URL
        ticker = row['ticker']
        url = row['linkToFilingDetails']
        accession_number = url.split('/data/')[1].split('/')[1]
        accession_number_with_dash = (
            accession_number[:10]
            + '-'
            + accession_number[10:12]
            + '-'
            + accession_number[12:]
        )
        url = url.replace('https://www.sec.gov/ix?doc=/', 'https://www.sec.gov/').replace('https://www.sec.gov/ix.xhtml?doc=/', 'https://www.sec.gov/')    
        section_ids = [item_col_map[c] for c in item_cols if row[c]] + ['signature']
        # Perform extraction
        actual_html = retriever.get_report_html('8-K', url, sections=section_ids, use_multithreading=True, workers=10)
        # Verify results
        doc_folder = Path('tests/data/8-K') / ticker / accession_number_with_dash
        with (doc_folder/'primary-document-secapio.htm').open('r') as f:
            expected_html = f.read()
        assert actual_html==expected_html

def test_get_report_html_8k_with_irrelevant_section(retriever):
    # Arrange
    section_ids = ['6-1']
    url_8k_without_61 = 'https://www.sec.gov/Archives/edgar/data/1837607/000110465923084851/tm2314948d1_8k.htm'
    expected_html = '''<top-level-section-start-marker id="6-1" title="ABS Informational and Computational Material" comment="This tag was added by sec-api-io library based on sec-api.io API" style="display: none;"</top-level-section-start-marker>
processing'''

    # Act
    actual_html = retriever.get_report_html('8-K', url_8k_without_61, sections=section_ids)

    # Assert
    assert expected_html==actual_html