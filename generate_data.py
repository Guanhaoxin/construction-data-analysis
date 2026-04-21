import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n = 1000

project_types = ['住宅', '商业', '市政', '工业', '仓储']
districts = ['天河区', '白云区', '黄埔区', '番禺区', '海珠区']
status_list = ['已签发', '审批中', '已驳回', '已过期']

data = {
    'project_id': [f'P{i:04d}' for i in range(1, n+1)],
    'project_type': np.random.choice(project_types, n),
    'district': np.random.choice(districts, n),
    'apply_date': [datetime(2023,1,1) + timedelta(days=int(x)) for x in np.random.randint(0, 730, n)],
    'estimated_cost': np.random.randint(50, 5000, n) * 10000,  # 预算：50万-5000万
    'area_sqm': np.random.randint(200, 50000, n),
}

df = pd.DataFrame(data)

# 生成状态（已签发占60%，审批中20%，已驳回15%，已过期5%）
df['status'] = np.random.choice(status_list, n, p=[0.6, 0.2, 0.15, 0.05])

# 已签发的才有实际成本和签发日期
df['actual_cost'] = np.where(
    df['status'] == '已签发',
    (df['estimated_cost'] * np.random.uniform(0.8, 1.4, n)).astype(int),
    np.nan
)
df['issue_date'] = np.where(
    df['status'] == '已签发',
    df['apply_date'] + pd.to_timedelta(np.random.randint(10, 120, n), unit='D'),
    pd.NaT
)

df.to_csv('projects.csv', index=False, encoding='utf-8-sig', na_rep='\\N')

print("生成完成：projects.csv")

