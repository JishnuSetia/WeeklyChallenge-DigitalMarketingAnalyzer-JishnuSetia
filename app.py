import pandas as pd
import matplotlib.pyplot as plt

try:
    data = pd.read_csv("marketing_data_sample_corrected.csv")

    channel_data = {}
    for index, row in data.iterrows():
        channel_name = row["Channel Name"]
        impressions = row["Impressions"]
        clicks = row["Clicks"]
        conversions = row["Conversions"]
        total_cost = row["Total Cost"]

        if channel_name not in channel_data:
            channel_data[channel_name] = {
                "impressions": [],
                "clicks": [],
                "conversions": [],
                "total_cost": 0
            }

        channel_data[channel_name]["impressions"].append(impressions)
        channel_data[channel_name]["clicks"].append(clicks)
        channel_data[channel_name]["conversions"].append(conversions)
        channel_data[channel_name]["total_cost"] += total_cost

    channels = sorted(channel_data.keys())
    impressions_mean = [
        sum(channel_data[channel]["impressions"]) / len(channel_data[channel]["impressions"])
        for channel in channels
    ]
    clicks_mean = [
        sum(channel_data[channel]["clicks"]) / len(channel_data[channel]["clicks"])
        for channel in channels
    ]
    conversions_mean = [
        sum(channel_data[channel]["conversions"]) / len(channel_data[channel]["conversions"])
        for channel in channels
    ]
    total_cost_sum = [channel_data[channel]["total_cost"] for channel in channels]

    ctr = [
        0 if impressions == 0 else (clicks / impressions) * 100
        for clicks, impressions in zip(clicks_mean, impressions_mean)
    ]
    conversion_rate = [
        0 if clicks == 0 else (conversions / clicks) * 100 for conversions, clicks in zip(conversions_mean, clicks_mean)
    ]

    cpa = [total_cost / conversions if conversions != 0 else 0 for total_cost, conversions in zip(total_cost_sum, conversions_mean)]

    metric_combined = [(ctr_i * conversion_rate_i) / (cpa_i + 1) for ctr_i, conversion_rate_i, cpa_i in zip(ctr, conversion_rate, cpa)]

    channels_to_increase_budget = [channel for channel, metric in zip(channels, metric_combined) if metric < max(metric_combined)]

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(16, 6))

    ax1.bar(channels, impressions_mean, label="Impressions", color="blue")
    ax1.bar(channels, clicks_mean, label="Clicks", color="green")
    ax1.bar(channels, conversions_mean, label="Conversions", color="red")
    ax1.set_title("Average Impressions, Clicks, and Conversions")
    ax1.set_xlabel("Channel Name")
    ax1.set_ylabel("Average Value")
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)

    ax2.bar(channels, total_cost_sum, label="Total Cost", color="goldenrod")
    ax2.set_title("Total Cost per Channel")
    ax2.set_xlabel("Channel Name")
    ax2.set_ylabel("Total Cost")
    ax2.legend()
    ax2.tick_params(axis='x', rotation=45)

    ax3.bar(channels, ctr, label="CTR", color="purple")
    ax3.set_title("Click-Through Rate (CTR)")
    ax3.set_xlabel("Channel Name")
    ax3.set_ylabel("Percentage (%)")
    ax3.legend()
    ax3.tick_params(axis='x', rotation=45)

    ax4.bar(channels, conversion_rate, label="Conversion Rate", color="orange")
    ax4.set_title("Conversion Rate")
    ax4.set_xlabel("Channel Name")
    ax4.set_ylabel("Percentage (%)")
    ax4.legend()
    ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

    fig, (ax5) = plt.subplots(1, 1, figsize=(16, 6))
    ax5.bar(channels, metric_combined, color="skyblue")
    ax5.set_title("Combined Metric for Budget Allocation Optimization")
    ax5.set_xlabel("Channel Name")
    ax5.set_ylabel("Combined Metric")
    ax5.set_xticks(range(len(channels)))
    ax5.set_xticklabels(channels, rotation=45, ha='right')
    ax5.tick_params(axis='x', labelsize=8)

    for channel in channels_to_increase_budget:
        ax5.text(channels.index(channel), metric_combined[channels.index(channel)], "Increase Budget", ha='center', va='bottom', color='red')
    plt.show()

except FileNotFoundError:
    print("Error: File not found!")
# made by Jishnu Setia