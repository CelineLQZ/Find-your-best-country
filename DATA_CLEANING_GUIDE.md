# 数据清洗和预处理脚本文档

## 概述

这个Python脚本用于清洗和标准化多个数据源，为国家推荐系统准备高质量的数据集。

## 功能特性

### 1. **国家名称标准化**
- 使用 `country_name.csv` 作为标准参考
- 自动清理和标准化所有数据源中的国家名称
- 处理常见的名称差异（如大小写、特殊字符等）

### 2. **数据合并**
- 合并多个CSV数据源：
  - `country_name.csv` - 国家列表
  - `cost_of_living.csv` - 生活成本数据
  - `quality_of_living.csv` - 生活质量数据
  - `economy_situation.json` - 经济数据（如果存在）

### 3. **评分系统**

#### 生活质量等级 (Quality Level: 1-10)
```
200+  → 10 (优秀)
180+  → 9  (非常好)
160+  → 8  (很好)
140+  → 7  (好)
120+  → 6  (中等)
100+  → 5  (及格)
80+   → 4  (一般)
60+   → 3  (差)
40+   → 2  (很差)
<40   → 1  (极差)
```

#### 生活成本等级 (Cost Level: 1-10)
```
100+  → 10 (最贵)
80+   → 9
60+   → 8
50+   → 7
40+   → 6
30+   → 5
25+   → 4
20+   → 3
15+   → 2
<15   → 1  (最便宜)
```

#### 收入等级评分 (Income Group Score: 1-10)
```
$50,000+   → 10 (高收入)
$30,000+   → 8  (中高收入)
$15,000+   → 6  (中等收入)
$5,000+    → 4  (中低收入)
<$5,000    → 2  (低收入)
```

### 4. **综合评分 (Composite Score)**

综合评分基于以下权重计算：

| 指标 | 权重 | 说明 |
|------|------|------|
| 生活质量等级 | 25% | 教育、医疗、安全等综合考虑 |
| 生活成本等级 | 20% | 成本越低评分越高 |
| 收入等级评分 | 20% | 经济发展水平 |
| 安全指数 | 15% | 犯罪率和社会安全 |
| 医疗指数 | 15% | 医疗服务质量 |
| 气候指数 | 5%  | 天气和气候条件 |

**综合评分 = Σ(标准化指标 × 权重)**

## 使用方法

### 前置条件

```bash
# 确保已安装必要的库
pip install pandas numpy
```

### 运行脚本

```bash
cd /Users/liceline/Desktop/personalized-country-recommender

# 方式1：直接运行
python scripts/data_cleaning.py

# 方式2：在Python中导入使用
python
>>> from scripts.data_cleaning import DataCleaner
>>> cleaner = DataCleaner()
>>> cleaned_data = cleaner.run_pipeline()
```

### 输出文件

脚本会生成以下文件到 `data/` 目录：

1. **cleaned_countries_data.csv** - 清洗后的主数据集（CSV格式）
2. **cleaned_countries_data.json** - 清洗后的数据（JSON格式）
3. **data_summary.txt** - 数据摘要报告

## 输出数据格式

### 列名说明

| 列名 | 类型 | 说明 |
|------|------|------|
| country_name | string | 国家名称 |
| cost_of_living_index | float | 生活成本指数 |
| cost_level | int | 生活成本等级 (1-10) |
| rent_index | float | 租房指数 |
| groceries_index | float | 食品杂货指数 |
| restaurant_index | float | 餐厅价格指数 |
| purchasing_power_index | float | 购买力指数 |
| quality_of_life_index | float | 生活质量指数 |
| quality_level | int | 生活质量等级 (1-10) |
| safety_index | float | 安全指数 |
| healthcare_index | float | 医疗指数 |
| pollution_index | float | 污染指数 |
| climate_index | float | 气候指数 |
| gdp | float | 国内生产总值 |
| gdp_per_capita | float | 人均GDP |
| income_group_score | int | 收入等级评分 (1-10) |
| population | int | 人口 |
| inflation | float | 通货膨胀率 |
| gni_per_capita | float | 人均国民收入 |
| composite_score | float | 综合评分 (0-10) |

## 数据质量说明

### 缺失值处理

- **删除**: 删除没有国家名称的行
- **保留**: 其他缺失值保留为 NaN，在计算时忽略

### 数据归一化

所有数值指标在创建综合评分前都会归一化到 0-10 的范围。

### 异常值

- 自动检测但不删除（保留原始数据的完整性）
- 建议在使用前进行检查

## 自定义配置

### 修改权重

编辑 `data_cleaning.py` 中的 `create_composite_score()` 方法：

```python
weights = {
    'quality_level': 0.25,        # 修改权重
    'cost_level': 0.20,
    'income_group_score': 0.20,
    'safety_index': 0.15,
    'healthcare_index': 0.15,
    'climate_index': 0.05
}
```

### 修改等级标准

编辑对应的等级函数，例如 `quality_level()`：

```python
def quality_level(score):
    """自定义生活质量等级"""
    if score >= 220:
        return 10
    # ... 其他条件
```

## 示例输出

```
60 rows × 20 columns

示例数据：
                country_name  cost_of_living_index  cost_level  quality_of_life_index  ...
0                  Austria                  71.3           8                   199.8  ...
1                 Australia                  67.9           8                   189.6  ...
2                  Bangladesh                  22.8           2                    73.3  ...
...
```

## 故障排除

### 问题1：找不到CSV文件
**解决方案**：确保所有数据文件都在 `data/` 目录中

### 问题2：国家名称不匹配
**解决方案**：
- 检查 `country_name.csv` 中的名称拼写
- 在 `name_mapping` 字典中添加映射关系

### 问题3：缺失值过多
**解决方案**：
- 检查源数据文件的格式
- 运行 `save_summary_report()` 查看各列的数据覆盖率

## 下一步

1. 将 `cleaned_countries_data.csv` 导入到推荐系统
2. 根据 `composite_score` 重新训练推荐算法
3. 进行A/B测试验证推荐准确度的改进

## 许可证

MIT License
