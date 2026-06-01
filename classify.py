def classify_document(text: str) -> str:

    if len(text.strip()) < 30:
        return "Unclassifiable"

    text_lower = text.lower()

    # no standalone "invoice" or "resume" — too generic
    invoice      = ["invoice #", "invoice number", "invoice no", "bill to", "total amount"]
    resume       = ["curriculum vitae", "work experience", "skills",
                    "education", "experience:", "email:", "phone:", "summary:"]
    utility_bill = ["account number", "meter reading", "kwh", "amount due",
                    "utility", "billing date"]

    scores = {
        "Invoice":      sum(1 for kw in invoice      if kw in text_lower),
        "Resume":       sum(1 for kw in resume        if kw in text_lower),
        "Utility Bill": sum(1 for kw in utility_bill  if kw in text_lower),
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Other"

    return best