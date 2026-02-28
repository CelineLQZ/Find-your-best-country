"""
数据清洗和预处理脚本 v3
用途：使用10个CSV数据源，整合成国家评分系统
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA_DIR = Path('./data')

class DataCleanerV3:
    def __init__(self):
        self.merged_data = None
        
    def load_all_data(self):
        """加载所有10个数据源"""
        print("Loading all 10 data sources...")
        
        # 从cost_of_living开始作为基础（通常最完整）
        cost_df = pd.read_csv(DATA_DIR / '2-cost-of-living.csv')
        df = cost_df.rename(columns={'Country Name': 'country_name', 'Score': 'cost_of_living_index'})
        df = df[['country_name', 'cost_of_living_index']].copy()
        print(f"✓ Loaded 2-cost-of-living.csv: {len(df)} countries")
        
        # 1. 经济机会
        economy = pd.read_csv(DATA_DIR / '1-economic-opportunity.csv')
        economy = economy.rename(columns={'Country Name': 'country_name', 'Score': 'economic_opportunity_index'})
        economy = economy[['country_name', 'economic_opportunity_index']]
        df = df.merge(economy, on='country_name', how='left')
        print(f"✓ Merged 1-economic-opportunity.csv")
        
        # 3. 房产价格
        property_df = pd.read_csv(DATA_DIR / '3-property-prices.csv')
        property_df = property_df.rename(columns={'Country Name': 'country_name', 'Score': 'property_price_index'})
        property_df = property_df[['country_name', 'property_price_index']]
        df = df.merge(property_df, on='country_name', how='left')
        print(f"✓ Merged 3-property-prices.csv")
        
        # 4. 安全指数
        safety = pd.read_csv(DATA_DIR / '4-safety-index.csv')
        safety = safety.rename(columns={'Country Name': 'country_name', 'Score': 'safety_index'})
        safety = safety[['country_name', 'safety_index']]
        df = df.merge(safety, on='country_name', how='left')
        print(f"✓ Merged 4-safety-index.csv")
        
        # 5. 医疗指数
        health = pd.read_csv(DATA_DIR / '5-health-index.csv')
        health = health.rename(columns={'Country Name': 'country_name', 'Score': 'healthcare_index'})
        health = health[['country_name', 'healthcare_index']]
        df = df.merge(health, on='country_name', how='left')
        print(f"✓ Merged 5-health-index.csv")
        
        # 6. 教育指数
        education = pd.read_csv(DATA_DIR / '6-education-index.csv')
        education = education.rename(columns={'Country Name': 'country_name', 'Score': 'education_index'})
        education = education[['country_name', 'education_index']]
        df = df.merge(education, on='country_name', how='left')
        print(f"✓ Merged 6-education-index.csv")
        
        # 7. 环保指数
        environment = pd.read_csv(DATA_DIR / '7-environment-index.csv')
        environment = environment.rename(columns={'Country Name': 'country_name', 'Score': 'environment_index'})
        environment = environment[['country_name', 'environment_index']]
        df = df.merge(environment, on='country_name', how='left')
        print(f"✓ Merged 7-environment-index.csv")
        
        # 8. 气候指数
        climate = pd.read_csv(DATA_DIR / '8-climate-index.csv')
        climate = climate.rename(columns={'Country Name': 'country_name', 'Score': 'climate_index'})
        climate = climate[['country_name', 'climate_index']]
        df = df.merge(climate, on='country_name', how='left')
        print(f"✓ Merged 8-climate-index.csv")
        
        # 9. 人均空乘指数
        airpass = pd.read_csv(DATA_DIR / '9-air-passengers-per-capita-index.csv')
        airpass = airpass.rename(columns={'Country Name': 'country_name', 'Score': 'air_passengers_index'})
        airpass = airpass[['country_name', 'air_passengers_index']]
        df = df.merge(airpass, on='country_name', how='left')
        print(f"✓ Merged 9-air-passengers-per-capita-index.csv")
        
        # 10. 税收指数
        tax = pd.read_csv(DATA_DIR / '10-tax-index.csv')
        tax = tax.rename(columns={'Country Name': 'country_name', 'Score': 'tax_index'})
        tax = tax[['country_name', 'tax_index']]
        df = df.merge(tax, on='country_name', how='left')
        print(f"✓ Merged 10-tax-index.csv")
        
        # 移除country_name为NaN的行
        df = df.dropna(subset=['country_name'])
        
        self.merged_data = df
        return df
    
    def normalize_to_ten_scale(self, series, old_min=None, old_max=None):
        """将指标归一化到 1-10 范围"""
        # 移除 'N/A' 和非数值
        valid_data = pd.to_numeric(series, errors='coerce')
        valid_data = valid_data.dropna()
        
        if len(valid_data) == 0:
            return series
        
        if old_min is None:
            old_min = valid_data.min()
        if old_max is None:
            old_max = valid_data.max()
        
        # 避免除以0
        if old_max == old_min:
            return series.apply(lambda x: 5 if pd.notna(x) else np.nan)
        
        # 线性归一化到 1-10
        normalized = (valid_data - old_min) / (old_max - old_min) * 9 + 1
        
        result = series.copy()
        result[valid_data.index] = normalized
        return result
    
    def normalize_indices(self):
        """归一化所有指标到 1-10 范围"""
        print("\nNormalizing indices to 1-10 scale...")
        
        indices_to_normalize = {
            'economic_opportunity_index': (0, 100),
            'property_price_index': (0, 100),
            'safety_index': (0, 100),
            'healthcare_index': (0, 100),
            'education_index': (0, 100),
            'environment_index': (0, 100),
            'climate_index': (0, 100),
            'air_passengers_index': (0, 100),
            'tax_index': (0, 100),
            'cost_of_living_index': (0, 100),
        }
        
        for col, (min_val, max_val) in indices_to_normalize.items():
            if col in self.merged_data.columns:
                self.merged_data[col + '_normalized'] = self.normalize_to_ten_scale(
                    self.merged_data[col], min_val, max_val
                )
                print(f"✓ Normalized {col}")
        
        return self.merged_data
    
    def create_preference_levels(self):
        """为用户偏好创建水平等级"""
        print("\nCreating preference levels...")
        
        def get_level(score):
            """将 1-10 分数转换为 high/medium/low"""
            if pd.isna(score):
                return None
            if score >= 7:
                return 'high'
            elif score >= 4:
                return 'medium'
            else:
                return 'low'
        
        # 教育等级
        if 'education_index_normalized' in self.merged_data.columns:
            self.merged_data['education_level'] = self.merged_data['education_index_normalized'].apply(get_level)
            print("✓ Created education_level (high/medium/low)")
        
        # 经济机会等级
        if 'economic_opportunity_index_normalized' in self.merged_data.columns:
            self.merged_data['economic_opportunity_level'] = self.merged_data['economic_opportunity_index_normalized'].apply(get_level)
            print("✓ Created economic_opportunity_level")
        
        # 安全等级
        if 'safety_index_normalized' in self.merged_data.columns:
            self.merged_data['safety_level'] = self.merged_data['safety_index_normalized'].apply(get_level)
            print("✓ Created safety_level")
        
        # 医疗等级
        if 'healthcare_index_normalized' in self.merged_data.columns:
            self.merged_data['healthcare_level'] = self.merged_data['healthcare_index_normalized'].apply(get_level)
            print("✓ Created healthcare_level")
        
        # 生活成本等级（反向：低成本更好）
        if 'cost_of_living_index_normalized' in self.merged_data.columns:
            def get_cost_level(score):
                if pd.isna(score):
                    return None
                # 反向：高分数意味着高成本，应该变成low level
                inverted_score = 11 - score  # 反向 (1-10变成10-1)
                if inverted_score >= 7:
                    return 'low'  # 便宜
                elif inverted_score >= 4:
                    return 'medium'
                else:
                    return 'high'  # 昂贵
            
            self.merged_data['cost_level'] = self.merged_data['cost_of_living_index_normalized'].apply(get_cost_level)
            print("✓ Created cost_level (low/medium/high - inverted)")
        
        # 气候偏好（基于climate_index）
        if 'climate_index_normalized' in self.merged_data.columns:
            def get_climate_preference(score):
                if pd.isna(score):
                    return None
                if score >= 8:
                    return 'tropical'  # 高分 = 温暖气候
                elif score >= 5:
                    return 'temperate'  # 中等分 = 温和气候
                else:
                    return 'cold'  # 低分 = 寒冷气候
            
            self.merged_data['climate_preference'] = self.merged_data['climate_index_normalized'].apply(get_climate_preference)
            print("✓ Created climate_preference")
        
        return self.merged_data
    
    def save_to_json(self, output_file='countries.json'):
        """保存为JSON格式"""
        print(f"\nSaving to {output_file}...")
        
        # 选择需要的列
        columns_to_keep = [
            'country_name',
            'education_index',
            'education_index_normalized',
            'education_level',
            'economic_opportunity_index',
            'economic_opportunity_index_normalized',
            'economic_opportunity_level',
            'safety_index',
            'safety_index_normalized',
            'safety_level',
            'healthcare_index',
            'healthcare_index_normalized',
            'healthcare_level',
            'cost_of_living_index',
            'cost_of_living_index_normalized',
            'cost_level',
            'climate_index',
            'climate_index_normalized',
            'climate_preference',
            'property_price_index',
            'environment_index',
            'air_passengers_index',
            'tax_index',
        ]
        
        # 只保留存在的列
        export_cols = [col for col in columns_to_keep if col in self.merged_data.columns]
        export_data = self.merged_data[export_cols].copy()
        
        # 转换为字典列表
        records = export_data.to_dict('records')
        
        # 将NaN转换为None（JSON兼容）
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        # 保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(records)} countries to {output_file}")
        
        # 打印统计信息
        print(f"\n数据覆盖统计:")
        for col in ['education_level', 'economic_opportunity_level', 'safety_level', 'healthcare_level', 'cost_level', 'climate_preference']:
            if col in self.merged_data.columns:
                non_null = self.merged_data[col].notna().sum()
                coverage = (non_null / len(self.merged_data)) * 100
                print(f"  {col}: {non_null}/{len(self.merged_data)} ({coverage:.1f}%)")
        
        # 打印示例
        print("\n示例数据（前3个国家）:")
        for record in records[:3]:
            print(f"  {record['country_name']}: Education={record.get('education_level')}, "
                  f"Economy={record.get('economic_opportunity_level')}, "
                  f"Safety={record.get('safety_level')}, Cost={record.get('cost_level')}")
        
        return records
    
    def run_pipeline(self):
        """运行完整管道"""
        print("=" * 60)
        print("数据清洗和预处理管道 v3")
        print("使用10个CSV数据源")
        print("=" * 60)
        
        self.load_all_data()
        self.normalize_indices()
        self.create_preference_levels()
        records = self.save_to_json()
        
        print("\n" + "=" * 60)
        print("✓ 数据处理完成！")
        print("=" * 60)
        
        return records

if __name__ == '__main__':
    cleaner = DataCleanerV3()
    cleaner.run_pipeline()
