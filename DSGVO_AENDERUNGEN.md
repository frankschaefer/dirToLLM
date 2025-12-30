# DSGVO-Klassifizierung: Änderungen v1.19.0

## Zusammenfassung
Die DSGVO-Klassifizierung wurde präzisiert, um zwischen Firmen-Bankdaten (nicht personenbezogen) und privaten Bankdaten (personenbezogen) zu unterscheiden.

## Rechtlicher Hintergrund

### Firmen-IBANs sind NICHT personenbezogen
- **Art. 4 Nr. 1 DSGVO**: Personenbezogene Daten müssen sich auf natürliche Personen beziehen
- **Juristische Personen** (GmbH, AG, UG, KG, OHG, e.V., Stiftung) fallen NICHT unter die DSGVO
- **Geschäftsdokumente** mit Firmen-IBAN sind normale Geschäftsvorgänge ohne besonderen Schutz

### Private IBANs SIND personenbezogen
- **Natürliche Personen**: Einzelunternehmer, Freiberufler ohne Rechtsform
- **Beschäftigtenkontext**: Gehaltsabrechnungen, Arbeitsverträge
- **Schutzbedarf**: Art. 6 Abs. 1 DSGVO - normale Sorgfaltspflichten (nicht Hochsicherheit)

## Technische Änderungen

### 1. BANKDATEN aus RegEx-Keywords entfernt
**Datei**: `FileInventory.py` (Zeile 150-153)

**Vorher**:
```python
"BANKDATEN": {
    "keywords": ["iban", "bankverbindung", "kontonummer", ...],
    "dsgvo_kategorie": "Art. 6 Abs. 1 DSGVO - Finanzdaten",
    "schutzklasse": "hoch"
}
```

**Nachher**: Kategorie komplett entfernt mit Kommentar zur Begründung

### 2. Neue LLM-basierte Kontext-Prüfung
**Datei**: `FileInventory.py` (Zeile 699-839)

**Neue Funktion**: `check_bankdata_context_with_llm(text)`
- Analysiert den Kontext von IBANs/Kontonummern
- Unterscheidet zwischen natürlichen und juristischen Personen
- Indikatoren für Firmen: GmbH, AG, UG, KG, Handelsregister, etc.
- Indikatoren für Privatpersonen: Einzelname, Freiberufler, Gehaltsabrechnung

**Return-Wert**:
```python
{
    'contains_private_bankdata': bool,
    'confidence': str,  # 'hoch', 'mittel', 'niedrig'
    'context': str      # Begründung
}
```

### 3. Integration in classify_sensitive_data()
**Datei**: `FileInventory.py` (Zeile 912-939)

- Prüft automatisch, ob IBAN/Kontonummer im Dokument vorhanden
- Führt LLM-Analyse nur bei Bedarf durch
- Markiert nur private Bankdaten als schützenswert
- Neue Kategorie: `BANKDATEN_PRIVAT`

### 4. Präzisierung GEHALTSABRECHNUNG-Keywords
**Problem**: "netto" in "14 Tage netto" triggerte falsch-positive Treffer

**Lösung**: Keywords präzisiert
```python
# Vorher: "brutto", "netto"
# Nachher: "bruttolohn", "nettolohn", "bruttogehalt", "nettogehalt"
```

## Test-Ergebnisse

### ✅ Test 1: Geschäftsbrief einer GmbH
- **Erwartung**: NICHT schützenswert
- **Ergebnis**: Keine sensiblen Daten erkannt
- **Status**: BESTANDEN

### ✅ Test 2: Gehaltsabrechnung
- **Erwartung**: SCHÜTZENSWERT (natürliche Person)
- **Ergebnis**: BANKDATEN_PRIVAT erkannt, Schutzklasse "sehr hoch"
- **LLM-Analyse**: "Gehaltsabrechnung mit natürlicher Person" (Konfidenz: hoch)
- **Status**: BESTANDEN

### ✅ Test 3: Freiberufler-Rechnung
- **Erwartung**: SCHÜTZENSWERT (natürliche Person)
- **Ergebnis**: BANKDATEN_PRIVAT erkannt, Schutzklasse "hoch"
- **LLM-Analyse**: "Keine Rechtsform, Freiberufler" (Konfidenz: hoch)
- **Status**: BESTANDEN

### ✅ Test 4: Angebot einer AG
- **Erwartung**: NICHT schützenswert
- **Ergebnis**: Keine sensiblen Daten erkannt
- **Status**: BESTANDEN

### ✅ Test 5: Dokument ohne Bankdaten
- **Erwartung**: Keine Bankdaten
- **Ergebnis**: Keine sensiblen Daten erkannt
- **Status**: BESTANDEN

## Auswirkungen auf bestehende JSONs

Beim nächsten Durchlauf von `update_all_jsons_with_dsgvo()` werden:
- **Firmen-Dokumente** nicht mehr als schützenswert markiert (wenn nur Firmen-IBAN)
- **Private Bankdaten** weiterhin korrekt erkannt
- **Gehaltsabrechnungen** präziser erkannt (kein Fehlalarm bei "14 Tage netto")

## Performance

- **LLM-Aufruf**: Nur bei Dokumenten mit IBAN/Kontonummer
- **Timeout**: 30 Sekunden
- **Fallback**: Im Zweifel als schützenswert markieren (Sicherheitsprinzip)

## Versionierung

- **Version**: 1.19.0
- **Datum**: 2025-12-30
- **Autor**: Claude Code (mit User-Input)
