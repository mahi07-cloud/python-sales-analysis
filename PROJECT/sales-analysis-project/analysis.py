import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the Data
print("--- Loading Data ---")
df = pd.read_csv('sales_data.csv')

# 2. Data Cleaning (THE FIX)
# Force columns to be numbers. 'coerce' turns bad data into NaN (empty)
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')

# Drop any rows that have empty numbers just in case
df.dropna(subset=['Quantity Ordered', 'Price Each'], inplace=True)

# 3. Calculate Sales
df['Sales'] = df['Quantity Ordered'] * df['Price Each']

# 4. ANALYSIS: Key Insights
print("\n--- Key Insights ---")

# Total Revenue
total_revenue = df['Sales'].sum()
print(f"Total Revenue: ${total_revenue:,.2f}") # Formatted with commas

# Best Selling Product
best_selling_product = df.groupby('Product')['Quantity Ordered'].sum().idxmax()
print(f"Best Selling Product: {best_selling_product}")

# Top City by Sales
top_city = df.groupby('Purchase Address')['Sales'].sum().idxmax()
print(f"City with Highest Sales: {top_city}")

# 5. VISUALIZATION: Sales by Product
print("\n--- Generating Chart ---")
product_sales = df.groupby('Product')['Sales'].sum()

# Create Bar Chart
plt.figure(figsize=(10, 6))
# Ensure we are plotting numeric data
product_sales.plot(kind='bar', color='#06b6d4') 

plt.title('Total Sales by Product')
plt.xlabel('Product Name')
plt.ylabel('Sales in USD ($)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout to prevent cutting off labels
plt.tight_layout()

# Save the plot
plt.savefig('sales_chart.png')
print("[SUCCESS] Chart saved as 'sales_chart.png'")

# Show the plot
plt.show()