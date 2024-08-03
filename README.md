# ML Translator

This repository contains a Flask application that uses the `MBartForConditionalGeneration` model from Hugging Face for language translation. The application exposes an API endpoint to translate text from English to various target languages.

## Prerequisites

Before setting up the application, ensure you have the following installed:

- Python 3.9 or later
- Pip (Python package installer)

## Setup

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a Virtual Environment**

   Create and activate a virtual environment to manage dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If you don't have a `requirements.txt` file, you can manually install the required packages:

   ```bash
   pip install flask transformers torch protobuf
   ```

4. **Verify Installation**

   Ensure that the necessary packages are installed:

   ```bash
   pip show flask transformers torch protobuf
   ```

5. **Run the Application**

   Start the Flask application:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:3000`.

## API Endpoint

### `/translate`

**Method:** `POST`

**Description:** Translates the provided input text into the specified target language.

**Request Body:**

```json
{
  "input_text": "The text to be translated",
  "target_language": "Language code (e.g., 'hi_IN' for Hindi, 'zh_CN' for Chinese)"
}
```

**Response:**

```json
{
  "translated_text": "Translated text in the target language"
}
```

**Example Request Using `curl`:**

```bash
curl -X POST http://localhost:3000/translate \
     -H "Content-Type: application/json" \
     -d '{
       "input_text": "The head of the United Nations says there is no military solution in Syria",
       "target_language": "hi_IN"
     }'
```

**Example Response:**

```json
{
  "translated_text": "संयुक्त राष्ट्र के नेता कहते हैं कि सीरिया में कोई सैन्य समाधान नहीं है"
}
```

## Langauges Covered:

- Arabic (ar_AR)
- Czech (cs_CZ)
- German (de_DE)
- English (en_XX)
- Spanish (es_XX)
- Estonian (et_EE)
- Finnish (fi_FI)
- French (fr_XX)
- Gujarati (gu_IN)
- Hindi (hi_IN)
- Italian (it_IT)
- Japanese (ja_XX)
- Kazakh (kk_KZ)
- Korean (ko_KR)
- Lithuanian (lt_LT)
- Latvian (lv_LV)
- Burmese (my_MM)
- Nepali (ne_NP)
- Dutch (nl_XX)
- Romanian (ro_RO)
- Russian (ru_RU)
- Sinhala (si_LK)
- Turkish (tr_TR)
- Vietnamese (vi_VN)
- Chinese (zh_CN)
- Afrikaans (af_ZA)
- Azerbaijani (az_AZ)
- Bengali (bn_IN)
- Persian (fa_IR)
- Hebrew (he_IL)
- Croatian (hr_HR)
- Indonesian (id_ID)
- Georgian (ka_GE)
- Khmer (km_KH)
- Macedonian (mk_MK)
- Malayalam (ml_IN)
- Mongolian (mn_MN)
- Marathi (mr_IN)
- Polish (pl_PL)
- Pashto (ps_AF)
- Portuguese (pt_XX)
- Swedish (sv_SE)
- Swahili (sw_KE)
- Tamil (ta_IN)
- Telugu (te_IN)
- Thai (th_TH)
- Tagalog (tl_XX)
- Ukrainian (uk_UA)
- Urdu (ur_PK)
- Xhosa (xh_ZA)
- Galician (gl_ES)
- Slovene (sl_SI)
