import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

# 1. 连接 MySQL
password = input("请输入 MySQL root 密码: ")
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/construction_db')

# 2. 创建输出文件夹
if not os.path.exists('output'):
    os.makedirs('output')

# 3. 执行5个查询，获取数据
# Q1: 项目类型平均预算
q1 = """
SELECT project_type, COUNT(*) AS cnt, ROUND(AVG(estimated_cost)/10000,2) AS avg_budget_wan 
FROM projects GROUP BY project_type ORDER BY avg_budget_wan DESC
"""
df1 = pd.read_sql(q1, engine)

# Q2: 区域审批通过率
q2 = """
SELECT district, COUNT(*) AS total, 
SUM(CASE WHEN status='已签发' THEN 1 ELSE 0 END) AS approved, 
ROUND(SUM(CASE WHEN status='已签发' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS rate 
FROM projects GROUP BY district ORDER BY rate DESC
"""
df2 = pd.read_sql(q2, engine)

# Q3: 审批周期
q3 = """
SELECT project_type, COUNT(*) AS cnt, 
ROUND(AVG(DATEDIFF(issue_date,apply_date)),1) AS avg_days 
FROM projects WHERE status='已签发' AND issue_date IS NOT NULL 
GROUP BY project_type ORDER BY avg_days DESC
"""
df3 = pd.read_sql(q3, engine)

# Q4: 成本偏差TOP10
q4 = """
SELECT project_id, project_type, 
ROUND((actual_cost-estimated_cost)*100.0/estimated_cost,2) AS deviation_pct 
FROM projects WHERE status='已签发' 
ORDER BY deviation_pct DESC LIMIT 10
"""
df4 = pd.read_sql(q4, engine)

# Q5: 月度趋势
q5 = """
SELECT DATE_FORMAT(apply_date,'%%Y-%%m') AS month, COUNT(*) AS cnt, 
ROUND(SUM(estimated_cost)/100000000,2) AS total_budget_yi 
FROM projects GROUP BY month ORDER BY month
"""

df5 = pd.read_sql(q5, engine)

# 4. 画图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
plt.rcParams['axes.unicode_minus'] = False    # 负号显示

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1: 项目类型平均预算
axes[0,0].bar(df1['project_type'], df1['avg_budget_wan'], color='steelblue')
axes[0,0].set_title('各类型项目平均预算（万元）', fontsize=12)
axes[0,0].set_ylabel('万元')

# 图2: 区域审批通过率
axes[0,1].barh(df2['district'], df2['rate'], color='green')
axes[0,1].set_title('各区域审批通过率（%）', fontsize=12)
axes[0,1].set_xlabel('通过率 %')

# 图3: 审批周期
axes[1,0].bar(df3['project_type'], df3['avg_days'], color='orange')
axes[1,0].set_title('各类型项目平均审批周期（天）', fontsize=12)
axes[1,0].set_ylabel('天数')

# 图4: 月度申请量趋势
axes[1,1].plot(df5['month'], df5['cnt'], marker='o', color='red', label='项目数')
axes[1,1].set_title('月度申请量趋势', fontsize=12)
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].legend()

plt.tight_layout()
plt.savefig('output/analysis_report.png', dpi=150, bbox_inches='tight')
print("图表已保存：output/analysis_report.png")

engine.dispose()
