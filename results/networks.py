from anova import print_df, main
import pandas as pd

# List of networks to analyze
mine_networks = ["Visual", "Salience", "FP"]
partner_networks = ["Sensorimotor", "DA", "DMN"]

rest, task, task_fidgeting = main(
    mine_networks, "anova_results_log", ["_Visual", "_Salience", "_FP"]
)
restb, taskb, task_fidgetingb = main(
    partner_networks, "anova_results_log_b", ["_SenMotor", "_DA", "_DMN"]
)

print_df(rest, f"Resting")
print_df(task, f"Task")
print_df(task_fidgeting, f"Task with fidgeting")

import pandas as pd

# 각 데이터프레임에 'condition' 열 추가
rest["condition"] = "rest"
task["condition"] = "task"
task_fidgeting["condition"] = "task_fidgeting"

# 하나로 합치기
networks = pd.concat([rest, task, task_fidgeting], ignore_index=True)
networks.to_excel("significant_networks.xlsx", index=False)


# # Perform ANOVA and filtering for both groups of networks
# print("Analyzing 'mine' networks...")
# anova, filtered = load_and_analyze_networks(mine_networks)
