# 🌐 Language Translation Tool

**CodeAlpha Artificial Intelligence Internship — Task 1**

A web app that translates text between 20+ languages using the **Microsoft Translator API** (Azure AI Translator), built with **Python** and **Streamlit**.

## ✨ Features

- Enter text and choose **source** and **target** languages
- **Auto-detect** the source language (with confidence score)
- **Swap** languages in one click (the translation becomes the new input)
- Translations come from the **Microsoft Translator REST API v3**
- **Copy** button for the translated text
- **Text-to-speech** (🔊 Listen) using gTTS
- Right-to-left display for Arabic, Persian and Urdu
- Clear error messages (missing key, invalid key, network errors, empty input)

## 🛠️ Tech Stack

| Part | Technology |
|------|------------|
| UI | Streamlit |
| Translation | Microsoft Translator API v3 |
| HTTP | requests |
| Text-to-speech | gTTS |
| Config | python-dotenv |

## 📁 Project Structure

```
CodeAlpha_LanguageTranslationTool/
├── app.py            # Streamlit user interface
├── translator.py     # Microsoft Translator API wrapper
├── requirements.txt
├── .env.example      # Template for your API credentials
└── README.md
```

## 🚀 Setup

### 1. Get a free Microsoft Translator key
1. Sign in to the [Azure portal](https://portal.azure.com).
2. **Create a resource** → search **Translator** → **Create**.
3. Choose the **Global** region and the **Free F0** pricing tier (2M characters/month).
   > Azure for Students subscriptions only allow some regions; if you get `RequestDisallowedByAzure`, pick **Global**.
4. After it deploys, open the resource → **Keys and Endpoint** → copy **KEY 1** and the **Location/Region** (`global`).

### 2. Install and configure
```bash
git clone https://github.com/Salsabil-23/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
python -m venv venv
venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env       # macOS/Linux: cp .env.example .env
```
Open `.env` and fill in `TRANSLATOR_KEY` and `TRANSLATOR_REGION`.

### 3. Run
```bash
streamlit run app.py
```
The app opens at http://localhost:8501.

## ⚙️ How It Works

1. The user enters text and picks the languages in the Streamlit UI.
2. `translator.translate()` sends a POST request to
   `https://api.cognitive.microsofttranslator.com/translate?api-version=3.0`
   with the subscription key and region in the headers.
3. The API returns JSON with the translated text (and the detected language when auto-detect is on).
4. The app shows the result, with options to copy it or listen to it.

## 🔒 Security

Your API key stays in `.env`, which is listed in `.gitignore` and never committed.

## 👤 Author

*Salsabil Hafsi* — CodeAlpha AI Intern · [LinkedIn](#) · [GitHub](#)
