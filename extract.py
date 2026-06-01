import re

def find_first(pattern: str, text: str):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_date(text: str):
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{2}-\d{2}-\d{4})",
        r"([A-Za-z]+\s+\d{1,2},\s+\d{4})",]
    
    for pattern in patterns:
        result = find_first(pattern, text)
        if result:
            return result
    return None


def extract_amount(text: str):
    patterns = [
        r"total\s*amount[:\s$]*([\d,]+(?:\.\d{1,2})?)",
        r"amount\s*due[:\s$]*([\d,]+(?:\.\d{1,2})?)",
        r"balance\s*due[:\s$]*([\d,]+(?:\.\d{1,2})?)",
        r"grand\s*total[:\s$]*([\d,]+(?:\.\d{1,2})?)",
        r"total[:\s$]*([\d,]+(?:\.\d{1,2})?)",]
    
    for pattern in patterns:
        result = find_first(pattern, text)
        if result:
            return float(result.replace(",", ""))
    return None


def extract_company(text: str):

    return (
        find_first(r"([A-Z][A-Za-z0-9\s]+?(?:Ltd|LLC|Inc|Corp|Tech))(?:\s|$)", text))

def extract_name(text: str):
    first_line = text.strip().split("\n")[0].strip()
    if 1 < len(first_line.split()) <= 5:
        return first_line

    words = text.split()
    if len(words) >= 2:
        return f"{words[0]} {words[1]}"

    return None

def extract_experience_years(text: str):
    patterns = [
    r"(\d+)\+?\s*(?:years|yrs)[\s\.]*(?:of\s*)?experience",
    r"experience[:\s]*(\d+)\+?\s*(?:years|yrs)",
    r"(\d+)\+?\s*(?:years|yrs)\s*(?:in|of|with)",
    r"over\s*(\d+)\s*(?:years|yrs)",]
    
    for pattern in patterns:
        result = find_first(pattern, text)
        if result:
            return int(result)
    return None

def extract_invoice_fields(text: str) -> dict:
    return {
        "invoice_number": find_first(r"invoice\s*#\s*(\d+)", text),
        "date":           extract_date(text),
        "company":        extract_company(text),
        "total_amount":   extract_amount(text),}

def extract_resume_fields(text: str) -> dict:
    return {
        "name":             extract_name(text),
        "email":            find_first(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text),
        "phone":            find_first(r"(\+?\d[\d\s\-()]{8,}\d)", text),
        "experience_years": extract_experience_years(text),}

def extract_utility_bill_fields(text: str) -> dict:
    return {
        "account_number": find_first(r"account\s*(?:number|no)?[:\s#-]*([A-Z0-9-]+)", text),
        "date":           extract_date(text),
        "usage_kwh":      find_first(r"([\d]+(?:\.\d+)?)\s*kwh", text),
        "amount_due":     extract_amount(text),}

def extract_fields(document_class: str, text: str) -> dict:
    if document_class == "Invoice":
        return extract_invoice_fields(text)
    if document_class == "Resume":
        return extract_resume_fields(text)
    if document_class == "Utility Bill":
        return extract_utility_bill_fields(text)
    return {}