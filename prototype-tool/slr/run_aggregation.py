from utils import aggregate_bibs_to_excel
import os

if __name__ == "__main__":
    root_bib_dir = "slr/bib"
    output_excel = "slr/bib_aggregation_results.xlsx"
    
    print(f"Starting aggregation of all .bib files in {root_bib_dir}...")
    aggregate_bibs_to_excel(root_bib_dir, output_excel)
    
    if os.path.exists(output_excel):
        print(f"SUCCESS: {output_excel} created.")
    else:
        print(f"FAILED: {output_excel} was not created.")
