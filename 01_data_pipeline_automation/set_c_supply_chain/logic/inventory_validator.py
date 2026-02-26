import csv
import re
import os

def validate_inventory(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    cleaned_data = []
    issues_found = 0

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        if 'flag_reason' not in fieldnames:
            fieldnames.append('flag_reason')

        for row in reader:
            flags = []
            
            # 1. SKU Standardization Check (Prefix-Numbers)
            # basic regex: ^[A-Z]{2}-[0-9]{4}$
            sku = row['item_sku']
            if not re.match(r'^[A-Z]{2}-[0-9]{4}$', sku):
                flags.append("MALFORMED_SKU")

            # 2. Stock Quantity Reality Check
            try:
                qty = int(row['stock_quantity'])
                if qty < 0:
                    flags.append("NEGATIVE_STOCK")
            except ValueError:
                flags.append("NON_NUMERIC_STOCK")

            # 3. Pricing Integrity
            try:
                price = float(row['unit_price'])
                if price <= 0:
                    flags.append("INVALID_PRICE")
                elif price > 5000:
                    flags.append("HIGH_VALUE_REVIEW_REQUIRED")
            except ValueError:
                flags.append("NON_NUMERIC_PRICE")

            row['flag_reason'] = " | ".join(flags)
            if flags:
                issues_found += 1
                
            cleaned_data.append(row)

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"Inventory Validation complete.")
    print(f"Total rows processed: {len(cleaned_data)}")
    print(f"Rows with Validation Flags: {issues_found}")
    print(f"Validated output saved to {output_file}")


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_csv = os.path.join(base_dir, '../data/inventory_logs.csv')
    
    # We write to /tmp to bypass Mac SIP / Sandbox environments safely.
    output_dir = '/tmp/supply_chain_output'
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, 'scrubbed_inventory.csv')
    
    validate_inventory(input_csv, output_csv)
