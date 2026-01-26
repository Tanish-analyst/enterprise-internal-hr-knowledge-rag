import os
from collections import defaultdict
from langchain_core.documents import Document


def preprocess(documents):
    docs_by_source = defaultdict(list)

    for page in documents:
        docs_by_source[page.metadata["source"]].append(page)

    merged_docs = []

    for raw_source, page_list in docs_by_source.items():
        page_list_sorted = sorted(
            page_list, key=lambda x: x.metadata.get("page", 0)
        )

        full_text = "\n\n".join(
            [p.page_content for p in page_list_sorted]
        )

        folder_name = os.path.basename(os.path.dirname(raw_source))
        filename = os.path.basename(raw_source)
        file_stem, _ = os.path.splitext(filename)

        display_source = f"{folder_name}/{file_stem}"

        category = "general"

        if "COMPANY-SPECIFIC" in folder_name:
            category = "company_info"
        elif "EMPLOYEE_LIFECYCLE" in folder_name:
            category = "employee_lifecycle"
        elif "hr_policy" in folder_name:
            category = "hr_policy"
        elif "PAYROLL" in folder_name or "BENEFITS" in folder_name:
            category = "payroll_benefits"

        employee = False
        manager = False
        hr = False

        if category == "company_info":
            hr = True
        elif category == "employee_lifecycle":
            manager = True
        elif category == "hr_policy":
            employee = True
        elif category == "payroll_benefits":
            employee = True
            manager = True

        metadata = {
            "source": display_source,
            "category": category,
            "employee": employee,
            "manager": manager,
            "hr": hr,
        }

        merged_docs.append(
            Document(page_content=full_text, metadata=metadata)
        )

    return merged_docs
