import os
import pandas as pd
import tqdm
import datetime
from dotenv import load_dotenv

# Import modularized functions
from utils import extract_bib, get_bib_paths, get_md_content
from api_handlers import call_rwth_gpt_api, call_gemini_api, call_groq_api

load_dotenv()

def screen_papers(experiment_name, provider, model, system_role, system_prompt, ):
    bib_files = get_bib_paths(f"slr/bib")
    inclusion_criteria = get_md_content(f"slr/criteria/inclusion_criteria.md")
    exclusion_criteria = get_md_content(f"slr/criteria/exclusion_criteria.md")
    prompt_template = get_md_content("prompts/slr-filter.md")
    
    included_df = pd.DataFrame()
    excluded_df = pd.DataFrame()
    uncertain_df = pd.DataFrame()
    missing_df = pd.DataFrame()
    
    for bib_file in tqdm.tqdm(bib_files, desc="Processing Bib files"):
        papers = extract_bib(bib_file) 
        for paper in tqdm.tqdm(papers, desc="Screening papers", leave=False):
            returned_content = {
                'doi': paper['doi'],
                'title': paper['title'],
                'abstract': paper['abstract'],
                'bib_file': bib_file
            }
            
            if paper['doi'] is None or paper['title'] is None or paper['abstract'] is None:
                returned_content.update({
                    'summary': '',
                    'decision': 'Uncertain',
                    'matched_ic': [],
                    'triggered_ec': [],
                    'justification': 'Missing DOI, Title, or Abstract',
                    'score': 0.0,
                    'confidence': 0.0
                })
                missing_df = pd.concat([missing_df, pd.DataFrame([returned_content])], ignore_index=True)
                continue
                
            try:
                if provider == 'rwth-gpt' or provider == 'rwth-gpt-emp':
                    res = call_rwth_gpt_api(model, system_role, system_prompt, prompt_template, 
                                            paper, inclusion_criteria, exclusion_criteria)
                elif provider == 'gemini':
                    res = call_gemini_api(model, system_role, system_prompt, prompt_template, 
                                          paper, inclusion_criteria, exclusion_criteria)
                elif provider == 'groq':
                    res = call_groq_api(model, system_role, system_prompt, prompt_template, 
                                        paper, inclusion_criteria, exclusion_criteria)
                else:
                    raise ValueError(f"Unknown provider: {provider}")
                
                returned_content.update(res)
            except Exception as e:
                print(f"Error processing paper {paper['title'][:50]}: {e}")
                returned_content.update({
                    'summary': 'Error',
                    'decision': 'Uncertain',
                    'matched_ic': [],
                    'triggered_ec': [],
                    'justification': f"Processing error: {str(e)}",
                    'score': 0.0
                })

            # Separate into decision dfs
            decision = returned_content.get('decision', 'Uncertain')
            if decision == 'Include':
                included_df = pd.concat([included_df, pd.DataFrame([returned_content])], ignore_index=True)
            elif decision == 'Exclude':
                excluded_df = pd.concat([excluded_df, pd.DataFrame([returned_content])], ignore_index=True)
            else:
                uncertain_df = pd.concat([uncertain_df, pd.DataFrame([returned_content])], ignore_index=True)
    output_path = f"slr/llm-output/{experiment_name}.xlsx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        included_df.to_excel(writer, sheet_name='Included', index=False)
        excluded_df.to_excel(writer, sheet_name='Excluded', index=False)
        uncertain_df.to_excel(writer, sheet_name='Uncertain', index=False)
        missing_df.to_excel(writer, sheet_name='Missing', index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    SYSTEM_ROLE = 'system'
    SYSTEM_PROMPT = 'You are a formal Research Reviewer Agent specialized in Decisions/Argument Modelling in Software engineering,MLOps and Ontology Engineering. Your task is to perform an initial screening of scientific literature for a Systematic Literature Review (SLR).'
    
    
    # ###########################RWTH GPT EMP############################
    # provider = 'rwth-gpt-emp'
    # model = "gpt-4o" #
    # experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)

    # ###########################RWTH GPT EMP############################
    # provider = 'rwth-gpt-emp'
    # model = "gpt-5.1" #
    # experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)

    # ###########################RWTH GPT############################
    # provider = 'rwth-gpt'
    # model = "mixtral-8x22B" #mixtral-8x22B, mistral-small-3.2-24B-instruct-2506, gpt-oss-120b
    # experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)
    ############################RWTH GPT############################
    provider = 'rwth-gpt'
    model = "mistral-small-3.2-24B-instruct-2506" #mixtral-8x22B, mistral-small-3.2-24B-instruct-2506, gpt-oss-120b
    experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)
    ############################RWTH GPT############################
    provider = 'rwth-gpt'
    model = "gpt-oss-120b" #mixtral-8x22B, mistral-small-3.2-24B-instruct-2506, gpt-oss-120b
    experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)

    ############################GROQ############################
    provider = 'groq'
    model = "llama-3.1-8b-instant" #llama-3.1-8b-instant, llama-3.3-70b-versatile
    experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)

    ############################GROQ############################
    # provider = 'groq'
    # model = "llama-3.3-70b-versatile" #llama-3.1-8b-instant, llama-3.3-70b-versatile
    # experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)

    ############################RWTH GPT EMP############################
    # provider = 'rwth-gpt-emp'
    # model = "gpt-4o" #
    # experiment_name = f"{model}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    # screen_papers(experiment_name, provider, model, SYSTEM_ROLE, SYSTEM_PROMPT)


