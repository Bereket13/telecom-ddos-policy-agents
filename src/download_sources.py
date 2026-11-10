"""Download the public source documents of the knowledge base into a folder.

The EU texts are fetched from the EU Publications Office (content negotiation),
because eur-lex.europa.eu blocks scripted downloads.
"""
import sys
import urllib.request
from pathlib import Path

DIRECT = {
    "G01_ITU-T_Y.3172_ML_architecture.pdf": "https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-Y.3172-201906-I!!PDF-E&type=items",
    "G02_ITU_AI_Ready_Readiness_Framework_v2.pdf": "https://www.itu.int/dms_pub/itu-t/opb/ai4g/T-AI4G-AI4GOOD-2025-6-PDF-E.pdf",
    "G03_ITU-T_X.1056_Telecom_Incident_Management.pdf": "https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-X.1056-200901-I!!PDF-E&type=items",
    "G04_EU_AI_Act_2024-1689.pdf": "https://publications.europa.eu/resource/celex/32024R1689",
    "G05_EU_NIS2_Directive_2022-2555.pdf": "https://publications.europa.eu/resource/celex/32022L2555",
    "G07_NIST_CSF_2.0.pdf": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    "G08_NIST_AI_RMF_1.0.pdf": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    "G09_NIST_SP800-61r3_Incident_Response.pdf": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf",
    "G10_OECD_AI_Recommendation.pdf": "https://legalinstruments.oecd.org/api/print?ids=648&lang=en",
    "G12_AU_Malabo_Convention_Cyber_Security_Data_Protection.pdf": "https://www.ccdcoe.org/uploads/2018/11/AU-270614-CSConvention.pdf",
    "G13_AU_Continental_AI_Strategy_2024.pdf": "https://au.int/sites/default/files/documents/44004-doc-EN-_Continental_AI_Strategy_July_2024.pdf",
    "U01_UAE_National_AI_Strategy_2031.pdf": "https://ai.gov.ae/wp-content/uploads/2021/07/UAE-National-Strategy-for-Artificial-Intelligence-2031.pdf",
    "E01_Ethiopia_Computer_Crime_Proclamation_958-2016_A19_translation.pdf": "https://www.article19.org/data/files/medialibrary/38450/Ethiopia-Computer-Crime-Proclamation-Legal-Analysis-July-(1).pdf",
    "E02_CoE_Octopus_Ethiopia_Cybercrime_Legal_Profile.pdf": "https://rm.coe.int/octocom-legal-profile-ethiopia-version-1apr2020/16809e9270",
}


def main(out_dir="docs"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, url in DIRECT.items():
        target = out / name
        if target.exists() and target.stat().st_size > 1000:
            print("[have]", name)
            continue
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/pdf", "Accept-Language": "eng"}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180) as r:
                data = r.read()
            if not data.startswith(b"%PDF"):
                raise ValueError("not a PDF")
            target.write_bytes(data)
            print("[ok]  ", name, len(data))
        except Exception as e:
            print("[FAIL]", name, e, "-> download manually from kb/sources.csv")


if __name__ == "__main__":
    main(*sys.argv[1:])
