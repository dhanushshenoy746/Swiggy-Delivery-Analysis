import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the lightweight dataset (~800 KB)
df = pd.read_csv("swiggy.csv")
print("Columns:", df.columns.tolist())
print(df.head())

# ---------------------------------------------------------
# 2. Data Cleaning
# ---------------------------------------------------------
df.drop_duplicates(inplace=True)

# Ensure numeric columns are properly formatted
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Avg ratings"] = pd.to_numeric(df["Avg ratings"], errors="coerce")
df["Delivery time"] = pd.to_numeric(df["Delivery time"], errors="coerce")

df.dropna(subset=["City", "Price", "Avg ratings", "Delivery time"], inplace=True)

# ---------------------------------------------------------
# 3. Feature Engineering (Price Segments)
# ---------------------------------------------------------
df["Price_Tier"] = pd.cut(
    df["Price"],
    bins=[0, 250, 500, 10000],
    labels=["Budget (<=₹250)", "Mid-Range (₹251-500)", "Premium (>₹500)"],
)

print(f"\nClean Restaurants: {len(df)}")
print(f"Avg Rating: {df['Avg ratings'].mean():.2f} | Avg Delivery: {df['Delivery time'].mean():.1f} mins")

# ---------------------------------------------------------
# 4. Three Focused Seaborn Visualizations
# ---------------------------------------------------------
sns.set_theme(style="whitegrid")

# Chart 1: Average Delivery Time Across Top 8 Cities
plt.figure(figsize=(9, 5))
top_cities = df["City"].value_counts().head(8).index
df_top = df[df["City"].isin(top_cities)]

sns.barplot(
    data=df_top,
    x="City",
    y="Delivery time",
    estimator=np.mean,
    errorbar=None,
    palette="Blues_d",
)
plt.title("Average Swiggy Delivery Time Across Major Indian Cities")
plt.xlabel("City")
plt.ylabel("Avg Delivery Time (Minutes)")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("chart1_city_delivery_time.png", dpi=300)
plt.show()

# Chart 2: Customer Ratings Across Price Tiers
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Price_Tier", y="Avg ratings", palette="Set2")
plt.title("Customer Ratings Across Restaurant Price Tiers")
plt.xlabel("Price Tier")
plt.ylabel("Average Rating (out of 5)")
plt.tight_layout()
plt.savefig("chart2_price_vs_rating.png", dpi=300)
plt.show()

# Chart 3: Does Longer Delivery Time Lower Ratings?
plt.figure(figsize=(8, 5))
sns.regplot(
    data=df.sample(min(1000, len(df)), random_state=42),
    x="Delivery time",
    y="Avg ratings",
    scatter_kws={"alpha": 0.4},
    line_kws={"color": "red"},
)
plt.title("Delivery Time vs. Customer Rating Trend")
plt.xlabel("Delivery Time (Minutes)")
plt.ylabel("Average Rating (out of 5)")
plt.tight_layout()
plt.savefig("chart3_delivery_vs_rating.png", dpi=300)
plt.show()