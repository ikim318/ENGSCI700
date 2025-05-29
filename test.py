from scipy import stats

group1 = [20, 21, 19, 18, 22]
group2 = [30, 29, 31, 32, 28]

t_stat, p_value = stats.ttest_ind(group1, group2)

print(f"t-statistic: {t_stat}, p-value: {p_value}")
