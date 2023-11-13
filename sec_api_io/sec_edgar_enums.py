from __future__ import annotations

from enum import Enum

from frozendict import frozendict


class DocumentType(Enum):
    INVALID_DOCUMENT_TYPE = (
        "INVALID"  # Placeholder for invalid or unimplemented document types
    )
    FORM_10Q = "10-Q"
    FORM_10K = "10-K"

    @staticmethod
    def from_str(s: str) -> DocumentType:
        try:
            return DocumentType(s.strip().upper())
        except ValueError as e:
            msg = f"Invalid document type {s}"
            raise InvalidDocumentTypeError(msg) from e


class SectionType(Enum):
    INVALID_SECTION_TYPE = (
        "INVALID"  # Placeholder for invalid or unimplemented document types
    )
    # Related to 10-Q
    FORM_10Q_PART1ITEM1 = "part1item1"
    FORM_10Q_PART1ITEM2 = "part1item2"
    FORM_10Q_PART1ITEM3 = "part1item3"
    FORM_10Q_PART1ITEM4 = "part1item4"
    FORM_10Q_PART2ITEM1 = "part2item1"
    FORM_10Q_PART2ITEM1A = "part2item1a"
    FORM_10Q_PART2ITEM2 = "part2item2"
    FORM_10Q_PART2ITEM3 = "part2item3"
    FORM_10Q_PART2ITEM4 = "part2item4"
    FORM_10Q_PART2ITEM5 = "part2item5"
    FORM_10Q_PART2ITEM6 = "part2item6"
    # Related to 10-K
    FORM_10K_1 = '1'
    FORM_10K_1A = '1A'
    FORM_10K_1B = '1B'
    FORM_10K_2 = '2'
    FORM_10K_3 = '3'
    FORM_10K_4 = '4'
    FORM_10K_5 = '5'
    FORM_10K_6 = '6'
    FORM_10K_7 = '7'
    FORM_10K_7A = '7A'
    FORM_10K_8 = '8'
    FORM_10K_9 = '9'
    FORM_10K_9A = '9A'
    FORM_10K_9B = '9B'
    FORM_10K_10 = '10'
    FORM_10K_11 = '11'
    FORM_10K_12 = '12'
    FORM_10K_13 = '13'
    FORM_10K_14 = '14'
    FORM_10K_15 = '15' # Note: No information provided about `15` in sec-api.io docs (https://sec-api.io/docs/sec-filings-item-extraction-api).

    @staticmethod
    def from_str(s: str) -> SectionType:
        try:
            return SectionType(s.strip().lower())
        except ValueError as e:
            msg = f"Invalid section {s}"
            raise InvalidSectionTypeError(msg) from e

    @property
    def name(self) -> str:
        return SECTION_NAMES.get(self, "Unknown Section")


class InvalidDocumentTypeError(ValueError):
    pass


class InvalidSectionTypeError(ValueError):
    pass


FORM_SECTIONS = frozendict(
    {
        DocumentType.FORM_10Q: [
            SectionType.FORM_10Q_PART1ITEM1,
            SectionType.FORM_10Q_PART1ITEM2,
            SectionType.FORM_10Q_PART1ITEM3,
            SectionType.FORM_10Q_PART1ITEM4,
            SectionType.FORM_10Q_PART2ITEM1,
            SectionType.FORM_10Q_PART2ITEM1A,
            SectionType.FORM_10Q_PART2ITEM2,
            SectionType.FORM_10Q_PART2ITEM3,
            SectionType.FORM_10Q_PART2ITEM4,
            SectionType.FORM_10Q_PART2ITEM5,
            SectionType.FORM_10Q_PART2ITEM6,
        ],
        DocumentType.FORM_10K: [
            SectionType.FORM_10K_1,
            SectionType.FORM_10K_1A,
            SectionType.FORM_10K_1B,
            SectionType.FORM_10K_2,
            SectionType.FORM_10K_3,
            SectionType.FORM_10K_4,
            SectionType.FORM_10K_5,
            SectionType.FORM_10K_6,
            SectionType.FORM_10K_7,
            SectionType.FORM_10K_7A,
            SectionType.FORM_10K_8,
            SectionType.FORM_10K_9,
            SectionType.FORM_10K_9A,
            SectionType.FORM_10K_9B,
            SectionType.FORM_10K_10,
            SectionType.FORM_10K_11,
            SectionType.FORM_10K_12,
            SectionType.FORM_10K_13,
            SectionType.FORM_10K_14,
            SectionType.FORM_10K_15,
        ],
    },
)

SECTION_NAMES = frozendict(
    {
        # Related to 10-Q
        SectionType.FORM_10Q_PART1ITEM1: "Financial Statements",
        SectionType.FORM_10Q_PART1ITEM2: "Management's Discussion and Analysis of Financial Condition and Results of Operations",  # noqa: E501
        SectionType.FORM_10Q_PART1ITEM3: "Quantitative and Qualitative Disclosures About Market Risk",  # noqa: E501
        SectionType.FORM_10Q_PART1ITEM4: "Controls and Procedures",
        SectionType.FORM_10Q_PART2ITEM1: "Legal Proceedings",
        SectionType.FORM_10Q_PART2ITEM1A: "Risk Factors",
        SectionType.FORM_10Q_PART2ITEM2: "Unregistered Sales of Equity Securities and Use of Proceeds",  # noqa: E501
        SectionType.FORM_10Q_PART2ITEM3: "Defaults Upon Senior Securities",
        SectionType.FORM_10Q_PART2ITEM4: "Mine Safety Disclosures",
        SectionType.FORM_10Q_PART2ITEM5: "Other Information",
        SectionType.FORM_10Q_PART2ITEM6: "Exhibits",
        # Related to 10-K
        SectionType.FORM_10K_1: "Business",
        SectionType.FORM_10K_1A: "Risk Factors",
        SectionType.FORM_10K_1B: "Unresolved Staff Comments",
        SectionType.FORM_10K_2: "Properties",
        SectionType.FORM_10K_3: "Legal Proceedings",
        SectionType.FORM_10K_4: "Mine Safety Disclosures",
        SectionType.FORM_10K_5: "Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities",
        SectionType.FORM_10K_6: "Selected Financial Data (prior to February 2021)",
        SectionType.FORM_10K_7: "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
        SectionType.FORM_10K_7A: "Quantitative and Qualitative Disclosures about Market Risk",
        SectionType.FORM_10K_8: "Financial Statements and Supplementary Data",
        SectionType.FORM_10K_9: "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure",
        SectionType.FORM_10K_9A: "Controls and Procedures",
        SectionType.FORM_10K_9B: "Other Information",
        SectionType.FORM_10K_10: "Directors, Executive Officers and Corporate Governance",
        SectionType.FORM_10K_11: "Executive Compensation",
        SectionType.FORM_10K_12: "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters",
        SectionType.FORM_10K_13: "Certain Relationships and Related Transactions, and Director Independence",
        SectionType.FORM_10K_14: "Principal Accountant Fees and Services",
        SectionType.FORM_10K_15: "Section 15 of a 10-K filing", # Note: No information provided about ID `15` in sec-api.io docs (https://sec-api.io/docs/sec-filings-item-extraction-api).
    },
)
