"""
Invoice Data Extractor — Gemini API
Extracts structured information from invoice images using Google Gemini.

Requirements:
    pip install google-genai

Usage:
    export GEMINI_API_KEY="your-api-key"
    python extract_invoice_gemini.py <image_path>

Get a free API key at: https://aistudio.google.com/apikey
"""

import base64
import json
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ── 1. Load image ─────────────────────────────────────────────────────────────

def load_image(image_path: str) -> tuple[str, str]:
    """Return (base64_data, mime_type) for the image."""
    suffix = Path(image_path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png",  ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(suffix, "image/jpeg")
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode(), mime_type


# ── 2. Extract via Gemini ─────────────────────────────────────────────────────

PROMPT = """Extract every field from this invoice image and return a single JSON object.
Use exactly this structure (keep all keys, use empty string or 0 when a field is blank):

{
  "invoice":   { "serial_number": "", "number": "", "date": "", "tax_authority_code": "" },
  "seller":    { "name": "", "tax_code": "", "address": "", "phone": "", "email": "",
                 "bank_account": "", "bank_name": "" },
  "buyer":     { "name": "", "company_name": "", "address": "", "tax_code": "",
                 "identity_card": "", "payment_method": "", "bank_account": "" },
  "line_items": [
    { "no": 1, "description": "", "unit": "", "quantity": 0,
      "unit_price": 0, "amount_before_vat": 0, "vat_rate": "",
      "vat_amount": 0, "amount_after_vat": 0 }
  ],
  "summary":   { "total_amount_before_vat": 0, "total_vat_amount": 0,
                 "total_payment": 0, "amount_in_words": "" },
  "signature": { "signed_by": "", "signed_date": "", "valid": false },
  "verification_url": "",
  "verification_code": ""
}

Return ONLY the JSON object — no markdown fences, no commentary."""


def extract(image_path: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("Set the GEMINI_API_KEY environment variable first.")

    client = genai.Client(api_key=api_key)

    image_data, mime_type = load_image(image_path)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=base64.b64decode(image_data),
                mime_type=mime_type,
            ),
            PROMPT,
        ],
    )

    raw = response.text.strip()
    # Strip accidental markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── 3. Pretty print ───────────────────────────────────────────────────────────

def print_summary(data: dict) -> None:
    inv, seller, buyer = data["invoice"], data["seller"], data["buyer"]
    items, summary, sig = data["line_items"], data["summary"], data["signature"]

    sep = "=" * 64
    print(sep)
    print("  INVOICE SUMMARY")
    print(sep)

    print("\n📄 Invoice")
    print(f"   Serial No : {inv['serial_number']}")
    print(f"   Number    : {inv['number']}")
    print(f"   Date      : {inv['date']}")
    print(f"   Tax Auth  : {inv['tax_authority_code']}")

    print("\n🏪 Seller")
    print(f"   Name      : {seller['name']}")
    print(f"   Tax Code  : {seller['tax_code']}")
    print(f"   Address   : {seller['address']}")
    print(f"   Phone     : {seller['phone']}")
    print(f"   Email     : {seller['email']}")
    print(f"   Bank      : {seller['bank_account']}  {seller['bank_name']}")

    print("\n🧑‍💼 Buyer")
    print(f"   Name      : {buyer['name']}")
    print(f"   Company   : {buyer['company_name']}")
    print(f"   Address   : {buyer['address']}")
    print(f"   Tax Code  : {buyer['tax_code']}")
    print(f"   Payment   : {buyer['payment_method']}")

    print("\n🛒 Line Items")
    print(f"   {'#':<3} {'Description':<32} {'Unit':<6} {'Qty':>3} {'Price':>10} {'VAT':>4} {'Total':>11}")
    print("   " + "-" * 74)
    for it in items:
        print(
            f"   {it['no']:<3} {it['description']:<32} {it['unit']:<6}"
            f" {it['quantity']:>3} {it['unit_price']:>10,.0f}"
            f" {it['vat_rate']:>4} {it['amount_after_vat']:>11,.0f}"
        )

    print("\n💰 Summary")
    print(f"   Before VAT : {summary['total_amount_before_vat']:>12,.0f} VND")
    print(f"   VAT        : {summary['total_vat_amount']:>12,.0f} VND")
    print(f"   Total      : {summary['total_payment']:>12,.0f} VND")
    print(f"   In words   : {summary['amount_in_words']}")

    print("\n✅ Signature")
    print(f"   Signed by : {sig['signed_by']}")
    print(f"   Date      : {sig['signed_date']}")
    print(f"   Valid     : {sig['valid']}")

    print("\n🔗 Verification")
    print(f"   URL  : {data['verification_url']}")
    print(f"   Code : {data['verification_code']}")
    print(sep)


# ── 4. Main ───────────────────────────────────────────────────────────────────

def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else "DemoInvoice.jpeg"

    print(f"Extracting invoice data from: {image_path}")
    print("Calling Gemini API …\n")

    data = extract(image_path)

    out = Path(image_path).stem + "_extracted.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON saved → {out}\n")

    print_summary(data)


if __name__ == "__main__":
    main()