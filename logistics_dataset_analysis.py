import pandas as pd
#-------------------------------------------------
#PROJECT 1_ Strategic Planning
#-------------------------------------------------

#1. Load the logistics dataset
df = pd.read_csv("C:/Users/singh/OneDrive/Desktop/Logistics Data Analysis Project/Dataset/Delivery_Logistics.csv")

#Conversion of Delayed column datatype from string to boolean to get the actual numbers
df["delayed"] = df["delayed"].astype(str).str.strip().str.lower().map({
    "yes": True,
    "no": False
})

#2. Dataset dimensions
print("Dataset Shape:", df.shape)

#3. Calling the first five values
print("\nFirst five records:")
print(df.head(5))

#4. Calling all the column names
print("\nColumn Names:")
print(df.columns)

#5. Calling Dataset Information
print("\nDataset Information:")
df.info()

#6. Checking missing values
print("\nMissing Values:")
print(df.isnull().sum())

#7. Checking Duplicate values
print("\nDuplicate Values:")
print(df.duplicated().sum())

#8. Checking unique values per column
print("\nUnique Values Per Column:")
for column in df.columns:
    print(column, ":", df[column].nunique())

#9. Analysis of Base KPI's
total_deliveries = len(df)
delayed_deliveries = df["delayed"].sum()

delay_rate = (delayed_deliveries / total_deliveries) * 100
non_delay_rate = 100 - delay_rate

average_cost = df["delivery_cost"].mean()
average_distance = df["distance_km"].mean()
average_rating = df["delivery_rating"].mean()

print("\n========== BASE KPIs ==========")

print("Total Deliveries:", total_deliveries)
print("Delayed Deliveries:", delayed_deliveries)
print("Delay Rate:", round(delay_rate, 2), "%")
print("Non-Delay Rate:", round(non_delay_rate, 2), "%")
print("Average Delivery Cost:", round(average_cost, 2))
print("Average Distance:", round(average_distance, 2), "km")
print("Average Customer Rating:", round(average_rating, 2))


#KPI Comparison
print("\n========== KPI Comparison ==========")

kpi_comparison = df.groupby("delayed").agg(
    average_cost=("delivery_cost", "mean"),
    average_distance=("distance_km", "mean"),
    average_rating=("delivery_rating", "mean"),
    number_of_deliveries=("delivery_id", "count")
)

print(kpi_comparison)

#10. Analysis of delays by important variables

#10.1 Does weather influences delays?
print("\n========== Delay Rate by Weather ==========")

weather_delay = (
    df.groupby("weather_condition")["delayed"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(weather_delay)

#10.2 Delay Rate by Delivery Mode
print("\n========== Delay Rate by Delivery Mode ==========")

mode_delay = (
    df.groupby("delivery_mode")["delayed"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(mode_delay)

#10.3 Delay Rate by Vehicle type
print("\n========== Delay Rate by Vehicle Type ==========")

vehicle_delay = (
    df.groupby("vehicle_type")["delayed"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(vehicle_delay)

#10.4 Delay Rate by Region
print("\n========== Delay Rate by Region ==========")

region_delay = (
    df.groupby("region")["delayed"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(region_delay)

#10.5 Delay Rate by Delivery Partner
print("\n========== Delay Rate by Delivery Partner ==========")

partner_delay = (
    df.groupby("delivery_partner")["delayed"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(partner_delay)

#10.6 Does Distance Affects Delay rates
print("\n========== Distance Analysis ==========")

distance_comparison = df.groupby("delayed")["distance_km"].agg(
    ["mean", "median", "min", "max"]
)

print(distance_comparison)

#10.7 Does package weight affects delay rates
print("\n========== Package Weight Analysis ==========")

weight_comparison = df.groupby("delayed")["package_weight_kg"].agg(
    ["mean", "median", "min", "max"]
)

print(weight_comparison)

# Save KPI comparison
kpi_comparison.to_csv(
    "../Project_1_Strategic_Planning/kpi_comparison.csv"
)

# Save delay rates by major categories
weather_delay.to_csv(
    "../Project_1_Strategic_Planning/weather_delay_rate.csv"
)

mode_delay.to_csv(
    "../Project_1_Strategic_Planning/mode_delay_rate.csv"
)

vehicle_delay.to_csv(
    "../Project_1_Strategic_Planning/vehicle_delay_rate.csv"
)

region_delay.to_csv(
    "../Project_1_Strategic_Planning/region_delay_rate.csv"
)

partner_delay.to_csv(
    "../Project_1_Strategic_Planning/partner_delay_rate.csv"
)

print("\nAnalysis results saved successfully.")

#11 Delivery status v/s delay
print("\n========== Delivery Status vs Delay ==========")

status_delay = pd.crosstab(
    df["delivery_status"],
    df["delayed"],
    normalize="index"
) * 100

print(status_delay)

#11.1 Counting the number of delivery status which got delivered
print("\n========== Delivery Status Counts ==========")

print(df["delivery_status"].value_counts())

print("\n========== Data Types ==========")
print(df.dtypes)

print("\n========== Time-related Columns ==========")

for column in df.columns:
    if "time" in column.lower() or "date" in column.lower():
        print(column)


print("\n========== COMPLETE MISSING VALUE CHECK ==========")

missing = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": df.isnull().mean() * 100
})

print(missing)

print("\n========== Delivery Time Values ==========")
print(df["delivery_time_hours"].value_counts(dropna=False).head(20))

print("\n========== Expected Time Values ==========")
print(df["expected_time_hours"].value_counts(dropna=False).head(20))

print("\n========== Raw Values ==========")
print(df[["delivery_time_hours", "expected_time_hours"]].head(20).to_string())

print(df[["delivery_time_hours", "expected_time_hours"]].head(20).to_string(index=False))

print(df["delivery_time_hours"].value_counts().head(20))
print(df["expected_time_hours"].value_counts().head(20))

print("Delivery time unique values:", df["delivery_time_hours"].nunique())
print("Expected time unique values:", df["expected_time_hours"].nunique())

print("\n========== Delivery ID Check ==========")

print("Missing IDs:", df["delivery_id"].isnull().sum())
print("Duplicate IDs:", df["delivery_id"].duplicated().sum())
print("Unique IDs:", df["delivery_id"].nunique())
print("Total Rows:", len(df))


print("\n========== DUPLICATE DELIVERY IDs ==========")

duplicate_ids = df[
    df["delivery_id"].duplicated(keep=False)
].sort_values("delivery_id")

print(duplicate_ids.head(20))

print("\nRows involved:",
      len(duplicate_ids))

print("Unique duplicated IDs:",
      duplicate_ids["delivery_id"].nunique())

print("\n========== EXACT DUPLICATE ROWS ==========")

print("Exact duplicate rows:",
      df.duplicated(keep=False).sum())

print("\n========== DUPLICATED DELIVERY ID FREQUENCY ==========")

print(
    df["delivery_id"]
    .value_counts()
    .loc[lambda x: x > 1]
)


duplicate_id_values = (
    df["delivery_id"]
    .value_counts()
    .loc[lambda x: x > 1]
    .index
)

print(
    df[df["delivery_id"].isin(duplicate_id_values)]
    .sort_values("delivery_id")
    .to_string(index=False)
)


print("\n========== DUPLICATED ID ANALYSIS ==========")

duplicate_ids = [250.99, 24750.01]

for id_value in duplicate_ids:
    subset = df[df["delivery_id"] == id_value]

    print(f"\nDelivery ID: {id_value}")
    print("Rows:", len(subset))
    print("Delayed:")
    print(subset["delayed"].value_counts())
    print("Delivery Status:")
    print(subset["delivery_status"].value_counts())
    print("Average Distance:", subset["distance_km"].mean())
    print("Average Cost:", subset["delivery_cost"].mean())

    failure_rate = (
            (df["delivery_status"] == "failed").mean() * 100
    )

    print("Failure Rate:", round(failure_rate, 2), "%")

    # ============================================================
    # PRESENTATION-READY KPI TABLE
    # ============================================================

    total_deliveries = len(df)
    delayed_deliveries = df["delayed"].sum()
    delay_rate = df["delayed"].mean() * 100
    failure_rate = (df["delivery_status"] == "failed").mean() * 100
    average_cost = df["delivery_cost"].mean()
    average_distance = df["distance_km"].mean()
    average_rating = df["delivery_rating"].mean()

    kpi_table = pd.DataFrame({
        "KPI": [
            "Total Deliveries",
            "Delayed Deliveries",
            "Delay Rate (%)",
            "Failure Rate (%)",
            "Average Delivery Cost",
            "Average Distance (km)",
            "Average Customer Rating"
        ],
        "Value": [
            total_deliveries,
            delayed_deliveries,
            round(delay_rate, 2),
            round(failure_rate, 2),
            round(average_cost, 2),
            round(average_distance, 2),
            round(average_rating, 2)
        ]
    })

    print("\n========== PRESENTATION KPI TABLE ==========")
    print(kpi_table.to_string(index=False))

    import matplotlib.pyplot as plt

    # ============================================================
    # DELAY RATE BY WEATHER CONDITION
    # ============================================================

    weather_delay = (
            df.groupby("weather_condition")["delayed"]
            .mean()
            .sort_values(ascending=False) * 100
    )

    plt.figure(figsize=(9, 5))

    weather_delay.plot(kind="bar")

    plt.title("Delivery Delay Rate by Weather Condition")
    plt.xlabel("Weather Condition")
    plt.ylabel("Delay Rate (%)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()

    # ============================================================
    # DELAY RATE BY DELIVERY MODE
    # ============================================================

    mode_delay = (
            df.groupby("delivery_mode")["delayed"]
            .mean()
            .sort_values(ascending=False) * 100
    )

    plt.figure(figsize=(9, 5))

    mode_delay.plot(kind="bar")

    plt.title("Delivery Delay Rate by Delivery Mode")
    plt.xlabel("Delivery Mode")
    plt.ylabel("Delay Rate (%)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()


# ============================================================
# AVERAGE DISTANCE: DELAYED VS NON-DELAYED
# ============================================================

distance_comparison = (
    df.groupby("delayed")["distance_km"]
    .mean()
)

distance_comparison.index = [
    "Not Delayed",
    "Delayed"
]

plt.figure(figsize=(7, 5))

distance_comparison.plot(kind="bar")

plt.title("Average Delivery Distance by Delay Status")
plt.xlabel("Delivery Status")
plt.ylabel("Average Distance (km)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


plt.savefig("delay_rate_weather.png", dpi=300, bbox_inches="tight")
plt.show()

plt.savefig("delay_rate_delivery_mode.png", dpi=300, bbox_inches="tight")
plt.show()

plt.savefig("average_distance_delay.png", dpi=300, bbox_inches="tight")
plt.show()

# ============================================================
# AVERAGE DELIVERY COST: DELAYED VS NON-DELAYED
# ============================================================

cost_comparison = df.groupby("delayed")["delivery_cost"].mean()

cost_comparison.index = [
    "Not Delayed",
    "Delayed"
]

print("\n========== AVERAGE COST BY DELAY STATUS ==========")
print(cost_comparison.round(2))

# Check for completely duplicated rows

duplicate_rows = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_rows)


# Check for duplicate delivery IDs
duplicate_ids = df["delivery_id"].duplicated().sum()

print("Number of duplicate delivery IDs:", duplicate_ids)

# Display records with duplicate delivery IDs
duplicate_id_rows = df[df["delivery_id"].duplicated(keep=False)]

duplicate_id_rows.sort_values("delivery_id").head(20)

# Count how many times each delivery ID appears
id_counts = df["delivery_id"].value_counts()

# Show IDs that occur more than once
repeated_ids = id_counts[id_counts > 1]

print("Number of unique repeated IDs:", len(repeated_ids))
print("\nFrequency of repeated IDs:")
print(repeated_ids.value_counts().sort_index())

# Display the most frequently repeated delivery IDs
print(repeated_ids.head(20))

# Inspect all records associated with the two repeated IDs
suspicious_ids = [250.99, 24750.01]

df[df["delivery_id"].isin(suspicious_ids)].head(20)

# Compare the two suspicious IDs across the other variables
df[df["delivery_id"].isin(suspicious_ids)].groupby(
    "delivery_id"
).agg({
    "distance_km": ["min", "max", "mean"],
    "package_weight_kg": ["min", "max", "mean"],
    "delivery_rating": ["min", "max", "mean"],
    "delivery_cost": ["min", "max", "mean"]
})

# Check whether delivery IDs contain decimal values
decimal_ids = df[
    df["delivery_id"] % 1 != 0
]["delivery_id"]

print("Number of IDs containing decimals:", len(decimal_ids))
print("\nSample decimal IDs:")
print(decimal_ids.head(20))


# Check the range and number of unique IDs
print("Minimum delivery ID:", df["delivery_id"].min())
print("Maximum delivery ID:", df["delivery_id"].max())
print("Unique delivery IDs:", df["delivery_id"].nunique())
print("Total records:", len(df))

# Convert delivery_id to string because it is an identifier,
# not a numerical variable for mathematical calculations
df["delivery_id"] = df["delivery_id"].astype(str)

print(df["delivery_id"].dtype)

# Check unique values in delivery_time_hours
print("Unique delivery time values:")
print(df["delivery_time_hours"].value_counts().head(20))

print("\nNumber of unique values:",
      df["delivery_time_hours"].nunique())

# Check unique values in expected_time_hours
print("Unique expected time values:")
print(df["expected_time_hours"].value_counts().head(20))

print("\nNumber of unique values:",
      df["expected_time_hours"].nunique())


# Create a copy for preprocessing
df_clean = df.copy()

# Remove non-informative constant columns
df_clean = df_clean.drop(
    columns=["delivery_time_hours", "expected_time_hours"]
)

print("Original columns:", df.shape[1])
print("Columns after removing constant time fields:", df_clean.shape[1])


# Examine unique categories in the main categorical variables

categorical_columns = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "delayed",
    "delivery_status"
]

for column in categorical_columns:
    print(f"\n--- {column} ---")
    print(df_clean[column].value_counts())

    # Numerical columns to validate
    numerical_columns = [
        "distance_km",
        "package_weight_kg",
        "delivery_rating",
        "delivery_cost"
    ]

    # Check minimum and maximum values
    for column in numerical_columns:
        print(f"\n--- {column} ---")
        print("Minimum:", df_clean[column].min())
        print("Maximum:", df_clean[column].max())


# Check logically invalid values

print("Negative distances:",
      (df_clean["distance_km"] < 0).sum())

print("Negative package weights:",
      (df_clean["package_weight_kg"] < 0).sum())

print("Invalid ratings:",
      ((df_clean["delivery_rating"] < 1) |
       (df_clean["delivery_rating"] > 5)).sum())

print("Negative delivery costs:",
      (df_clean["delivery_cost"] < 0).sum())


# Detect outliers using the IQR method

numerical_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_rating",
    "delivery_cost"
]

outlier_summary = []

for column in numerical_columns:
    Q1 = df_clean[column].quantile(0.25)
    Q3 = df_clean[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (
        (df_clean[column] < lower_bound) |
        (df_clean[column] > upper_bound)
    ).sum()

    outlier_summary.append({
        "Variable": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower Bound": lower_bound,
        "Upper Bound": upper_bound,
        "Outlier Count": outliers
    })

outlier_summary = pd.DataFrame(outlier_summary)

print(outlier_summary)


# Create a summary of preprocessing actions

cleaning_summary = pd.DataFrame({
    "Issue": [
        "Missing values",
        "Complete duplicate rows",
        "Duplicate delivery IDs",
        "Incorrect ID data type",
        "Constant time fields",
        "Categorical inconsistencies",
        "Invalid numerical values",
        "Statistical outliers"
    ],
    "Finding": [
        "0 missing values",
        "0 duplicate rows",
        "2 IDs repeated 250 times each",
        "delivery_id stored as float64",
        "00:00.0 in all 25,000 records",
        "No obvious inconsistencies",
        "0 invalid values",
        "0 IQR outliers"
    ],
    "Action": [
        "No imputation required",
        "No rows removed",
        "Retained; documented as identifier issue",
        "Converted to string",
        "Removed from analytical dataset",
        "No changes required",
        "No correction required",
        "No treatment required"
    ]
})

print(cleaning_summary)


from sklearn.preprocessing import MinMaxScaler

# Variables selected for normalization
normalization_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_cost"
]

# Create the scaler
scaler = MinMaxScaler()

# Create normalized versions without changing the original variables
for column in normalization_columns:
    df_clean[column + "_normalized"] = scaler.fit_transform(
        df_clean[[column]]
    )

# Display the result
print(
    df_clean[
        normalization_columns +
        [column + "_normalized" for column in normalization_columns]
    ].head()
)


# Verify the minimum and maximum after normalization

for column in normalization_columns:
    normalized_column = column + "_normalized"

    print(
        normalized_column,
        "Min =", df_clean[normalized_column].min(),
        "Max =", df_clean[normalized_column].max()
    )



# Compare original and normalized values

comparison = df_clean[
    [
        "distance_km",
        "distance_km_normalized",
        "package_weight_kg",
        "package_weight_kg_normalized",
        "delivery_cost",
        "delivery_cost_normalized"
    ]
].head(10)

print(comparison)


from sklearn.preprocessing import StandardScaler

standard_scaler = StandardScaler()

for column in normalization_columns:
    df_clean[column + "_standardized"] = standard_scaler.fit_transform(
        df_clean[[column]]
    )

print(
    df_clean[
        [column + "_standardized" for column in normalization_columns]
    ].describe()
)


# Final validation of the cleaned dataset

print("FINAL DATASET VALIDATION")
print("-" * 40)

print("Number of rows:", len(df_clean))
print("Number of columns:", df_clean.shape[1])

print("\nTotal missing values:",
      df_clean.isnull().sum().sum())

print("Complete duplicate rows:",
      df_clean.duplicated().sum())

print("Duplicate delivery IDs:",
      df_clean["delivery_id"].duplicated().sum())

print("\nData types:")
print(df_clean.dtypes)


# Check normalized variables

normalized_columns = [
    "distance_km_normalized",
    "package_weight_kg_normalized",
    "delivery_cost_normalized"
]

print(df_clean[normalized_columns].describe())

# Final preprocessing summary

final_summary = pd.DataFrame({
    "Data Quality Check": [
        "Records",
        "Columns",
        "Missing values",
        "Complete duplicate rows",
        "Duplicate delivery IDs",
        "Constant time columns",
        "Categorical inconsistencies",
        "Invalid numerical values",
        "IQR outliers"
    ],

    "Before Preprocessing": [
        25000,
        15,
        0,
        0,
        498,
        2,
        "None identified",
        0,
        0
    ],

    "After Preprocessing": [
        25000,
        13,
        0,
        0,
        498,
        0,
        "None identified",
        0,
        0
    ],

    "Treatment": [
        "Retained",
        "2 non-informative columns removed",
        "No treatment required",
        "No treatment required",
        "Retained and documented as ID issue",
        "Removed from analytical dataset",
        "No treatment required",
        "No treatment required",
        "No treatment required"
    ]
})

print(final_summary)


# Save the preprocessed dataset

df_clean.to_csv(
    "Delivery_Logistics_Cleaned.csv",
    index=False
)

print("Cleaned dataset saved successfully.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the original dataset
df = pd.read_csv("C:/Users/singh/OneDrive/Desktop/Logistics Data Analysis Project/Dataset/Delivery_Logistics.csv")

# Create analytical copy
df_eda = df.copy()

# Treat delivery ID as an identifier
df_eda["delivery_id"] = df_eda["delivery_id"].astype(str)

# Remove non-informative variables identified in Project 2
df_eda = df_eda.drop(
    columns=["delivery_time_hours", "expected_time_hours"]
)

print("EDA dataset shape:", df_eda.shape)

# Descriptive statistics for key numerical variables

numeric_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_rating",
    "delivery_cost"
]

descriptive_stats = df_eda[numeric_columns].describe()

print(descriptive_stats)

central_tendency = pd.DataFrame({
    "Mean": df_eda[numeric_columns].mean(),
    "Median": df_eda[numeric_columns].median(),
    "Standard Deviation": df_eda[numeric_columns].std()
})

print(central_tendency)



plt.figure(figsize=(8, 5))

sns.histplot(
    df_eda["distance_km"],
    bins=30,
    kde=True
)

plt.title("Distribution of Delivery Distance")
plt.xlabel("Distance (km)")
plt.ylabel("Number of Deliveries")
plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(
    df_eda["package_weight_kg"],
    bins=30,
    kde=True
)

plt.title("Distribution of Package Weight")
plt.xlabel("Package Weight (kg)")
plt.ylabel("Number of Deliveries")
plt.show()

plt.figure(figsize=(8, 5))

sns.histplot(
    df_eda["delivery_cost"],
    bins=30,
    kde=True
)

plt.title("Distribution of Delivery Cost")
plt.xlabel("Delivery Cost")
plt.ylabel("Number of Deliveries")
plt.show()


plt.figure(figsize=(8, 5))

sns.boxplot(
    y=df_eda["delivery_cost"]
)

plt.title("Box Plot of Delivery Cost")
plt.ylabel("Delivery Cost")
plt.show()


delay_by_mode = (
    df_eda.groupby("delivery_mode")["delayed"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .sort_values(ascending=False)
)

print(delay_by_mode)


plt.figure(figsize=(8, 5))

sns.barplot(
    x=delay_by_mode.index,
    y=delay_by_mode.values
)

plt.title("Delay Rate by Delivery Mode")
plt.xlabel("Delivery Mode")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


delay_by_weather = (
    df_eda.groupby("weather_condition")["delayed"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .sort_values(ascending=False)
)

print(delay_by_weather)


plt.figure(figsize=(8, 5))

sns.barplot(
    x=delay_by_weather.index,
    y=delay_by_weather.values
)

plt.title("Delay Rate by Weather Condition")
plt.xlabel("Weather Condition")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


delay_by_partner = (
    df_eda.groupby("delivery_partner")["delayed"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .sort_values(ascending=False)
)

print(delay_by_partner)

plt.figure(figsize=(10, 5))

sns.barplot(
    x=delay_by_partner.values,
    y=delay_by_partner.index
)

plt.title("Delay Rate by Delivery Partner")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Delivery Partner")
plt.tight_layout()
plt.show()


delay_by_region = (
    df_eda.groupby("region")["delayed"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .sort_values(ascending=False)
)

print(delay_by_region)

plt.figure(figsize=(8, 5))

sns.barplot(
    x=delay_by_region.index,
    y=delay_by_region.values
)

plt.title("Delay Rate by Region")
plt.xlabel("Region")
plt.ylabel("Delay Rate (%)")
plt.tight_layout()
plt.show()


delay_by_vehicle = (
    df_eda.groupby("vehicle_type")["delayed"]
    .apply(lambda x: (x == "yes").mean() * 100)
    .sort_values(ascending=False)
)

print(delay_by_vehicle)


# Define predictor variables
features = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "distance_km",
    "package_weight_kg"
]

# Define target variable
target = "delivery_cost"

X = df[features]
y = df[target]

print("Features shape:", X.shape)
print("Target shape:", y.shape)

categorical_features = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition"
]

numerical_features = [
    "distance_km",
    "package_weight_kg"
]

print("Categorical Features:")
print(categorical_features)

print("\nNumerical Features:")
print(numerical_features)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

print("Preprocessing pipeline created successfully.")

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

linear_regression = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ]
)

linear_regression.fit(X_train, y_train)

print("Linear Regression model trained successfully.")


y_pred_lr = linear_regression.predict(X_test)

print("First 10 predictions:")
print(y_pred_lr[:10])


from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

mae_lr = mean_absolute_error(y_test, y_pred_lr)

rmse_lr = mean_squared_error(
    y_test,
    y_pred_lr
) ** 0.5

r2_lr = r2_score(y_test, y_pred_lr)

print("Linear Regression Performance")
print("-----------------------------")
print("MAE :", mae_lr)
print("RMSE:", rmse_lr)
print("R²  :", r2_lr)


from sklearn.tree import DecisionTreeRegressor

decision_tree = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", DecisionTreeRegressor(
            random_state=42,
            max_depth=10,
            min_samples_leaf=5
        ))
    ]
)

decision_tree.fit(X_train, y_train)

print("Decision Tree model trained successfully.")

y_pred_dt = decision_tree.predict(X_test)

print("First 10 Decision Tree predictions:")
print(y_pred_dt[:10])

mae_dt = mean_absolute_error(y_test, y_pred_dt)

rmse_dt = mean_squared_error(
    y_test,
    y_pred_dt
) ** 0.5

r2_dt = r2_score(y_test, y_pred_dt)

print("Decision Tree Performance")
print("------------------------")
print("MAE :", mae_dt)
print("RMSE:", rmse_dt)
print("R²  :", r2_dt)


from sklearn.ensemble import RandomForestRegressor

random_forest = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=250,
            random_state=42,
            n_jobs=-1,
            max_features="sqrt",
            min_samples_leaf=2
        ))
    ]
)

random_forest.fit(X_train, y_train)

print("Random Forest model trained successfully.")


y_pred_rf = random_forest.predict(X_test)

print("First 10 Random Forest predictions:")
print(y_pred_rf[:10])


mae_rf = mean_absolute_error(y_test, y_pred_rf)

rmse_rf = mean_squared_error(
    y_test,
    y_pred_rf
) ** 0.5

r2_rf = r2_score(y_test, y_pred_rf)

print("Random Forest Performance")
print("-------------------------")
print("MAE :", mae_rf)
print("RMSE:", rmse_rf)
print("R²  :", r2_rf)

model_comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Decision Tree",
        "Random Forest"
    ],
    "MAE": [
        mae_lr,
        mae_dt,
        mae_rf
    ],
    "RMSE": [
        rmse_lr,
        rmse_dt,
        rmse_rf
    ],
    "R2": [
        r2_lr,
        r2_dt,
        r2_rf
    ]
})

model_comparison


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

x = range(len(model_comparison))

plt.bar(
    [i - 0.2 for i in x],
    model_comparison["MAE"],
    width=0.4,
    label="MAE"
)

plt.bar(
    [i + 0.2 for i in x],
    model_comparison["RMSE"],
    width=0.4,
    label="RMSE"
)

plt.xticks(
    x,
    model_comparison["Model"],
    rotation=15
)

plt.xlabel("Model")
plt.ylabel("Error")
plt.title("Comparison of Model Prediction Errors")
plt.legend()

plt.tight_layout()
plt.show()


from sklearn.model_selection import KFold, cross_validate

kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

models = {
    "Linear Regression": linear_regression,
    "Decision Tree": decision_tree,
    "Random Forest": random_forest
}

cv_results = []

for name, model in models.items():

    scores = cross_validate(
        model,
        X,
        y,
        cv=kf,
        scoring={
            "MAE": "neg_mean_absolute_error",
            "RMSE": "neg_root_mean_squared_error",
            "R2": "r2"
        },
        n_jobs=1
    )

    cv_results.append({
        "Model": name,
        "CV MAE": -scores["test_MAE"].mean(),
        "CV RMSE": -scores["test_RMSE"].mean(),
        "CV R2": scores["test_R2"].mean()
    })

cv_results_df = pd.DataFrame(cv_results)

cv_results_df

best_model_name = cv_results_df.loc[
    cv_results_df["CV R2"].idxmax(),
    "Model"
]

print("Best model based on cross-validation R²:", best_model_name)

cv_results_df

from sklearn.model_selection import GridSearchCV

decision_tree_tuning = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", DecisionTreeRegressor(
            random_state=42
        ))
    ]
)

param_grid = {
    "model__max_depth": [5, 10, 15, None],
    "model__min_samples_leaf": [1, 5]
}

grid_search = GridSearchCV(
    decision_tree_tuning,
    param_grid=param_grid,
    cv=3,
    scoring="neg_root_mean_squared_error",
    n_jobs=1
)

grid_search.fit(X_train, y_train)

print("Best Parameters:")
print(grid_search.best_params_)

print("\nBest CV RMSE:")
print(-grid_search.best_score_)


tuned_dt = grid_search.best_estimator_

y_pred_tuned_dt = tuned_dt.predict(X_test)

mae_tuned_dt = mean_absolute_error(
    y_test,
    y_pred_tuned_dt
)

rmse_tuned_dt = mean_squared_error(
    y_test,
    y_pred_tuned_dt
) ** 0.5

r2_tuned_dt = r2_score(
    y_test,
    y_pred_tuned_dt
)

print("Tuned Decision Tree Performance")
print("--------------------------------")
print("MAE :", mae_tuned_dt)
print("RMSE:", rmse_tuned_dt)
print("R²  :", r2_tuned_dt)

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred_lr,
    alpha=0.5
)

min_value = min(y_test.min(), y_pred_lr.min())
max_value = max(y_test.max(), y_pred_lr.max())

plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linewidth=2
)

plt.xlabel("Actual Delivery Cost")
plt.ylabel("Predicted Delivery Cost")
plt.title("Actual vs Predicted Delivery Cost")

plt.tight_layout()
plt.show()

residuals = y_test - y_pred_lr

plt.figure(figsize=(8, 5))

plt.hist(
    residuals,
    bins=40
)

plt.xlabel("Prediction Error")
plt.ylabel("Frequency")
plt.title("Residual Distribution — Linear Regression")

plt.tight_layout()
plt.show()

# Create a preprocessing pipeline without scaling
preprocessor_unscaled = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

# Build and train interpretable Linear Regression model
interpretable_lr = Pipeline(
    steps=[
        ("preprocessor", preprocessor_unscaled),
        ("model", LinearRegression())
    ]
)

interpretable_lr.fit(X_train, y_train)

# Extract feature names and coefficients
feature_names = (
    interpretable_lr
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

coefficients = (
    interpretable_lr
    .named_steps["model"]
    .coef_
)

feature_effects = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

feature_effects["Absolute Effect"] = (
    feature_effects["Coefficient"].abs()
)

feature_effects = feature_effects.sort_values(
    "Absolute Effect",
    ascending=False
)

feature_effects.head(15)


top_features = (
    feature_effects
    .head(10)
    .sort_values("Absolute Effect")
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_features["Feature"],
    top_features["Coefficient"]
)

plt.xlabel("Regression Coefficient")
plt.ylabel("Feature")
plt.title("Top Predictive Drivers of Delivery Cost")

plt.tight_layout()
plt.show()

# Average values in the dataset
print("Average delivery cost:", df["delivery_cost"].mean())
print("Average distance:", df["distance_km"].mean())
print("Average package weight:", df["package_weight_kg"].mean())

# Linear regression coefficients
distance_coef = feature_effects[
    feature_effects["Feature"] == "numerical__distance_km"
]["Coefficient"].iloc[0]

weight_coef = feature_effects[
    feature_effects["Feature"] == "numerical__package_weight_kg"
]["Coefficient"].iloc[0]

print("\nDistance coefficient:", distance_coef)
print("Weight coefficient:", weight_coef)


avg_distance = df["distance_km"].mean()
avg_weight = df["package_weight_kg"].mean()

distance_10_percent_effect = (
    avg_distance * 0.10 * distance_coef
)

weight_10_percent_effect = (
    avg_weight * 0.10 * weight_coef
)

print("Estimated effect of 10% distance reduction:",
      distance_10_percent_effect)

print("Estimated effect of 10% weight reduction:",
      weight_10_percent_effect)






