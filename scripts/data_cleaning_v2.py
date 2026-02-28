"""
数据清洗和预处理脚本 v2
用途：整合多个指标数据源，创建完整的国家评分系统
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA_DIR = Path('./data')

class DataCleanerV2:
    def __init__(self):
        self.merged_data = None
        
    def load_all_data(self):
        """加载所有数据源"""
        print("Loading all data sources...")
        
        # 1. 生活成本和质量数据（已清洗）
        cleaned_data = pd.read_csv(DATA_DIR / 'dataset_exercise/cleaned_countries_data.csv')
        df = cleaned_data[['country_name', 'cost_of_living_index', 'cost_level']].copy()
        print(f"✓ Loaded baseline data: {len(df)} countries")
        
        # 2. 教育指数
        if (DATA_DIR / '6-education-index.csv').exists():
            education = pd.read_csv(DATA_DIR / '6-education-index.csv')
            education = education.rename(columns={'Country Name': 'country_name', 'Score': 'education_index'})
            education = education[['country_name', 'education_index']]
            df = df.merge(education, on='country_name', how='left')
            print(f"✓ Merged education index")
        
        # 3. 经济机会指数
        if (DATA_DIR / '1-economic-opportunity.csv').exists():
            economy = pd.read_csv(DATA_DIR / '1-economic-opportunity.csv')
            economy = economy.rename(columns={'Country Name': 'country_name', 'Score': 'economic_opportunity_index'})
            economy = economy[['country_name', 'economic_opportunity_index']]
            df = df.merge(economy, on='country_name', how='left')
            print(f"✓ Merged economic opportunity index")
        
        # 4. 安全指数
        if (DATA_DIR / '4-safety-index.csv').exists():
            safety = pd.read_csv(DATA_DIR / '4-safety-index.csv')
            safety = safety.rename(columns={'Country Name': 'country_name', 'Score': 'safety_index'})
            safety = safety[['country_name', 'safety_index']]
            df = df.merge(safety, on='country_name', how='left')
            print(f"✓ Merged safety index")
        
        # 5. 医疗指数
        if (DATA_DIR / '5-health-index.csv').exists():
            health = pd.read_csv(DATA_DIR / '5-health-index.csv')
            health = health.rename(columns={'Country Name': 'country_name', 'Score': 'healthcare_index'})
            health = health[['country_name', 'healthcare_index']]
            df = df.merge(health, on='country_name', how='left')
            print(f"✓ Merged healthcare index")
        
        # 6. 气候指数
        if (DATA_DIR / '8-climate-index.csv').exists():
            climate = pd.read_csv(DATA_DIR / '8-climate-index.csv')
            climate = climate.rename(columns={'Country Name': 'country_name', 'Score': 'climate_index'})
            climate = climate[['country_name', 'climate_index']]
            df = df.merge(climate, on='country_name', how='left')
            print(f"✓ Merged climate index")
        
        self.merged_data = df
        return df
    
    def normalize_to_ten_scale(self, series, old_min=None, old_max=None):
        """将指标归一化到 1-10 范围"""
        # 移除 'N/A' 和非数值
        valid_data = pd.to_numeric(series, errors='coerce')
        valid_data = valid_data.dropna()
        
        if len(valid_data) == 0:
            return series  # 全是NaN，返回原值
        
        if old_min is None:
            old_min = valid_data.min()
        if old_max is None:
            old_max = valid_data.max()
        
        # 避免除以0
        if old_max == old_min:
            return series.apply(lambda x: 5 if pd.notna(x) else np.nan)
        
        # 线性归一化到 1-10
        normalized = (valid_data - old_min) / (old_max - old_min) * 9 + 1
        
        # 将归一化结果放回原series位置
        result = series.copy()
        result[valid_data.index] = normalized
        return result
    
    def normalize_indices(self):
        """归一化所有指标到 1-10 范围"""
        print("\nNormalizing indices to 1-10 scale...")
        
        indices_to_normalize = {
            'education_index': (0, 100),
            'economic_opportunity_index': (0, 100),
            'safety_index': (0, 100),
            'healthcare_index': (0, 100),
            'climate_index': (0, 100),
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
        
        # 教育等级
        if 'education_index_normalized' in self.merged_data.columns:
            def education_level(score):
                if pd.isna(score):
                    return np.nan
                if score >= 8:
                    return 'high'
                elif score >= 5:
                    return 'medium'
                else:
                    return 'low'
            
            self.merged_data['education_level'] = self.merged_data['education_index_normalized'].apply(education_level)
            print("✓ Created education levels (high/medium/low)")
        
        # 经济机会等级
        if 'economic_opportunity_index_normalized' in self.merged_data.columns:
            def economic_level(score):
                if pd.isna(score):
                    return np.nan
                if score >= 8:
                    return 'high'
                elif score >= 5:
                    return 'medium'
                else:
                    return 'low'
            
            self.merged_data['economic_opportunity_level'] = self.merged_data['economic_opportunity_index_normalized'].apply(economic_level)
            print("✓ Created economic opportunity levels")
        
        # 安全等级
        if 'safety_index_normalized' in self.merged_data.columns:
            def safety_level(score):
                if pd.isna(score):
                    return np.nan
                if score >= 8:
                    return 'high'
                elif score >= 5:
                    return 'medium'
                else:
                    return 'low'
            
            self.merged_data['safety_level'] = self.merged_data['safety_index_normalized'].apply(safety_level)
            print("✓ Created safety levels")
        
        # 医疗等级
        if 'healthcare_index_normalized' in self.merged_data.columns:
            def healthcare_level(score):
                if pd.isna(score):
                    return np.nan
                if score >= 8:
                    return 'high'
                elif score >= 5:
                    return 'medium'
                else:
                    return 'low'
            
            self.merged_data['healthcare_level'] = self.merged_data['healthcare_index_normalized'].apply(healthcare_level)
            print("✓ Created healthcare levels")
        
        # 气候等级
        if 'climate_index_normalized' in self.merged_data.columns:
            def climate_preference(score):
                if pd.isna(score):
                    return np.nan
                if score >= 7:
                    return 'tropical'
                elif score >= 4:
                    return 'temperate'
                else:
                    return 'cold'
            
            self.merged_data['climate_preference'] = self.merged_data['climate_index_normalized'].apply(climate_preference)
            print("✓ Created climate preferences")
        
        return self.merged_data
    
    def save_to_json(self, output_file='countries.json'):
        """保存为JSON格式"""
        print(f"\nSaving to {output_file}...")
        
        # 选择需要的列
        columns_to_keep = [
            'country_name',
            'cost_of_living_index',
            'cost_level',
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
            'climate_index',
            'climate_index_normalized',
            'climate_preference',
        ]
        
        # 只保留存在的列
        export_cols = [col for col in columns_to_keep if col in self.merged_data.columns]
        export_data = self.merged_data[export_cols].copy()
        
        # 移除country_name为NaN的行
        export_data = export_data.dropna(subset=['country_name'])
        
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
        
        # 打印示例
        print("\n示例数据（前3个国家）:")
        for record in records[:3]:
            print(f"  {record['country_name']}: Education={record.get('education_level')}, "
                  f"Economy={record.get('economic_opportunity_level')}, "
                  f"Safety={record.get('safety_level')}")
        
        return records
    
    def run_pipeline(self):
        """运行完整管道"""
        print("=" * 60)
        print("数据清洗和预处理管道 v2")
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
    cleaner = DataCleanerV2()
    cleaner.run_pipeline()
