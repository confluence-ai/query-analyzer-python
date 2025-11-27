# Furniture Query Parser

Convert natural-language furniture queries into structured JSON for backend systems and sends brand and product name recommendations.

This service accepts human-written queries like:

```css
“I need a modern sofa with ornate legs”
```

and converts them into machine-readable structured output:

```json
{
  "product_types": ["Sofa"],
  "features": ["Ornate leg"],
  "styles": ["Modern"],
  "classification_summary": {},
  "price_range": null,
  "suggested_query": null,
  "original_query": "I need a modern sofa with ornate legs",
  "success": true
}
```
The parser uses direct string match, fuzzy matching, and spelling correction to interpret queries reliably.

## Features

### Product Type Detection

Recognizes furniture types (sofa, armchair, table, bed…) using a domain-trained dictionary.

### Feature Extraction

Identifies features such as:
- ornate legs
- rounded arms
- metal legs
- etc.

### Style Extraction

Parses style indicators:
- modern
- Scandinavian
- rustic
- mid-century
- etc.

### Classification Extraction

Understands variant descriptors:
- 1 seater
- 2 seater
- 3 seater
- Compact
- etc.

### Price Extraction

Understands patterns like:

- “under 20k”
- “between ₹10,000–15,000”
- “budget under $500”

### Spelling Suggestion

If user types:

```csharp
modren sofaa with metal legs
```

System correctly interprets:
```json
{
  "product_types": ["Sofa"],
  "features": ["metal leg"],
  "styles": ["Modern"],
  "classification_summary": {"2 seater": 1.0},
  "price_range": null,
  "suggested_query": null,
  "original_query": "modren sofaa with metal legs",
  "success": true
}
```

### Dictionary-Based Parsing

Furniture dictionaries are stored in `/dictionary` and can be updated without changing parser logic.

## Project Structure

```
├── config
│   ├── config.py
│   ├── constants.py
│   ├── database.py
│   ├── sync_dicts.py
│
├── dictionary
│   ├── furniture_classification.json
│   ├── furniture_features.json
│   ├── furniture_styles.json
│   ├── furniture_type.json
│
├── query_parser
│   ├── classification_extractor.py
│   ├── feature_extractor.py
│   ├── furniture_parser.py
│   ├── price_extractor.py
│   ├── product_type_extractor.py
│
├── query_suggestion
│   ├── style_extractor.py
│   ├── product_brand_extractor.py
│   ├── suggestion.py
│
├── utils
│   ├── helpers.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt

```

## Installation

1. Clone repo
```bash
git clone <your-repo-url>
cd furniture-query-parser
```

2.  Create venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add environment variables
    
    Copy example file:
    ```bash
    cp .env.example .env
    ```

    Edit `.env` according to your configs.

## Docker Support

Build:

```bash
docker build -t furniture-parser .
```

Run:

```bash
docker run -p 8432:8432 furniture-parser
```

## Roadmap (Upcoming Features)

This lists future planned features that are NOT yet started but will provide major improvements.

1. Semantic Embedding Matching

    Use Embeddings (OpenAI / HuggingFace) to detect relationships like:
    - “couch” → “sofa”
    - “retro” → “mid-century”
    - “sitting chair” → “armchair”

2. Multiword Phrase Recognition

    Improve detection of multiword furniture terms using n-grams:
    - "wing back chair"
    - "queen size bed"
    - "storage hydraulic lift bed"

3. Multilingual Support

    Detect and parse Hindi + Hinglish:
    - “modern sofa chahiye with wooden legs”

4. Advanced Ranking Engine

    Combine:
    - embeddings
    - lexical match
    - popularity
    - click logs

## Ongoing Work (Current Active Development)

These are the tasks currently in development, based on updates:

1. Lexical Search Matching Instead of Direct Matching

    Replacing rigid string lookup with:
    - token-level matching
    - phrase-level matching
    - robust normalization
    - synonym expansion

    This improves parsing of messy queries like:
    ```csharp
    modrn soffa with woodn legz
    ```

2. Enhanced Spelling Correction Engine

    Currently updating the spell-correction pipeline to:
    - avoid over-correction
    - use context-sensitive repair
    - use embeddings for ambiguous cases
    - identify when NOT to correct

3. Query Rewriting Layer

    Rewriting user query into a normalized form:

    ```arduino
    "modrn soffa with woodn legz"
    → "modern sofa with wooden legs"
    ```

    This helps downstream search systems produce better results.

4. Dictionary Expansion
    
    Actively refining domain dictionaries:
    - Adding new features
    - Fixing inconsistent naming
    - Improving synonym mapping
    - Handling multiple variants (“grey/gray”)