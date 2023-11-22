from __future__ import annotations

from enum import Enum

from frozendict import frozendict


class DocumentType(Enum):
    INVALID_DOCUMENT_TYPE = (
        "INVALID"  # Placeholder for invalid or unimplemented document types
    )
    FORM_10Q = "10-Q"
    FORM_10K = "10-K"
    FORM_8K = "8-K"

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
    FORM_10K_1 = "1"
    FORM_10K_1A = "1A"
    FORM_10K_1B = "1B"
    FORM_10K_2 = "2"
    FORM_10K_3 = "3"
    FORM_10K_4 = "4"
    FORM_10K_5 = "5"
    FORM_10K_6 = "6"
    FORM_10K_7 = "7"
    FORM_10K_7A = "7A"
    FORM_10K_8 = "8"
    FORM_10K_9 = "9"
    FORM_10K_9A = "9A"
    FORM_10K_9B = "9B"
    FORM_10K_10 = "10"
    FORM_10K_11 = "11"
    FORM_10K_12 = "12"
    FORM_10K_13 = "13"
    FORM_10K_14 = "14"
    FORM_10K_15 = "15" # Note: No information provided about `15` in sec-api.io docs (https://sec-api.io/docs/sec-filings-item-extraction-api).
    # Related to 8-K
    FORM_8K_11 = "1-1"
    FORM_8K_12 = "1-2"
    FORM_8K_13 = "1-3"
    FORM_8K_14 = "1-4"
    FORM_8K_21 = "2-1"
    FORM_8K_22 = "2-2"
    FORM_8K_23 = "2-3"
    FORM_8K_24 = "2-4"
    FORM_8K_25 = "2-5"
    FORM_8K_26 = "2-6"
    FORM_8K_31 = "3-1"
    FORM_8K_32 = "3-2"
    FORM_8K_33 = "3-3"
    FORM_8K_41 = "4-1"
    FORM_8K_42 = "4-2"
    FORM_8K_51 = "5-1"
    FORM_8K_52 = "5-2"
    FORM_8K_53 = "5-3"
    FORM_8K_54 = "5-4"
    FORM_8K_55 = "5-5"
    FORM_8K_56 = "5-6"
    FORM_8K_57 = "5-7"
    FORM_8K_58 = "5-8"
    FORM_8K_61 = "6-1"
    FORM_8K_62 = "6-2"
    FORM_8K_63 = "6-3"
    FORM_8K_64 = "6-4"
    FORM_8K_65 = "6-5"
    FORM_8K_66 = "6-6"
    FORM_8K_610 = "6-10"
    FORM_8K_71 = "7-1"
    FORM_8K_81 = "8-1"
    FORM_8K_91 = "9-1"
    FORM_8K_SIGNATURE = "signature"

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
        DocumentType.FORM_8K: [
            SectionType.FORM_8K_11,
            SectionType.FORM_8K_12,
            SectionType.FORM_8K_13,
            SectionType.FORM_8K_14,
            SectionType.FORM_8K_21,
            SectionType.FORM_8K_22,
            SectionType.FORM_8K_23,
            SectionType.FORM_8K_24,
            SectionType.FORM_8K_25,
            SectionType.FORM_8K_26,
            SectionType.FORM_8K_31,
            SectionType.FORM_8K_32,
            SectionType.FORM_8K_33,
            SectionType.FORM_8K_41,
            SectionType.FORM_8K_42,
            SectionType.FORM_8K_51,
            SectionType.FORM_8K_52,
            SectionType.FORM_8K_53,
            SectionType.FORM_8K_54,
            SectionType.FORM_8K_55,
            SectionType.FORM_8K_56,
            SectionType.FORM_8K_57,
            SectionType.FORM_8K_58,
            SectionType.FORM_8K_61,
            SectionType.FORM_8K_62,
            SectionType.FORM_8K_63,
            SectionType.FORM_8K_64,
            SectionType.FORM_8K_65,
            SectionType.FORM_8K_66,
            SectionType.FORM_8K_610,
            SectionType.FORM_8K_71,
            SectionType.FORM_8K_81,
            SectionType.FORM_8K_91,
            SectionType.FORM_8K_SIGNATURE,
        ]
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
        SectionType.FORM_10K_15: "Exhibit and Financial Statement Schedules", # Note: No information provided about ID `15` in sec-api.io docs (https://sec-api.io/docs/sec-filings-item-extraction-api).
        # Related to 8-K
        SectionType.FORM_8K_11: "Entry into a Material Definitive Agreement",
        SectionType.FORM_8K_12: "Termination of a Material Definitive Agreement",
        SectionType.FORM_8K_13: "Bankruptcy or Receivership",
        SectionType.FORM_8K_14: "Mine Safety - Reporting of Shutdowns and Patterns of Violations",
        SectionType.FORM_8K_21: "Completion of Acquisition or Disposition of Assets",
        SectionType.FORM_8K_22: "Results of Operations and Financial Condition",
        SectionType.FORM_8K_23: "Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant",
        SectionType.FORM_8K_24: "Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement",
        SectionType.FORM_8K_25: "Cost Associated with Exit or Disposal Activities",
        SectionType.FORM_8K_26: "Material Impairments",
        SectionType.FORM_8K_31: "Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing",
        SectionType.FORM_8K_32: "Unregistered Sales of Equity Securities",
        SectionType.FORM_8K_33: "Material Modifications to Rights of Security Holders",
        SectionType.FORM_8K_41: "Changes in Registrant's Certifying Accountant",
        SectionType.FORM_8K_42: "Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review",
        SectionType.FORM_8K_51: "Changes in Control of Registrant",
        SectionType.FORM_8K_52: "Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers: Compensatory Arrangements of Certain Officers",
        SectionType.FORM_8K_53: "Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year",
        SectionType.FORM_8K_54: "Temporary Suspension of Trading Under Registrant's Employee Benefit Plans",
        SectionType.FORM_8K_55: "Amendments to the Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics",
        SectionType.FORM_8K_56: "Change in Shell Company Status",
        SectionType.FORM_8K_57: "Submission of Matters to a Vote of Security Holders",
        SectionType.FORM_8K_58: "Shareholder Nominations Pursuant to Exchange Act Rule 14a-11",
        SectionType.FORM_8K_61: "ABS Informational and Computational Material",
        SectionType.FORM_8K_62: "Change of Servicer or Trustee",
        SectionType.FORM_8K_63: "Change in Credit Enhancement or Other External Support",
        SectionType.FORM_8K_64: "Failure to Make a Required Distribution",
        SectionType.FORM_8K_65: "Securities Act Updating Disclosure",
        SectionType.FORM_8K_66: "Static Pool",
        SectionType.FORM_8K_610: "Alternative Filings of Asset-Backed Issuers",
        SectionType.FORM_8K_71: "Regulation FD Disclosure",
        SectionType.FORM_8K_81: "Other Events",
        SectionType.FORM_8K_91: "Financial Statements and Exhibits",
        SectionType.FORM_8K_SIGNATURE: "Signature",
    },
)
