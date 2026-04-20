import bibtexparser
import pandas as pd
import glob
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_bib(bib_file_path):
    with open(bib_file_path, 'r', encoding='utf-8') as bibfile:
        library = bibtexparser.load(bibfile)
    
    results = []
    for entry in library.entries:
        title = entry.get('title', None)
        abstract = entry.get('abstract', None)
        doi = entry.get('doi', None)

        results.append({
            "doi": doi,
            "title": title,
            "abstract": abstract
        })
    return results

def get_bib_paths(bib_folder_path):
    bib_files = [f for f in glob.glob(f"{bib_folder_path}/**/*.bib", recursive=True)]
    print(bib_files)
    return bib_files

def get_md_content(md_file_path):
    if not os.path.exists(md_file_path):
        print(f"Warning: File not found {md_file_path}")
        return ""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def create_payload(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria):
    messages = [
        {
            "role": system_role,
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt_template.format(INCLUSION_CRITERIA=inclusion_criteria, 
                                            EXCLUSION_CRITERIA=exclusion_criteria, 
                                            TITLE=prompt_data['title'], 
                                            ABSTRACT=prompt_data['abstract'])
        }
    ]
    return messages

# Constants for Selenium redirection due to C: drive space constraints
D_CACHE_DIR = 'D:\\.cache\\selenium'
D_PROFILE_DIR = 'D:\\.cache\\edge_profile'

def get_ieee_abstract(url):
    """
    Scrapes the abstract from an IEEE Xplore page using Edge browser.
    Redirects cache and profile to D: drive due to C: drive space constraints.
    """
    os.makedirs(D_CACHE_DIR, exist_ok=True)
    os.makedirs(D_PROFILE_DIR, exist_ok=True)
    os.environ['SELENIUM_MANAGER_CACHE'] = D_CACHE_DIR

    # Setup headless Edge
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument(f"--user-data-dir={D_PROFILE_DIR}")
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

    driver = None
    try:
        service = Service() 
        driver = webdriver.Edge(options=edge_options, service=service)
        driver.get(url)

        # Wait for the abstract div
        wait = WebDriverWait(driver, 20)
        abstract_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[xplmathjax]"))
        )
        return abstract_element.text
    except Exception as e:
        return f"Error during scraping: {e}"
    finally:
        if driver:
            driver.quit()

def aggregate_bibs_to_excel(root_dir, output_file):
    """
    Scans root_dir for all .bib files, extracts papers, 
    separates duplicates and missing elements, and saves to Excel.
    """
    bib_files = get_bib_paths(root_dir)
    
    all_papers = []
    seen_dois = {} # doi -> list of titles/files for tracking duplicates
    duplicates = []
    missing_doi = []
    valid_papers = []

    for bib_file in bib_files:
        papers = extract_bib(bib_file)
        for paper in papers:
            paper['bib_file'] = bib_file
            
            # 1. Check for missing elements
            if not paper['doi']:
                missing_doi.append(paper)
                continue
                
            # 2. Check for duplicates
            doi = paper['doi'].strip().lower()
            if doi in seen_dois:
                paper['original_occurrence'] = seen_dois[doi]
                duplicates.append(paper)
                continue
            
            # 3. Valid paper
            seen_dois[doi] = f"{bib_file} | {paper['title']}"
            valid_papers.append(paper)

    # Convert to DataFrames
    df_valid = pd.DataFrame(valid_papers)
    df_missing = pd.DataFrame(missing_doi)
    df_duplicates = pd.DataFrame(duplicates)

    # Reorder columns for better readability if they exist
    cols = ['doi', 'title', 'abstract', 'bib_file']
    if not df_valid.empty:
        df_valid = df_valid[[c for c in cols if c in df_valid.columns]]
    if not df_missing.empty:
        df_missing = df_missing[[c for c in cols if c in df_missing.columns]]
    if not df_duplicates.empty:
        dup_cols = cols + ['original_occurrence']
        df_duplicates = df_duplicates[[c for c in dup_cols if c in df_duplicates.columns]]

    # Write to Excel
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_valid.to_excel(writer, sheet_name='Results', index=False)
        df_missing.to_excel(writer, sheet_name='missing_doi', index=False)
        df_duplicates.to_excel(writer, sheet_name='duplicated_dois', index=False)
    
    print(f"Aggregation complete. Results saved to: {output_file}")
    print(f"Valid: {len(valid_papers)}, Missing: {len(missing_doi)}, Duplicates: {len(duplicates)}")

if __name__ == "__main__":
    aggregate_bibs_to_excel("slr/bib", "slr/bib/bib_aggregation_results.xlsx")
