from results import anova
import pandas as pd

# List of networks to analyze
mine_networks = ["Visual", "Salience", "FP"]
partner_networks = ["Sensorimotor", "DA", "DMN"]

rest, task, task_fidgeting = anova.main(mine_networks, "anova_results_log")
restb, taskb, task_fidgetingb = anova.main(partner_networks, "anova_results_log_b")

anova.print_df(rest, f"Resting")
anova.print_df(task, f"Task")
anova.print_df(task_fidgeting, f"Task with fidgeting")

# # Perform ANOVA and filtering for both groups of networks
# print("Analyzing 'mine' networks...")
# anova, filtered = load_and_analyze_networks(mine_networks)
