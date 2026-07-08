import os
import re
import requests
import telebot
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

load_dotenv()
ai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENAI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

class HermesAuditor:
    def __init__(self):
        self.api_key = os.getenv("BASESCAN_API_KEY")
        self.v2_api_url = "https://api.etherscan.io/v2/api"

    def check_risks(self, code):
        risky = ["setBlacklist", "blacklist", "setTax", "setFees", "renounceOwnership"]
        return [f for f in risky if f in code]

    def fetch_contract_source(self, address):
        params = {"chainid": "8453", "module": "contract", "action": "getsourcecode", "address": address, "apikey": self.api_key}
        try:
            res = requests.get(self.v2_api_url, params=params, timeout=15).json()
            if res.get("status") == "1": return res["result"][0].get("SourceCode"), "Verified"
        except: pass
        return None, None

    def ai_deep_audit(self, code, ctype, dist, addr):
        risks = self.check_risks(code)
        prompt = f"Audit this contract. Risky functions found: {risks}. Code: {code[:3000]}"
        try:
            res = ai_client.chat.completions.create(model="google/gemini-2.5-flash", messages=[{"role": "user", "content": prompt}])
            return res.choices[0].message.content
        except: return "Audit Failed."

    def build_pdf_report(self, file, addr, dist, report, ctype):
        doc = SimpleDocTemplate(file, pagesize=letter)
        story = [Paragraph("<b>HERMES SECURITY REPORT</b>", ParagraphStyle('Title', fontSize=16))]
        story.append(Paragraph(f"Address: {addr}", ParagraphStyle('Meta', fontSize=10)))
        story.append(Paragraph(report, ParagraphStyle('Body', fontSize=9)))
        doc.build(story)

auditor = HermesAuditor()

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "Hermes Online. Address gir.")

@bot.message_handler(func=lambda m: True)
def handle(m):
    addr = m.text.strip()
    code, ctype = auditor.fetch_contract_source(addr)
    report = auditor.ai_deep_audit(code or "", ctype, [], addr)
    pdf = f"Report_{addr[:8]}.pdf"
    auditor.build_pdf_report(pdf, addr, [], report, ctype)
    with open(pdf, "rb") as f: bot.send_document(m.chat.id, f)

if __name__ == "__main__":
    bot.infinity_polling()