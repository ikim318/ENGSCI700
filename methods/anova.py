import pandas as pd
from scipy.stats import f_oneway
import re

directory = "../data/Brain_networks/Network_CC/"

# Load demographic info once
info = pd.read_excel(f"../data/Brain_networks/Demographic.xlsx")
info["Participant_ID"] = info["Participant_ID"].apply(
    lambda x: int(re.findall(r"\d+", str(x))[0])
)
# info = info.drop_duplicates(subset='Participant_ID').reset_index(drop=True)


def read_file(fn) -> pd.DataFrame:
    """Load data from file and merge with demographic info."""
    if fn[-4:] != "xlsx":
        fn += ".xlsx"
    df = pd.read_excel(f"{directory}{fn}")
    return df.merge(info, on="Participant_ID", how="inner")


def get_relevant_columns(df):
    """Return relevant columns excluding certain demographic and condition columns."""
    return df.drop(
        columns=[
            "Participant_ID",
            "Sequence_name",
            "Condition_matfile",
            "Condition",
            "Averaged_CC",
            "ADHD/NT",
            "Gender",
        ]
    ).columns.tolist()


def separate_adhd_nt(df: pd.DataFrame):
    """Separate dataframe into ADHD and NT groups."""
    return df[df["ADHD/NT"] == "ADHD"], df[df["ADHD/NT"] == "NT"]


def separate_via_condition(df: pd.DataFrame):

    return df


def anova(df: pd.DataFrame, network: str) -> pd.DataFrame:
    """Perform ANOVA test between ADHD and NT groups for each connection."""
    df_clean = df.dropna()
    connections = get_relevant_columns(df_clean)
    adhd, nt = separate_adhd_nt(df_clean)

    # Perform ANOVA test for each connection column across years
    anova_results = []
    for connection in connections:
        f, p = f_oneway(adhd[connection], nt[connection])
        anova_results.append({"Feature": connection, "F-statistic": f, "p-value": p})

    anova_df = pd.DataFrame(anova_results)
    return anova_df


def filtering_anova(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out features with p-value greater than 0.05."""
    return df[df["p-value"] <= 0.05]


def print_df(df: pd.DataFrame, title):
    # print(f"\n------<<ANOVA Results of {network}>>------")
    print(f"\n------<<{title}>>------")
    print(df)


def load_and_analyze_networks(networks: list):
    """Load data for multiple networks, perform ANOVA, and filter results."""
    results = []
    for network in networks:
        if network == "Sensorimotor":
            network_data = pd.concat(
                [read_file(f"SenMotor_{2020 + i}") for i in range(1, 4)]
            )
        else:
            network_data = pd.concat(
                [read_file(f"{network}_{2020 + i}") for i in range(1, 4)]
            )
        anova_results = anova(network_data, f"{network} Network")
        filtered_results = filtering_anova(anova_results)

        return anova_results, filtered_results


# if __name__ == "__main__":
#     # List of networks to analyze
#     mine_networks = ["Visual", "Salience", "FP"]
#     partner_networks = ["Sensorimotor", "DA", "DMN"]
#
#     # Perform ANOVA and filtering for both groups of networks
#     print("Analyzing 'mine' networks...")
#     load_and_analyze_networks(mine_networks)
#
#     print("=" * 47)
#
#     print("Analyzing 'partner' networks...")
#     load_and_analyze_networks(partner_networks)


# def anova_result():
#     # visual = pd.concat([read_file(f"Visual_202{i}") for i in range(1, 4)])
#     # visual_df = anova(visual, "Visual Network")
#     # print("=" * 47)
#     # salience = pd.concat([read_file(f"Salience_202{i}") for i in range(1, 4)])
#     # salience_df = anova(salience, "Salience Network")
#     # print("=" * 47)
#     # FP = pd.concat([read_file(f"FP_202{i}") for i in range(1, 4)])
#     # fp_df = anova(FP, "FrontoParietal Network")
#     # return visual_df, salience_df, fp_df
#     sensorimotor = pd.concat([read_file(f"SenMotor_202{i}") for i in range(1, 4)])
#     sensorimotor_df = anova(sensorimotor, "Sensorimotor Network")
#     print("=" * 47)
#     dorsal = pd.concat([read_file(f"DA_202{i}") for i in range(1, 4)])
#     dorsal_df = anova(dorsal, "Dorsal Network")
#     print("=" * 47)
#     DMN = pd.concat([read_file(f"DMN_202{i}") for i in range(1, 4)])
#     dmn_df = anova(DMN, "DMN Network")
#     return sensorimotor_df, dorsal_df, dmn_df
#
#
#
# me = ["visual", "salience", "fp"]
# partner = ["sensorimotor", "DA", "DMN"]
# def mine():
#     visual_df, salience_df, fp_df = anova_result()
#
#     visual_filter = filtering_anova(visual_df)
#     print(f"\n-Visual Network-\n{visual_filter}")
#     salience_filter = filtering_anova(salience_df)
#     print(f"\n-Salience Network-\n{salience_filter}")
#     fp_filter = filtering_anova(fp_df)
#     print(f"\n-FrontoParietal Network-\n{fp_filter}")
#
# def partner():
#     sensorimotor_df, dorsal_df, dmn_df = anova_result()
#
#     sensorimotor_filter = filtering_anova(sensorimotor_df)
#     print(f"\n-Sensorimotor Network-\n{sensorimotor_filter}")
#     dorsal_filter = filtering_anova(dorsal_df)
#     print(f"\n-Dorsal Network-\n{dorsal_filter}")
#     dmn_filter = filtering_anova(dmn_df)
#     print(f"\n-DMN Network-\n{dmn_filter}")
#
# if __name__ == "__main__":
#     # mine()
#     partner()
