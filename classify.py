def classify_document(text: str) -> str:

    text_lower = text.lower()

    if len(text_lower.strip()) < 30:
        return "Unclassifiable"

    invoice = ["invoice","invoice number","invoice no","inv-","bill to","total amount"]

    resume = ["resume","curriculum vitae","work experience","skills","education","projects","experience"]

    utility_bill = ["utility bill","electricity bill","gas bill","water bill","account number","meter reading","kwh","amount due"]

    if any(keyword in text_lower for keyword in invoice):
        return "Invoice"

    if any(keyword in text_lower for keyword in resume):
        return "Resume"

    if any(keyword in text_lower for keyword in utility_bill):
        return "Utility Bill"

    return "Other"