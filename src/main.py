import pandas as pd
from tkinter import Tk, filedialog

import config


def safe_str(value):

    if pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def normalize_phone(number):
    if not number:
        return None

    number = str(number)  

    for char in config.CLEANUP_CHARS:
        number = number.replace(char, "")

    if number.startswith(config.DEFAULT_COUNTRY_CODE):
        return number

    if number.startswith(config.COUNTRY_CODE_WITH_PREFIX):
        return config.DEFAULT_COUNTRY_CODE + number[len(config.COUNTRY_CODE_WITH_PREFIX):]

    if number.startswith(config.NATIONAL_PREFIX):
        return config.DEFAULT_COUNTRY_CODE + number[1:]

    return config.DEFAULT_COUNTRY_CODE + number



def excel_to_vcf():
    root = Tk()
    root.withdraw()

    excel_files = filedialog.askopenfilenames(
        title="Excel-Dateien auswählen",
        filetypes=[("Excel Dateien", "*.xlsx *.xls")]
    )

    if not excel_files:
        print("Keine Dateien ausgewählt.")
        return

    vcf_lines = []
    skipped = 0

    for file in excel_files:
        try:
            df = pd.read_excel(file)

            for _, row in df.iterrows():
                vorname = safe_str(row.get(config.COLUMN_NAME_NAME))
                nachname = safe_str(row.get(config.COLOUMN_NAME_SURNAME))
                telefon_raw = safe_str(row.get(config.COLUMN_NAME_PHONE))

                # Unvollständige Zeilen überspringen
                if not vorname or not nachname or not telefon_raw:
                    skipped += 1
                    continue

                telefon = normalize_phone(telefon_raw)
                if not telefon:
                    skipped += 1
                    continue

                vcf_lines.append(
                    "BEGIN:VCARD\n"
                    "VERSION:3.0\n"
                    f"N:{nachname};{vorname};;;\n"
                    f"FN:{vorname} {nachname}\n"
                    f"TEL;TYPE=CELL:{telefon}\n"
                    "END:VCARD\n"
                )

        except Exception as e:
            print(f"Fehler in Datei {file}: {e}")

    with open("kontakte.vcf", "w", encoding="utf-8") as f:
        f.writelines(vcf_lines)

    print(f"Fertig: {len(vcf_lines)} Kontakte gespeichert")
    print(f"Übersprungen  {skipped} ungültige Zeilen")


if __name__ == "__main__":
    excel_to_vcf()
