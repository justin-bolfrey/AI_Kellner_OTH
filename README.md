# OTH AI Projekt – Angewandte KI und KI Literacy

Dieses Repository enthält begleitenden Beispielcode aus der Vorlesung zu Angewandter KI und KI Literacy. Ziel ist es, tabellarische Daten (CSV) in eine SQLite‑Datenbank zu laden und darauf aufbauend einfache Explorative Datenanalysen (EDA) in Python durchzuführen.

## Überblick
- `create_db.py`: Liest CSV‑Dateien aus `oth_data/`, schreibt sie als Tabellen in `oth_shpm.db` (SQLite) und stellt die Funktion `get_data()` zum Laden der DataFrames bereit.
- `03_eda.py`: Führt DataFrames zusammen (Join/Merge), bereitet Spalten auf (z. B. Datumsparsing) und zeigt einfache EDA‑Schritte. Die Datei ist in ausführbare Zellen (`# %%`) gegliedert.
- `oth_data/`: Enthält die Quelldaten (`customer.csv`, `plant.csv`, `shipment.csv`, `us_change.csv`).
- `oth_shpm.db`: Die generierte SQLite‑Datenbank.

## Voraussetzungen
- Python 3 (empfohlen: 3.10+)
- Optional: Virtuelle Umgebung (`venv`)
- Python‑Pakete: `pandas`, optional `plotnine` (für Visualisierung), sowie für interaktive Zellen/Notebooks `ipykernel`/`jupyter`.

## Setup (empfohlen mit venv)
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install pandas plotnine ipykernel jupyter
```

## Datenbank erstellen
```bash
python3 create_db.py
```
Dadurch werden die CSV‑Dateien aus `oth_data/` in die SQLite‑Datenbank `oth_shpm.db` geschrieben (Tabellen: `customer`, `plant`, `shipment`, `us_change`). Die Funktion `get_data()` kann in anderen Skripten genutzt werden, um diese Tabellen als DataFrames zu laden.

## Explorative Datenanalyse (EDA)
Die Datei `03_eda.py` nutzt `# %%`‑Zellmarkierungen. In Editoren wie Cursor/VS Code können einzelne Zellen ausgeführt werden (Python/Jupyter‑Erweiterung erforderlich). Typische Schritte:
- Zusammenführen der Tabellen über Schlüsselspalten (`merge`).
- Aufbereiten von Spalten, z. B. Datumswerte im Format `dd.mm.yyyy` mittels `pd.to_datetime(..., format="%d.%m.%Y", errors="coerce")`.
- Erste Sichten (`head`, `tail`, `info`) und einfache Ableitungen (z. B. `tons = GWkg / 1000`).

## Hinweise
- Pfade sind relativ zum Projektstamm; bitte Repository als Workspace öffnen.
- Das Datumsfeld `Delivery_day` ist deutsch formatiert (`dd.mm.yyyy`). Falls Parsing‑Fehler auftreten, Format/`dayfirst` passend setzen.
- Für interaktive Ausführung sicherstellen, dass als Interpreter der Projekt‑`venv` ausgewählt ist.

## Kontext der Vorlesung
Der Code entstammt der Lehrveranstaltung zu Angewandter KI und KI Literacy. Er dient dazu, den praktischen Umgang mit Datenpipelines (CSV → SQLite), grundlegender Datenaufbereitung und ersten Analyse‑/Visualisierungsschritten in Python zu demonstrieren.

## Lizenz/Urheberschaft
Nur zu Lehr‑ und Übungszwecken. Inhalte stammen aus der Vorlesung und wurden für das praktische Arbeiten im Kurs aufbereitet. Bitte klären Sie eine Weitergabe/Weiterverwendung außerhalb des Kurses mit den verantwortlichen Lehrenden.


