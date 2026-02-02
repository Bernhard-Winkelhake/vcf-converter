# vcf-converter

This Python script converts one or multiple Excel files (`.xlsx`, `.xls`) into a single `VCF` (vCard) file that can be imported into contact applications such as **Android**, **iOS**, **Google Contacts**, or **Outlook**.

Phone numbers are automatically normalized to a configurable country format (default: **Germany +49**).

---

## Expected Excel Format

Your Excel files must contain the following **column headers**:

| Column name      | Required | Description              |
|------------------|----------|--------------------------|
| `Vorname`        | yes      | First name               |
| `Nachname`       | yes      | Last name                |
| `Telefonnummer` | yes      | Phone number (any format)|

> Column names are **case-sensitive**.


## Configuration (`config.py`)

All country-specific settings are centralized in `config.py`:

```python
COUNTRY_CODE = "49"
INT_PREFIX = "00"
NATIONAL_PREFIX = "0"