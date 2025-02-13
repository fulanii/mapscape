## MapScape

A Selenium bot built with python, that scrape's publicly available business data form Google maps and save it to a text file.
## Instalation
1. Clone the repository:

```bash
git clone https://github.com/fulanii/mapscape.git
cd mapscape
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Update these variables from bot.py:
    * business_type
    * business_city
    * business_state_or_country

4. run bot.py
```bash
python bot.py
```

## Demo
![dome](/mapscrape.gif)