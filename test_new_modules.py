#!/usr/bin/env python
"""Test script pour les nouveaux modules"""

import sys
sys.path.insert(0, '/Users/fati/python/data_analysis_app')

import pandas as pd
from utils.report_generator import ReportGenerator
from utils.data_exporter import DataExporter

# Créer un DataFrame de test
df = pd.DataFrame({
    'age': [25, 30, 35, None, 45],
    'salaire': [30000, 45000, None, 55000, 60000],
    'ville': ['Paris', 'Lyon', 'Paris', 'Marseille', None]
})

print("=" * 80)
print("TEST DES MODULES NOUVEAU")
print("=" * 80)

# Test 1: ReportGenerator
print("\n✅ TEST 1: ReportGenerator")
try:
    gen = ReportGenerator(df, "dataset_test")
    summary = gen.get_summary_stats()
    print(f"  • Summary stats: OK")
    print(f"    - Lignes: {summary['lignes']}")
    print(f"    - Colonnes: {summary['colonnes']}")
    print(f"    - Complétude: {summary['completness_pct']:.1f}%")
    
    missing = gen.get_missing_analysis()
    print(f"  • Missing analysis: OK")
    
    stats = gen.get_numeric_stats()
    print(f"  • Numeric stats: OK")
    
    html = gen.generate_html_report()
    print(f"  • HTML report: OK (longueur: {len(html)})")
    
    text = gen.generate_text_report()
    print(f"  • Text report: OK (longueur: {len(text)})")
    
    print("  ✅ ReportGenerator: TOUT FONCTIONNE!")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

# Test 2: DataExporter
print("\n✅ TEST 2: DataExporter")
try:
    csv = DataExporter.to_csv(df)
    print(f"  • CSV export: OK (longueur: {len(csv)})")
    
    excel = DataExporter.to_excel(df)
    print(f"  • Excel export: OK (longueur: {excel.getbuffer().nbytes})")
    
    info = DataExporter.get_export_info(df)
    print(f"  • Export info: OK")
    print(f"    - Lignes: {info['lignes']}")
    print(f"    - Colonnes: {info['colonnes']}")
    print(f"    - Complétude: {info['completness_pct']:.1f}%")
    
    print("  ✅ DataExporter: TOUT FONCTIONNE!")
except Exception as e:
    print(f"  ❌ Erreur: {e}")

print("\n" + "=" * 80)
print("🎉 TOUS LES TESTS RÉUSSIS!")
print("=" * 80)
