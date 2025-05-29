from methods.anova import load_and_analyze_networks, read_file
import pandas as pd

# List of networks to analyze
mine_networks = ["Visual", "Salience", "FP"]
partner_networks = ["Sensorimotor", "DA", "DMN"]

network_data = pd.concat(
    [read_file(f"{mine_networks[0]}_{2020 + i}") for i in range(1, 4)]
)
print(network_data)

# # Perform ANOVA and filtering for both groups of networks
# print("Analyzing 'mine' networks...")
# anova, filtered = load_and_analyze_networks(mine_networks)
