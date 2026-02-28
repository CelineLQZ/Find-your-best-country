"""
数据清洗和预处理脚本
用途：标准化国家名称，合并多个数据源，创建评分系统
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# 设置数据目录
DATA_DIR = Path('./data')

class DataCleaner:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        self.countries_name = None
        self.quality_of_living = None
        self.cost_of_living = None
        self.economy_data = None
        self.merged_data = None
        
    def load_data(self):
        """加载所有CSV文件"""
        print("Loading data...")
        
        # 加载国家名称（作为标准参考）
        country_name_file = self.data_dir / 'country_name.csv'
        if country_name_file.exists():
            self.countries_name = pd.read_csv(country_name_file)
            print(f"✓ Loaded {len(self.countries_name)} countries from country_name.csv")
        else:
            print("⚠ country_name.csv not found")
        
        # 加载生活质量数据
        quality_file = self.data_dir / 'quality_of_living.csv'
        if quality_file.exists():
            self.quality_of_living = pd.read_csv(quality_file)
            print(f"✓ Loaded quality_of_living.csv ({len(self.quality_of_living)} records)")
        else:
            print("⚠ quality_of_living.csv not found")
        
        # 加载生活成本数据
        cost_file = self.data_dir / 'cost_of_living.csv'
        if cost_file.exists():
            self.cost_of_living = pd.read_csv(cost_file)
            print(f"✓ Loaded cost_of_living.csv ({len(self.cost_of_living)} records)")
        else:
            print("⚠ cost_of_living.csv not found")
        
        # 加载经济数据（如果存在）
        economy_file = self.data_dir / 'economy_situation.json'
        if economy_file.exists():
            self.economy_data = pd.read_json(economy_file)
            print(f"✓ Loaded economy_situation.json ({len(self.economy_data)} records)")
        else:
            print("⚠ economy_situation.json not found")
    
    def standardize_country_names(self):
        """
        标准化国家名称
        创建国家名称映射表，处理不同数据源的国家名称差异
        """
        print("\nStandardizing country names...")
        
        # 创建标准国家名称列表
        standard_countries = self.countries_name['country_name'].str.strip().str.title().tolist()
        
        # 创建清洁映射字典（处理常见的名称差异）
        name_mapping = {
            'Czech Republic': 'Czech Republic',
            'North Macedonia': 'North Macedonia',
            'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
            'Hong Kong': 'Hong Kong',
            'United States': 'United States',
            'United Kingdom': 'United Kingdom',
            'Puerto Rico': 'Puerto Rico',
            'United Arab Emirates': 'United Arab Emirates',
            'South Korea': 'South Korea',
            'South Africa': 'South Africa',
            'Costa Rica': 'Costa Rica',
            'El Salvador': 'El Salvador',
            'New Zealand': 'New Zealand',
            'Sri Lanka': 'Sri Lanka',
            'Trinidad and Tobago': 'Trinidad and Tobago',
        }
        
        return standard_countries, name_mapping
    
    def clean_quality_of_living(self):
        """清洗生活质量数据"""
        print("\nCleaning quality_of_living data...")
        
        if self.quality_of_living is None:
            return None
        
        df = self.quality_of_living.copy()
        
        # 标准化国家名称
        df['Country'] = df['Country'].str.strip().str.title()
        
        # 创建等级评分函数
        def quality_level(score):
            """将生活质量指数转换为等级（1-10）"""
            if score >= 200:
                return 10
            elif score >= 180:
                return 9
            elif score >= 160:
                return 8
            elif score >= 140:
                return 7
            elif score >= 120:
                return 6
            elif score >= 100:
                return 5
            elif score >= 80:
                return 4
            elif score >= 60:
                return 3
            elif score >= 40:
                return 2
            else:
                return 1
        
        # 添加等级列
        df['Quality_Level'] = df['Quality of Life Index'].apply(quality_level)
        
        # 选择关键列
        df_clean = df[['Country', 'Quality of Life Index', 'Quality_Level',
                       'Safety Index', 'Health Care Index', 'Pollution Index', 
                       'Climate Index']].copy()
        
        # 重命名列
        df_clean.columns = ['country_name', 'quality_of_life_index', 'quality_level',
                            'safety_index', 'healthcare_index', 'pollution_index', 
                            'climate_index']
        
        # 标准化数值
        df_clean['quality_of_life_index'] = df_clean['quality_of_life_index'].round(2)
        df_clean['safety_index'] = df_clean['safety_index'].round(2)
        df_clean['healthcare_index'] = df_clean['healthcare_index'].round(2)
        
        print(f"✓ Cleaned {len(df_clean)} quality_of_living records")
        return df_clean
    
    def clean_cost_of_living(self):
        """清洗生活成本数据"""
        print("\nCleaning cost_of_living data...")
        
        if self.cost_of_living is None:
            return None
        
        df = self.cost_of_living.copy()
        
        # 标准化国家名称
        df['Country'] = df['Country'].str.strip().str.title()
        
        # 创建成本等级函数
        def cost_level(index):
            """
            将生活成本指数转换为等级（1-10）
            1=最便宜，10=最贵
            """
            if index >= 100:
                return 10
            elif index >= 80:
                return 9
            elif index >= 60:
                return 8
            elif index >= 50:
                return 7
            elif index >= 40:
                return 6
            elif index >= 30:
                return 5
            elif index >= 25:
                return 4
            elif index >= 20:
                return 3
            elif index >= 15:
                return 2
            else:
                return 1
        
        # 添加等级列
        df['Cost_Level'] = df['Cost of Living Index'].apply(cost_level)
        
        # 选择关键列
        df_clean = df[['Country', 'Cost of Living Index', 'Cost_Level',
                       'Rent Index', 'Groceries Index', 'Restaurant Price Index',
                       'Local Purchasing Power Index']].copy()
        
        # 重命名列
        df_clean.columns = ['country_name', 'cost_of_living_index', 'cost_level',
                            'rent_index', 'groceries_index', 'restaurant_index',
                            'purchasing_power_index']
        
        # 标准化数值
        for col in df_clean.columns[1:]:
            if col != 'cost_level':
                df_clean[col] = df_clean[col].round(2)
        
        print(f"✓ Cleaned {len(df_clean)} cost_of_living records")
        return df_clean
    
    def clean_economy_data(self):
        """清洗经济数据"""
        print("\nCleaning economy data...")
        
        if self.economy_data is None:
            return None
        
        df = self.economy_data.copy()
        
        # 标准化国家名称
        if 'country_name' in df.columns:
            df['country_name'] = df['country_name'].str.strip().str.title()
        
        # 创建收入等级评分
        def income_group_score(gdp_per_capita):
            """
            基于人均GDP分类收入等级
            """
            if pd.isna(gdp_per_capita):
                return None
            
            if gdp_per_capita >= 50000:
                return 10  # 高收入
            elif gdp_per_capita >= 30000:
                return 8   # 中高收入
            elif gdp_per_capita >= 15000:
                return 6   # 中等收入
            elif gdp_per_capita >= 5000:
                return 4   # 中低收入
            else:
                return 2   # 低收入
        
        # 添加收入等级列
        df['income_group_score'] = df['gdp_per_capita'].apply(income_group_score)
        
        # 选择关键列
        if 'gdp_per_capita' in df.columns:
            df_clean = df[['country_name', 'gdp', 'gdp_per_capita', 'income_group_score',
                           'population', 'inflation', 'gni_per_capita']].copy()
        else:
            df_clean = df.copy()
        
        # 处理缺失值
        df_clean = df_clean.dropna(subset=['country_name'])
        
        # 标准化数值
        numeric_cols = ['gdp', 'gdp_per_capita', 'population', 'inflation', 'gni_per_capita']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').round(2)
        
        print(f"✓ Cleaned {len(df_clean)} economy records")
        return df_clean
    
    def merge_all_data(self):
        """合并所有数据源"""
        print("\nMerging all data sources...")
        
        # 清洗各个数据源
        quality_clean = self.clean_quality_of_living()
        cost_clean = self.clean_cost_of_living()
        economy_clean = self.clean_economy_data()
        
        # 从cost_of_living开始作为基础（通常数据最完整）
        merged = cost_clean.copy() if cost_clean is not None else None
        
        # 合并生活质量数据
        if merged is not None and quality_clean is not None:
            merged = merged.merge(
                quality_clean, 
                on='country_name', 
                how='outer'
            )
        elif quality_clean is not None:
            merged = quality_clean.copy()
        
        # 合并经济数据
        if merged is not None and economy_clean is not None:
            merged = merged.merge(
                economy_clean, 
                on='country_name', 
                how='outer'
            )
        elif economy_clean is not None:
            merged = economy_clean.copy()
        
        # 清理重复列
        merged = merged.loc[:, ~merged.columns.duplicated()]
        
        # 排序
        merged = merged.sort_values('country_name').reset_index(drop=True)
        
        self.merged_data = merged
        print(f"✓ Merged data: {len(merged)} countries, {len(merged.columns)} features")
        
        return merged
    
    def create_composite_score(self):
        """创建综合评分"""
        print("\nCreating composite score...")
        
        if self.merged_data is None:
            print("⚠ No merged data available")
            return self.merged_data
        
        df = self.merged_data.copy()
        
        # 权重设置
        weights = {
            'quality_level': 0.25,           # 生活质量：25%
            'cost_level': 0.20,              # 生活成本：20%（成本越低越好，所以需要反向）
            'income_group_score': 0.20,      # 收入水平：20%
            'safety_index': 0.15,            # 安全指数：15%
            'healthcare_index': 0.15,        # 医疗指数：15%
            'climate_index': 0.05             # 气候指数：5%
        }
        
        # 初始化综合分数
        df['composite_score'] = 0
        
        # 标准化各个指标到0-10分
        for col, weight in weights.items():
            if col in df.columns:
                # 检查是否有非null值
                if df[col].notna().sum() > 0:
                    # 获取有效数据的最小和最大值
                    valid_data = df[col].dropna()
                    if len(valid_data) > 0:
                        min_val = valid_data.min()
                        max_val = valid_data.max()
                        
                        # 处理特殊情况：cost_level需要反向（成本越低越好）
                        if col == 'cost_level':
                            normalized = 10 - ((df[col] - min_val) / (max_val - min_val + 1) * 10)
                        else:
                            normalized = (df[col] - min_val) / (max_val - min_val + 1) * 10
                        
                        df['composite_score'] += normalized * weight
                    else:
                        print(f"  ⚠ No valid data for {col}")
        
        # 四舍五入到两位小数
        df['composite_score'] = df['composite_score'].round(2)
        
        print("✓ Composite score created")
        return df
    
    def save_cleaned_data(self, output_filename='cleaned_countries_data.csv'):
        """保存清洗后的数据"""
        print(f"\nSaving cleaned data to {output_filename}...")
        
        if self.merged_data is None:
            print("⚠ No merged data to save")
            return
        
        output_path = self.data_dir / output_filename
        self.merged_data.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✓ Data saved to {output_path}")
    
    def save_summary_report(self, output_filename='data_summary.txt'):
        """保存数据摘要报告"""
        print(f"\nGenerating summary report...")
        
        if self.merged_data is None:
            print("⚠ No data to summarize")
            return
        
        output_path = self.data_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("数据清洗和预处理摘要报告\n")
            f.write("=" * 60 + "\n\n")
            
            # 基本统计信息
            f.write("1. 数据概览\n")
            f.write("-" * 60 + "\n")
            f.write(f"总国家数: {len(self.merged_data)}\n")
            f.write(f"总特征数: {len(self.merged_data.columns)}\n")
            f.write(f"缺失值: {self.merged_data.isnull().sum().sum()}\n\n")
            
            # 列信息
            f.write("2. 数据列信息\n")
            f.write("-" * 60 + "\n")
            for col in self.merged_data.columns:
                non_null = self.merged_data[col].notna().sum()
                f.write(f"{col}: {non_null}/{len(self.merged_data)} ({non_null/len(self.merged_data)*100:.1f}%)\n")
            f.write("\n")
            
            # 统计指标
            f.write("3. 关键指标统计\n")
            f.write("-" * 60 + "\n")
            for col in ['quality_level', 'cost_level', 'income_group_score', 'composite_score']:
                if col in self.merged_data.columns:
                    stats = self.merged_data[col].describe()
                    f.write(f"\n{col}:\n")
                    f.write(f"  平均值: {stats['mean']:.2f}\n")
                    f.write(f"  中位数: {stats['50%']:.2f}\n")
                    f.write(f"  最小值: {stats['min']:.2f}\n")
                    f.write(f"  最大值: {stats['max']:.2f}\n")
            
            # 顶部和底部国家
            if 'composite_score' in self.merged_data.columns:
                f.write("\n4. 综合评分排名\n")
                f.write("-" * 60 + "\n")
                f.write("前10名:\n")
                top10 = self.merged_data.nlargest(10, 'composite_score')[['country_name', 'composite_score']]
                for idx, row in top10.iterrows():
                    f.write(f"  {row['country_name']}: {row['composite_score']}\n")
                
                f.write("\n底部10名:\n")
                bottom10 = self.merged_data.nsmallest(10, 'composite_score')[['country_name', 'composite_score']]
                for idx, row in bottom10.iterrows():
                    f.write(f"  {row['country_name']}: {row['composite_score']}\n")
        
        print(f"✓ Report saved to {output_path}")
    
    def run_pipeline(self):
        """执行完整的数据处理管道"""
        print("\n" + "=" * 60)
        print("开始数据清洗和预处理管道")
        print("=" * 60)
        
        # 1. 加载数据
        self.load_data()
        
        # 2. 合并数据
        self.merge_all_data()
        
        # 3. 创建综合评分
        self.merged_data = self.create_composite_score()
        
        # 4. 保存结果
        self.save_cleaned_data('cleaned_countries_data.csv')
        self.save_cleaned_data('cleaned_countries_data.json')
        self.save_summary_report()
        
        print("\n" + "=" * 60)
        print("✓ 数据处理完成！")
        print("=" * 60)
        
        return self.merged_data


if __name__ == "__main__":
    # 创建清洁器实例并运行
    cleaner = DataCleaner()
    cleaned_data = cleaner.run_pipeline()
    
    # 显示处理结果示例
    print("\n数据示例（前5行）:")
    print(cleaned_data.head().to_string())
    
    print("\n列名列表:")
    print(cleaned_data.columns.tolist())
