import csv
import random
from datetime import datetime, timedelta
import os

def generate_inventory_data(num_rows=50):
    data = []
    
    # Valid SKU format: Prefix-Numbers e.g., WH-9942
    prefixes = ['WH', 'ST', 'AB', 'TX']
    malformed_skus = ['9942-WH', 'WH_9942', 'NO-SKU-HERE', '12345']
    
    warehouse_ids = ['W-East', 'W-West', 'W-North', 'W-South', 'W-Central']
    
    start_date = datetime.now() - timedelta(days=90)

    for i in range(num_rows):
        is_dirty = random.random() < 0.25  # 25% chance of dirty data
        
        # 1. SKU Standardization
        if is_dirty and random.random() < 0.4:
            item_sku = random.choice(malformed_skus)
        else:
            item_sku = f"{random.choice(prefixes)}-{random.randint(1000, 9999)}"
            
        # 2. Warehouse
        warehouse_id = random.choice(warehouse_ids)
        
        # 3. Stock Quantity (Physical Reality Check: >= 0)
        if is_dirty and random.random() < 0.5:
            # Negative physical stock
            stock_quantity = random.randint(-50, -1)
        else:
            stock_quantity = random.randint(0, 1000)
            
        # 4. Unit Price (Pricing Integrity: > $0.00)
        if is_dirty and random.random() < 0.3:
            # Zero or negative pricing
            unit_price = round(random.uniform(-100, 0), 2)
        else:
            unit_price = round(random.uniform(10, 8000), 2) # Include some high value items
            
        # 5. Restock Date
        days_offset = random.randint(0, 90)
        restock_date = start_date + timedelta(days=days_offset)
        
        data.append({
            'item_sku': item_sku,
            'warehouse_id': warehouse_id,
            'stock_quantity': stock_quantity,
            'unit_price': unit_price,
            'last_restock_date': restock_date.strftime('%Y-%m-%d')
        })
        
    return data

if __name__ == '__main__':
    header = ['item_sku', 'warehouse_id', 'stock_quantity', 'unit_price', 'last_restock_date']
    data = generate_inventory_data(50)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, '../data')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'inventory_logs.csv')
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Successfully generated 50 rows of synthetic supply chain data to {output_file}")
