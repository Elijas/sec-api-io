import os
import pytest
from dotenv import load_dotenv
from httpx._exceptions import HTTPStatusError
from sec_api_io.secapio_data_retriever import SecapioDataRetriever
from sec_api_io.sec_edgar_enums import DocumentType


@pytest.fixture
def url_10k():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087222000026/a-20221031.htm'

@pytest.fixture
def url_10k_wrong():
    return 'https://www.sec.gov/Archives/edgar/data/1090872/000109087222111111/a-20221031.htm'

@pytest.fixture
def url_10k_expected_html():
    with open('tests/A.000109087222000026.result.htm', 'r') as f:
        expected_html = f.read()
    return expected_html

@pytest.fixture
def retriever():
    return SecapioDataRetriever(api_key=os.environ['SECAPIO_API_KEY'])

def test_api_key():
    assert load_dotenv()
    assert 'SECAPIO_API_KEY' in os.environ

def test_get_report_html(retriever, url_10k, url_10k_expected_html):
    actual_html = retriever.get_report_html('10-K', url_10k)
    assert actual_html==url_10k_expected_html

def test_get_report_html_multithreading(retriever, url_10k, url_10k_expected_html):
    actual_html = retriever.get_report_html('10-K', url_10k, use_multithreading=True, workers=10)
    assert actual_html==url_10k_expected_html

def test_get_report_html_wrong_url(retriever, url_10k_wrong, url_10k_expected_html):
    with pytest.raises(HTTPStatusError):
        actual_html = retriever.get_report_html('10-K', url_10k)
