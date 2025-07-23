import pandas as pd
from scipy.stats import f_oneway
import re, os


# 현재 파일(anova.py)의 절대 경로 가져오기
base_dir = os.path.dirname(os.path.abspath(__file__))
directory = "../data/Brain_networks/Network_CC/"

# Load demographic info once
info = pd.read_excel(os.path.abspath(os.path.join(base_dir, '../data/Brain_networks/Demographic.xlsx')))
info["Participant_ID"] = info["Participant_ID"].apply(
    lambda x: int(re.findall(r"\d+", str(x))[0])
)


def read_file(fn) -> pd.DataFrame:
    """Load data from file and merge with demographic info."""
    if not fn.endswith(".xlsx"):
        fn += ".xlsx"
    df = pd.read_excel(f"{directory}{fn}")
    return df.merge(info, on="Participant_ID", how="inner")


def get_relevant_columns(df):
    """Return relevant columns excluding certain demographic and condition columns."""
    columns_to_drop = [
        "Participant_ID",
        "Sequence_name",
        "Condition_matfile",
        "Condition",
        "Averaged_CC",
        "ADHD/NT",
        "Gender",
    ]
    return df.drop(columns=columns_to_drop).columns.tolist()


def separate_adhd_nt(df: pd.DataFrame):
    """Separate dataframe into ADHD and NT groups."""
    return df[df["ADHD/NT"] == "ADHD"], df[df["ADHD/NT"] == "NT"]


def separate_via_condition(df: pd.DataFrame):
    df["Condition"] = df["Sequence_name"].apply(
        lambda x: (
            "task"
            if x == "flanker_events"
            else ("task_twitching" if x == "flanker_events_twitching" else "rest")
        )
    )
    return (
        df[df["Condition"] == "rest"],
        df[df["Condition"] == "task"],
        df[df["Condition"] == "task_twitching"],
    )


def perform_anova(df: pd.DataFrame, network: str) -> pd.DataFrame:
    """Perform ANOVA test between ADHD and NT groups for each connection."""
    df_clean = df.dropna()
    connections = get_relevant_columns(df_clean)
    adhd, nt = separate_adhd_nt(df_clean)

    # Perform ANOVA test for each connection column across years
    anova_results = [
        {
            "Feature": connection,
            "F-statistic": f_oneway(adhd[connection], nt[connection])[0],
            "p-value": f_oneway(adhd[connection], nt[connection])[1],
        }
        for connection in connections
    ]

    return pd.DataFrame(anova_results)


def filtering_anova(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out features with p-value greater than 0.05."""
    return df[df["p-value"] <= 0.05]


def log_results(
    log_file,
    network: str,
    condition_name: str,
    anova_results: pd.DataFrame,
    filtered_results: pd.DataFrame,
):
    """Log the results into the specified log file."""
    log_file.write(f"\n\n{'=' * 50}\n")
    log_file.write(
        f"ANOVA Results for {network} Network - {condition_name} Condition\n"
    )
    log_file.write(f"{'=' * 50}\n")
    log_file.write(anova_results.to_string())
    log_file.write(
        f"\n\nFiltered Results for {network} Network - {condition_name} Condition\n"
    )
    log_file.write(f"{'=' * 50}\n")
    log_file.write(filtered_results.to_string())


def print_df(df: pd.DataFrame, title: str):
    # print(f"\n------<<ANOVA Results of {network}>>------")
    print(f"\n------ {title} ------")
    print(df)


def main(networks: list, log_name: str):
    """Load data for multiple networks, perform ANOVA, and filter results."""
    rest_results, task_results, task_fidgeting_results = (
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
    )

    # Open a log file where all results will be written
    with open(f"{log_name}.txt", "w") as log_file:
        for network in networks:
            if network == "Sensorimotor":
                network_data = pd.concat(
                    [read_file(f"SenMotor_{2020 + i}") for i in range(1, 4)]
                )
            else:
                network_data = pd.concat(
                    [read_file(f"{network}_{2020 + i}") for i in range(1, 4)]
                )

            rest_df, task_df, task_fidgeting_df = separate_via_condition(network_data)

            for condition_df, condition_name in zip(
                [rest_df, task_df, task_fidgeting_df],
                ["rest", "task", "task_twitching"],
            ):
                anova_results = perform_anova(condition_df, f"{network} Network")
                filtered_results = filtering_anova(anova_results)

                # Log the results for each condition
                log_results(
                    log_file, network, condition_name, anova_results, filtered_results
                )

                # Concatenate filtered results into respective DataFrames
                if condition_name == "rest":
                    rest_results = pd.concat(
                        [rest_results, filtered_results], ignore_index=True
                    )
                elif condition_name == "task":
                    task_results = pd.concat(
                        [task_results, filtered_results], ignore_index=True
                    )
                else:
                    task_fidgeting_results = pd.concat(
                        [task_fidgeting_results, filtered_results], ignore_index=True
                    )

        log_file.write(f"\n{'=' * 50}\n")
        log_file.write(f"{'=' * 50}")

        for df, title in zip(
            [rest_results, task_results, task_fidgeting_results],
            ["Resting", "Task", "Task with Fidgeting"],
        ):
            log_file.write(f"\n------ {title} ------\n")
            log_file.write(df.to_string())

    return rest_results, task_results, task_fidgeting_results


#
# def main(networks: list):
#     """Load data for multiple networks, perform ANOVA, and filter results."""
#     rest_results = pd.DataFrame()
#     task_results = pd.DataFrame()
#     task_fidgeting_results = pd.DataFrame()
#
#     for network in networks:
#         network_data = pd.concat(
#             [read_file(f"{network}_{2020 + i}") for i in range(1, 4)]
#         )
#
#         rest_df, task_df, task_fidgeting_df = separate_via_condition(network_data)
#
#         for condition_df in [rest_df, task_df, task_fidgeting_df]:
#             anova_results = anova(condition_df, f"{network} Network")
#             filtered_results = filtering_anova(anova_results)
#
#             print_df(
#                 anova_results,
#                 f"{network} Network when {condition_df['Condition'].iloc[0]}",
#             )
#             print_df(
#                 filtered_results,
#                 f"{network} Network when {condition_df['Condition'].iloc[0]} (filtered)",
#             )
#
#             if condition_df["Condition"].iloc[0] == "rest":
#                 rest_results = pd.concat(
#                     [rest_results, filtered_results], ignore_index=True
#                 )
#             elif condition_df["Condition"].iloc[0] == "task":
#                 task_results = pd.concat(
#                     [task_results, filtered_results], ignore_index=True
#                 )
#             else:
#                 task_fidgeting_results = pd.concat(
#                     [task_fidgeting_results, filtered_results], ignore_index=True
#                 )
#     return rest_results, task_results, task_fidgeting_results
