-- Q1: 项目类型平均预算
SELECT project_type, COUNT(*) AS cnt, ROUND(AVG(estimated_cost)/10000,2) AS avg_budget_wan FROM projects GROUP BY project_type ORDER BY avg_budget_wan DESC;

-- Q2: 区域审批通过率
SELECT district, COUNT(*) AS total, SUM(CASE WHEN status='已签发' THEN 1 ELSE 0 END) AS approved, ROUND(SUM(CASE WHEN status='已签发' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS rate FROM projects GROUP BY district ORDER BY rate DESC;

-- Q3: 审批周期
SELECT project_type, COUNT(*) AS cnt, ROUND(AVG(DATEDIFF(issue_date,apply_date)),1) AS avg_days FROM projects WHERE status='已签发' AND issue_date IS NOT NULL GROUP BY project_type ORDER BY avg_days DESC;

-- Q4: 成本偏差TOP10
SELECT project_id, project_type, ROUND(estimated_cost/10000,2) AS budget_wan, ROUND(actual_cost/10000,2) AS actual_wan, ROUND((actual_cost-estimated_cost)*100.0/estimated_cost,2) AS deviation_pct FROM projects WHERE status='已签发' ORDER BY deviation_pct DESC LIMIT 10;

-- Q5: 月度趋势
SELECT DATE_FORMAT(apply_date,'%Y-%m') AS month, COUNT(*) AS cnt, ROUND(SUM(estimated_cost)/100000000,2) AS total_budget_yi FROM projects GROUP BY month ORDER BY month;
