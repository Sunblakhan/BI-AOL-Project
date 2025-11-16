import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the dark teal color
DARK_TEAL_COLOR = "#008080"

# Assuming df_top5 contains the results of the final Question 3 SQL query
# Load data (if not already loaded in the environment)
try:
    df_top5 = pd.read_csv("./data/question3-data.csv")
    df_top5.columns = df_top5.columns.str.strip()
    df_top5["CATEGORY"] = df_top5["CATEGORY"].astype(str).str.strip()
    df_top5 = df_top5.sort_values(
        by=["CATEGORY", "DOMAIN_RANK_WITHIN_CATEGORY"], ascending=[True, True]
    )
except FileNotFoundError:
    print("Error: The file './data/question3-data.csv' was not found.")
    exit()

# ----------------------------------------------------------------------
# SMALL MULTIPLES VERTICAL RANKED BAR CHART (with Independent Y-Scales)
# ----------------------------------------------------------------------

plt.figure(figsize=(15, 12))

g = sns.catplot(
    data=df_top5,
    # X-axis is the domain name
    x="THISDOMAIN",
    # Y-axis is the magnitude (Clicks)
    y="DOMAIN_CLICK_COUNT",
    # Facet by Category
    col="CATEGORY",
    kind="bar",
    color=DARK_TEAL_COLOR,
    col_wrap=2,  # Layout for 2 charts per row
    height=4,
    aspect=2,
    # CRITICAL FIX: Allows each chart to have its own Y-axis range
    sharey=False,
    # CRITICAL FIX: Ensures X-axis labels (domains) are unique per plot
    sharex=False,
)

# 1. FIX THE Y-AXIS SCALE ISSUE (Visibility for small categories)
# 2. FIX THE X-AXIS LABEL ISSUE (Readability)

for ax in g.axes.flatten():
    # Rotate X-axis labels (Domains) for readability
    ax.tick_params(axis="x", rotation=90)

    # Add a title to show the current category being displayed
    ax.set_title(ax.get_title(), fontsize=12)

    # Optional: Clean up the Y-axis label (Seaborn repeats it)
    ax.set_ylabel("Total Clicks (High Intent)", fontsize=10)
    ax.set_xlabel("Domain", fontsize=10)

g.fig.suptitle(
    "Top 5 Clicked Domains Ranked by Digital Commerce Category", y=1.02, fontsize=18
)
plt.subplots_adjust(hspace=0.6, wspace=0.2)  # Adjust spacing between charts

plt.savefig(
    "question3/q3_small_multiples_vertical_independent_scale.png", bbox_inches="tight"
)
plt.close()

print(
    "Successfully generated q3_small_multiples_vertical_independent_scale.png with fixed scales and readable labels."
)
