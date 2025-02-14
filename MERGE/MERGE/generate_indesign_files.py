import os
import shutil
from system_settings import *

sys_settings = SystemSettings()  # Load system settings

# Define paths
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../TEST/MERGE/OUTPUT/", sys_settings.process_date)  
PRODUCTION_DIR = os.path.join(os.path.dirname(__file__), "../TEST/MERGE/INDESIGN/PRODUCTION")

def extract_base_template(txt_filename):
    """
    Extracts the base template name from the given .txt filename.
    Assumes the format: ORDERNUMBER_PRODUCTTYPE_SKU_VARIANT.txt
    Example: 3592981640_CWS_HCL_MD001_02.txt → CWS_HCL
    """
    parts = txt_filename.split("_")
    if len(parts) < 3:
        return None  # Invalid format

    return f"{parts[1]}_{parts[2]}.indd"  # Example output: "CWS_HCL.indd"

def generate_indesign_files():
    """Copies and renames InDesign files to match the .txt files."""
    if not os.path.exists(OUTPUT_DIR):
        print(f"❌ Output directory not found: {OUTPUT_DIR}")
        return

    txt_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".txt")]

    copied_files = 0
    for txt_file in txt_files:
        base_template = extract_base_template(txt_file)

        if not base_template:
            print(f"⚠️ Skipping {txt_file} - Invalid format")
            continue

        source_indd_path = os.path.join(PRODUCTION_DIR, base_template)
        target_indd_path = os.path.join(OUTPUT_DIR, txt_file.replace(".txt", ".indd"))

        if not os.path.exists(source_indd_path):
            print(f"❌ No matching template found for {txt_file} ({base_template} missing)")
            continue

        shutil.copy2(source_indd_path, target_indd_path)
        copied_files += 1
        # print(f"✅ Copied {source_indd_path} → {target_indd_path}")

    print(f"🎨 Successfully generated {copied_files} InDesign files.")

if __name__ == "__main__":
    generate_indesign_files()
