import csv
import json

# 读取CSV并转换为应用格式
countries = []
with open('data/dataset_exercise/cleaned_countries_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # 只保存有composite_score的国家（避免缺失数据多的国家）
        if row.get('composite_score') and row['composite_score'].strip():
            country = {
                'name': row['country_name'],
                'compositeScore': float(row['composite_score']),
                'costLevel': int(float(row.get('cost_level', 0))) if row.get('cost_level') else None,
                'qualityLevel': int(float(row.get('quality_level', 0))) if row.get('quality_level') else None,
                'costOfLivingIndex': float(row['cost_of_living_index']),
                'qualityOfLifeIndex': float(row.get('quality_of_life_index', 0)) if row.get('quality_of_life_index') else None,
                'safetyIndex': float(row.get('safety_index', 0)) if row.get('safety_index') else None,
                'healthcareIndex': float(row.get('healthcare_index', 0)) if row.get('healthcare_index') else None,
                'pollutionIndex': float(row.get('pollution_index', 0)) if row.get('pollution_index') else None,
                'climateIndex': float(row.get('climate_index', 0)) if row.get('climate_index') else None,
            }
            countries.append(country)

# 排序
countries.sort(key=lambda x: x['compositeScore'], reverse=True)

# 保存为JSON
with open('countries.json', 'w', encoding='utf-8') as f:
    json.dump(countries, f, indent=2, ensure_ascii=False)

print(f"✓ 成功转换 {len(countries)} 个国家的数据到 countries.json")
print(f"\n前5个国家:")
for i, c in enumerate(countries[:5], 1):
    print(f"  {i}. {c['name']} (评分: {c['compositeScore']:.2f})")
