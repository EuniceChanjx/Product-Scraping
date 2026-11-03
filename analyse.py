

import pandas as pd

# =====================================
# 1. LOAD SCRAPED DATA
# =====================================

df = pd.read_csv("products.csv")

print("\n========== ORIGINAL DATA ==========")
print(df.head())

print("\n========== DATASET INFORMATION ==========")
df.info()


# =====================================
# 2. CLEAN PRODUCT PRICES
# =====================================

df["price"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .astype(float)
)


# =====================================
# 3. CONVERT RATINGS INTO NUMBERS
# =====================================

rating_mapping = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_mapping)


# =====================================
# 4. PRICE STATISTICS
# =====================================

print("\n========== PRICE STATISTICS ==========")

print("Total products:", len(df))
print("Cheapest price: £", df["price"].min())
print("Most expensive price: £", df["price"].max())
print("Average price: £", round(df["price"].mean(), 2))
print("Median price: £", round(df["price"].median(), 2))


# =====================================
# 5. TOP 10 CHEAPEST PRODUCTS
# =====================================

print("\n========== TOP 10 CHEAPEST PRODUCTS ==========")

cheapest_products = df.sort_values(
    by="price",
    ascending=True
)

print(cheapest_products[["name", "price", "rating"]].head(10))


# =====================================
# 6. TOP 10 MOST EXPENSIVE PRODUCTS
# =====================================

print("\n========== TOP 10 MOST EXPENSIVE PRODUCTS ==========")

expensive_products = df.sort_values(
    by="price",
    ascending=False
)

print(expensive_products[["name", "price", "rating"]].head(10))


# =====================================
# 7. HIGHEST RATED PRODUCTS
# =====================================

print("\n========== HIGHEST RATED PRODUCTS ==========")

highest_rated = df.sort_values(
    by="rating",
    ascending=False
)

print(highest_rated[["name", "price", "rating"]].head(10))


# =====================================
# 8. ANALYZE 5-STAR PRODUCTS
# =====================================

print("\n========== 5-STAR PRODUCTS ==========")

five_star = df[df["rating"] == 5]

print("Number of 5-star products:", len(five_star))

if not five_star.empty:
    print(
        "Average price of 5-star products: £",
        round(five_star["price"].mean(), 2)
    )


# =====================================
# 9. RATING DISTRIBUTION
# =====================================

print("\n========== RATING DISTRIBUTION ==========")

print(df["rating"].value_counts().sort_index())


# =====================================
# 10. EXPORT CLEANED DATA
# =====================================

df.to_csv("cleaned_products.csv", index=False)

print("\n=====================================")
print("ANALYSIS COMPLETED!")
print("Cleaned data saved to cleaned_products.csv")
print("=====================================")
