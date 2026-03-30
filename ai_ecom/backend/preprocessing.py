import pandas as pd
import numpy as np
import os

def clean_data(
    input_file: str = "backend/data/clean_data.csv", 
    output_file: str = "backend/data/clean_data.csv"
):
    """
    Clean and preprocess the raw e-commerce dataset.
    """
    print("🚀 Starting data cleaning process...\n")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        print("💡 Please place your raw dataset in 'backend/data/' folder and update the filename.")
        return None

    try:
        df = pd.read_csv(input_file)
        print(f"✅ Loaded {len(df):,} rows from '{input_file}'")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

    print("🧹 Cleaning data...")

    # === Basic Cleaning ===
    df = df.drop_duplicates()

    # Drop rows missing critical columns
    df = df.dropna(subset=['product_id', 'product_name'])

    # Fill missing values
    if 'rating' in df.columns:
        df['rating'] = df['rating'].fillna(df['rating'].mean())

    if 'price' in df.columns:
        df['price'] = df['price'].fillna(df['price'].median())

    if 'rating_count' not in df.columns:
        df['rating_count'] = np.random.randint(50, 800, size=len(df))

    # === Clean Columns ===
    df['product_id'] = df['product_id'].astype(str).str.strip()
    df['product_name'] = df['product_name'].astype(str).str.strip()

    # Image URL handling
    if 'image_url' in df.columns:
        df['image_url'] = df['image_url'].astype(str).str.strip()
        invalid_mask = df['image_url'].str.contains('nan|NaN|None|undefined', case=False, na=True)
        df.loc[invalid_mask, 'image_url'] = "/assets/placeholder.jpg"
    else:
        df['image_url'] = "/assets/placeholder.jpg"

    # Tags and Category
    if 'tags' in df.columns:
        df['tags'] = df['tags'].astype(str).str.strip().replace('nan', 'General')
    else:
        df['tags'] = "General"

    if 'category' in df.columns:
        df['category'] = df['category'].astype(str).str.strip().replace('nan', 'Uncategorized')
    else:
        df['category'] = "Uncategorized"

    # Add description if missing
    if 'description' not in df.columns:
        df['description'] = df['product_name'] + ". " + df['tags']

    # === Type Conversion & Validation ===
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(499.0)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').clip(1, 5)
    df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce').fillna(100).astype(int)

    # Remove invalid prices
    df = df[df['price'] > 0]

    df = df.reset_index(drop=True)

    # === Save Cleaned Dataset ===
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\n🎉 Data cleaning completed successfully!")
    print(f"   Input  : {len(df):,} products (after cleaning)")
    print(f"   Output : {output_file}")
    
    print("\n📊 Summary:")
    print(f"   Total Products : {len(df)}")
    print(f"   Avg Rating     : {df['rating'].mean():.2f}/5")
    print(f"   Avg Price      : ₹{df['price'].mean():.2f}")
    print(f"   Columns        : {list(df.columns)}")

    return df


# ====================== Run Cleaner ======================
if __name__ == "__main__":
    # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
    # CHANGE THIS LINE to match your actual raw file name
    clean_data(
        input_file="backend/data/your_raw_file.csv",   # ←←← CHANGE THIS
        output_file="backend/data/clean_data.csv"
    )