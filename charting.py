import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

mapper = {
    "gemini-2_5-flash-preview_thinking": "Gemini 2.5 Flash",
    "gemini-2_5-pro-preview-03-25": "Gemini 2.5 Pro",
    "gemma-3-27b-it": "Gemma 3 27B",
    "o1-pro": "o1 Pro",
    "o1": "o1",
    "o4-mini-high": "o4 Mini High",
    "o3": "o3",
    "o3-mini": "o3 Mini",
    "o3-mini-high": "o3 Mini High",
    "o4-mini": "o4 Mini",
    "gpt-4_1": "GPT-4.1",
    "gpt-4_5-preview": "GPT-4.5",
    "gpt-4o-2024-11-20": "GPT-4o",
    "grok-3-mini-beta": "Grok 3 Mini Beta",
    "grok-3-beta": "Grok 3 Beta",
    "deepseek-chat-v3-0324": "DeepSeek Chat V3",
    "deepseek-r1-zero_free": "DeepSeek R1 Zero",
    "deepseek-r1": "DeepSeek R1",
    "claude-3_7-sonnet_thinking": "Claude 3.7 Sonnet Thinking",
    "claude-3_7-sonnet": "Claude 3.7 Sonnet",
    "claude-3_5-sonnet": "Claude 3.5 Sonnet",
    "llama-4-maverick": "Llama 4 Maverick",
    "qwen-max": "Qwen Max",
    "qwen-2_5-coder-32b-instruct": "Qwen 2.5 Coder",
    "mistral-large-2411": "Mistral Large",
    "codestral-2501": "Codestral 2501",
    "command-a": "Command A",
    "sonar-reasoning-pro": "Sonar Reasoning Pro",
}


def define_data(final_stats: pd.DataFrame):
    ## Define the data
    # models = ["Human level*", "GPT-4 Turbo", "Claude 3 Opus", "Mistral Large", "Gemini Pro 1.5",
    #           "Gemini Pro 1.0", "Llama 3 70B", "Mistral 8x22B"]
    # mean_scores = [80, 38, 33, 30, 29, 27, 21, 16]
    # lower_bounds = [10, 16, 15, 15, 15, 15, 13, 11]
    # upper_bounds = [10, 16, 15, 15, 15, 15, 13, 11]

    final_stats["model"] = final_stats["model"].map(mapper).fillna(final_stats["model"])
    final_stats.loc[-1] = {
        "model": "Human level*",
        "mean_score": 86,
        "std_dev_score": 0,
        "z_interval_error": 0,
        "ci_lower": 93,
        "ci_upper": 78,
    }
    final_stats = final_stats.sort_values(by="mean_score", ascending=False)

    models = final_stats["model"].to_list()
    mean_scores = final_stats["mean_score"].to_list()
    lower_bounds = final_stats["ci_lower"].to_list()
    upper_bounds = final_stats["ci_upper"].to_list()

    data = {
        "Model": models,
        "Average": mean_scores,
        "Confidence Interval Low": lower_bounds,
        "Confidence Interval High": upper_bounds,
    }
    return pd.DataFrame(data)


def create_performance_chart(
    final_stats: pd.DataFrame, title="LLM Linguistic Benchmark Performance", highlight_models=None
):
    if highlight_models is None:
        highlight_models = []

    df = define_data(final_stats)
    # Create a basic barplot
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 8))

    # Different colors for different models
    colors = ["skyblue" if model not in highlight_models else "orange" for model in df["Model"]]
    barplot = sns.barplot(data=df, y="Model", x="Average", palette=colors, errorbar=None)

    # Shade the "Human level*" bar
    for i, bar in enumerate(barplot.patches):
        if df["Model"][i] == "Human level*":
            bar.set_hatch("///")

    # Add confidence intervals (horizontal lines now)
    capwidth = 0.5
    for i, model in enumerate(df["Model"]):
        plt.plot(
            [df["Confidence Interval Low"][i], df["Confidence Interval High"][i]],
            [i, i],
            color="grey",
            lw=1,
        )
        # Caps
        plt.plot(
            [df["Confidence Interval Low"][i], df["Confidence Interval Low"][i]],
            [i - capwidth / 2, i + capwidth / 2],
            color="grey",
            lw=1,
        )
        plt.plot(
            [df["Confidence Interval High"][i], df["Confidence Interval High"][i]],
            [i - capwidth / 2, i + capwidth / 2],
            color="grey",
            lw=1,
        )

    plt.title(title, fontsize=18)
    plt.xlabel("Average Score (%)", fontsize=14)
    plt.ylabel("")
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.tight_layout()

    return barplot, plt
