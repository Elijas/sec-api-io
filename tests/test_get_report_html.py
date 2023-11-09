import os
import pytest
from dotenv import load_dotenv
from sec_api_io.secapio_data_retriever import SecapioDataRetriever
from sec_api_io.sec_edgar_enums import DocumentType


@pytest.fixture
def url_10q():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087216000070/a-04302016x10q.htm'

@pytest.fixture
def url_10q_expected_html():
    with open('tests/A.000109087216000070.result.htm', 'r') as f:
        expected_html = f.read()
    return expected_html

@pytest.fixture
def retriever():
    return SecapioDataRetriever(api_key=os.environ['SECAPIO_API_KEY'])

def test_api_key():
    assert load_dotenv()
    assert 'SECAPIO_API_KEY' in os.environ

def test_get_report_html(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q)
    assert actual_html==url_10q_expected_html

def test_get_report_html_with_multithreading_and_one_worker(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True)
    assert actual_html==url_10q_expected_html

def test_get_report_html_with_multithreading_and_negative_worker(retriever, url_10q, url_10q_expected_html):
    with pytest.raises(AssertionError, match='workers cannot be less than 1.'):
        actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True, workers=-1)

def test_get_report_html_with_multithreading_only_worker(retriever, url_10q, url_10q_expected_html):
    with pytest.raises(AssertionError, match='when workers are greater than 1, use_multithreading must be True.'):
        actual_html = retriever.get_report_html('10-Q', url_10q, workers=4)

def test_get_report_html_with_multithreading_and_custom_workers(retriever, url_10q, url_10q_expected_html):
    actual_html = retriever.get_report_html('10-Q', url_10q, use_multithreading=True, workers=11)
    assert actual_html==url_10q_expected_html