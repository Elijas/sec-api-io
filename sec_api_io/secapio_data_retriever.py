from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from concurrent.futures import ThreadPoolExecutor
import httpx
from sec_api_io.retry import retry_with_exponential_backoff
from sec_api_io.abstract_sec_data_retriever import (
    AbstractSECDataRetriever,
    DocumentTypeNotSupportedError,
)
from sec_api_io.sec_edgar_enums import (
    FORM_SECTIONS,
    SECTION_NAMES,
    DocumentType,
    SectionType,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

ACCESSION_NUMBER_LENGTH = 18


class ValueNotSetError(ValueError):
    pass


def get_value_or_env_var(
    value: str | None,
    env_var: str,
    default: str | None = None,
    exc: type[Exception] = ValueNotSetError,
) -> str:
    value = (value or "").strip()
    if value:
        return value

    env_value = os.environ.get(env_var, "").strip()
    if env_value:
        return env_value

    if default is not None:
        return default

    msg = f"No value provided and the environment variable '{env_var}' is also not set."
    raise exc(msg)


class SecapioApiKeyNotSetError(ValueError):
    pass


class SecapioApiKeyInvalidError(ValueError):
    pass


class SecapioRequestError(RuntimeError):
    pass


class SecapioDataRetriever(AbstractSECDataRetriever):
    """Retrieves data from sec-api.io API."""

    SUPPORTED_DOCUMENT_TYPES = frozenset({DocumentType.FORM_10Q})
    API_KEY_ENV_VAR_NAME = "SECAPIO_API_KEY"

    def __init__(
        self: SecapioDataRetriever,
        api_key: str | None = None,
        *,
        timeout_s: int | None = None,
    ) -> None:
        self._api_key = get_value_or_env_var(
            api_key,
            self.API_KEY_ENV_VAR_NAME,
            exc=SecapioApiKeyNotSetError,
        )
        self._timeout_s = timeout_s or 10

    def retrieve_report_metadata(
        self: SecapioDataRetriever,
        doc_type: DocumentType | str,
        *,
        accession_number: str | None = None,
        latest_from_ticker: str | None = None,
    ) -> dict:
        # Validate arguments
        if not accession_number and not latest_from_ticker:
            msg = "either url or ticker must be provided"
            raise ValueError(msg)
        if accession_number and latest_from_ticker:
            msg = "only one of accession_number or ticker must be provided"
            raise ValueError(msg)
        new_doc_type = (
            DocumentType.from_str(doc_type) if isinstance(doc_type, str) else doc_type
        )
        if new_doc_type not in self.SUPPORTED_DOCUMENT_TYPES:
            msg = f"Document type {doc_type} not supported."
            raise DocumentTypeNotSupportedError(msg)

        # Retrieve metadata
        metadata = None
        if latest_from_ticker:
            metadata = self._call_latest_report_metadata_api(
                new_doc_type,
                key="ticker",
                value=latest_from_ticker,
            )
        if accession_number:
            accession_number = _extract_accession_number(accession_number)
            metadata = self._call_latest_report_metadata_api(
                new_doc_type,
                key="accessionNo",
                value=accession_number,
            )
        if not metadata:
            msg = "metadata is None"
            raise RuntimeError(msg)
        return metadata

    def _get_report_html(
        self: SecapioDataRetriever,
        doc_type: DocumentType,
        url: str,
        *,
        sections: Iterable[SectionType] | None = None,
        use_multithreading: bool = False,
        workers: int = 1,
    ) -> str:
        assert workers>=1, "workers cannot be less than 1."
        if workers>1:
            assert use_multithreading, "when workers are greater than 1, use_multithreading must be True."
        if (not use_multithreading) or (workers==1) :
            html_parts = []
            sections = sections or FORM_SECTIONS[doc_type]
            for section in sections:
                title = SECTION_NAMES[section]
                title = re.sub(r"[^a-zA-Z0-9' ]+", "", title)
                separator_html = (
                    "<top-level-section-start-marker"
                    f' id="{section.value}"'
                    f' title="{title}"'
                    ' comment="This tag was added by '
                    'sec-api-io library based on sec-api.io API"'
                    ' style="display: none;"'
                    "</top-level-section-start-marker>"
                )
                html_parts.append(separator_html)
                section_html = self._call_sections_extractor_api(
                    url,
                    section,
                )
                html_parts.append(section_html)
            return "\n".join(html_parts)
        else:
            return self._get_report_html_with_multithreading(doc_type, url, sections=sections, num_workers=workers)

    def _get_report_html_with_multithreading(
        self: SecapioDataRetriever,
        doc_type: DocumentType,
        url: str,
        *,
        sections: Iterable[SectionType] | None = None,
        num_workers: int = 6
    ):
        html_parts = []
        sections = sections or FORM_SECTIONS[doc_type]
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            section_htmls = list(executor.map(lambda section: self._call_sections_extractor_api(url, section), sections))
        for section, section_html in zip(sections, section_htmls):
            title = re.sub(r"[^a-zA-Z0-9' ]+", "", SECTION_NAMES[section])
            separator_html = (
                "<top-level-section-start-marker"
                f' id="{section.value}"'
                f' title="{title}"'
                ' comment="This tag was added by '
                'sec-api-io library based on sec-api.io API"'
                ' style="display: none;"'
                "</top-level-section-start-marker>"
            )
            html_parts.append(separator_html)
            html_parts.append(section_html)
        return "\n".join(html_parts)

    @retry_with_exponential_backoff
    def _call_sections_extractor_api(
        self: SecapioDataRetriever,
        url: str,
        section: SectionType,
    ) -> str:
        params = {
            "url": url,
            "item": section.value,
            "type": "html",
            "token": self._api_key,
        }
        response = httpx.get(
            "https://api.sec-api.io/extractor",
            timeout=self._timeout_s,
            params=params,
        )
        response.raise_for_status()
        return response.text

    def _call_latest_report_metadata_api(
        self: SecapioDataRetriever,
        doc_type: DocumentType,
        *,
        key: str,
        value: str,
    ) -> dict:
        key = key.strip()
        value = value.strip()
        query = {
            "query": {
                "query_string": {
                    "query": f'{key}:"{value}" AND formType:"{doc_type.value}"',
                },
            },
            "from": "0",
            "size": "1",
            "sort": [{"filedAt": {"order": "desc"}}],
        }

        client = httpx.Client()
        try:
            res = client.post(
                f"https://api.sec-api.io?token={self._api_key}",
                json=query,
            )
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == httpx.codes.FORBIDDEN:
                msg = "Invalid API key."
                raise SecapioApiKeyInvalidError(msg) from e
            msg = f"HTTP Status Error occurred while making the request: {e!s}"
            raise SecapioRequestError(msg) from e
        except httpx.RequestError as e:
            msg = f"An unexpected error occurred while making the request: {e!s}"
            raise SecapioRequestError(msg) from e

        filings = res.json()["filings"]
        if len(filings) == 0:
            msg = f'no {doc_type.value} found for {key}="{value}"'
            raise SecapioRequestError(msg)
        if not isinstance(filings[0], dict):
            msg = f"expected a dict, got {type(filings[0])}"
            raise SecapioRequestError(msg)
        return filings[0]


def _extract_accession_number(url: str) -> str:
    numbers = re.findall(r"\d+", url)
    s = max(numbers, key=len)
    if len(s) != ACCESSION_NUMBER_LENGTH:
        msg = "Input string must be 18 characters long"
        raise ValueError(msg)
    result = s[:10] + "-" + s[10:12] + "-" + s[12:]
    if not isinstance(result, str):
        msg = f"expected a str, got {type(result)}"
        raise TypeError(msg)
    return result
