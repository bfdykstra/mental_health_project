#!/usr/bin/env python3
"""
Script to tag patient prompts using an LLM with structured outputs via Instructor.
Generates 1-4 search keywords for each patient prompt that can be used as search metadata.
"""

import asyncio
import csv
import os
import pandas as pd
from typing import List, Tuple, Dict
from pydantic import BaseModel, Field, validator
import instructor
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm
import argparse
import dotenv

dotenv.load_dotenv()

search_keywords = [
  "Coping Strategies",
  "Decision-Making & Motivation",
  "Stress & Burnout",
  "Depression",
  "Mood Disorders",
  "Behavioral Challenges",
  "Self-Esteem & Identity",
  "Identity, Stigma & Social Norms",
  "Parenting & Child Behavior",
  "Family Dynamics",
  "Romantic & Intimate Relationships",
  "Communication & Conflict Resolution",
  "Social Connection & Isolation",
  "Youth & Adolescence",
  "Weight Management",
  "Nutrition & Food Habits",
  "Body Image & Eating Disorders",
  "Physical Activity & Lifestyle",
  "Chronic Illness & Mental Health",
  "Medication & Treatment Adherence",
  "Healthcare Trust & Access",
  "Therapeutic Engagement",
  "Support Systems & Caregiving",
  "Life Transitions & Adjustment",
  "Grief & Loss",
  "Trauma & PTSD",
  "Trust & Safety",
  "Anxiety",
  "Sleep & Fatigue",
  "Substance Use & Addiction",
  "Other"
]

class PromptSearchKeywords(BaseModel):
    """Structured model for prompt search keywords"""
    search_keywords: List[str] = Field(
        description="1-4 relevant search keywords from the predefined list that capture key themes, health conditions, or concerns",
        min_items=1,
        max_items=4
    )
    
    @validator('search_keywords')
    def validate_keywords(cls, v):
        """Ensure all keywords are from the predefined list"""
        invalid_keywords = [keyword for keyword in v if keyword not in search_keywords]
        if invalid_keywords:
            raise ValueError(f"Invalid keywords: {invalid_keywords}. Must choose from predefined list.")
        return v

def setup_async_client(api_key: str = None, model: str = "gpt-4o-mini"):
    """
    Setup the async OpenAI client with Instructor
    
    Args:
        api_key: OpenAI API key (defaults to env var OPENAI_API_KEY)
        model: OpenAI Model name to use
    """
    client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    return instructor.from_openai(client), model

def create_tagging_prompt(patient_prompt: str) -> str:
    """Create the prompt for the LLM to generate search keywords"""
    keywords_list = '\n'.join([f"- {keyword}" for keyword in search_keywords])
    
    return f"""You are a healthcare assistant helping to categorize patient concerns for mental health counselors.

Given the following patient prompt, select 1-4 relevant search keywords from the predefined list below that best capture the key themes, health conditions, concerns, or topics mentioned. These keywords will be used as search metadata in a vector database to help counselors find similar cases.

IMPORTANT: You must ONLY choose keywords from this exact list (case-sensitive):

{keywords_list}

Guidelines:
- Select 1-4 keywords that best match the prompt content
- Choose the most specific and relevant keywords
- Prioritize keywords that capture the main themes
- Use the exact spelling and capitalization from the list above

Patient Prompt: "{patient_prompt}"

Select the most appropriate search keywords from the predefined list above."""

async def tag_single_prompt_async(client, model: str, prompt: str, idx: int) -> Tuple[int, List[str]]:
    """Tag a single prompt using the LLM asynchronously"""
    try:
        response = await client.chat.completions.create(
            model=model,
            response_model=PromptSearchKeywords,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful healthcare assistant that selects relevant search keywords for patient concerns from a predefined list. You must only use keywords from the provided list, with exact spelling and capitalization."
                },
                {
                    "role": "user", 
                    "content": create_tagging_prompt(prompt)
                }
            ],
            temperature=0.1,  # Lower temperature for more consistent keyword selection
            max_tokens=150
        )
        return idx, response.search_keywords
    except Exception as e:
        print(f"Error tagging prompt at index {idx}: {e}")
        # Return fallback keywords that exist in the predefined list
        return idx, ["Other"]

async def process_batch(client, model: str, batch_data: List[Tuple[int, str]], semaphore: asyncio.Semaphore) -> List[Tuple[int, List[str]]]:
    """Process a batch of prompts concurrently with rate limiting"""
    async with semaphore:
        tasks = [tag_single_prompt_async(client, model, prompt, idx) for idx, prompt in batch_data]
        return await asyncio.gather(*tasks, return_exceptions=True)

def create_batches(data: List[Tuple[int, str]], batch_size: int) -> List[List[Tuple[int, str]]]:
    """Create batches from the data"""
    batches = []
    for i in range(0, len(data), batch_size):
        batches.append(data[i:i + batch_size])
    return batches

async def process_csv_async(input_file: str, output_file: str, api_key: str = None, 
                           model: str = "gpt-4o-mini", start_row: int = 0, 
                           max_rows: int = None, batch_size: int = 5, 
                           max_concurrent: int = 10):
    """
    Process the CSV file and add search keywords to each prompt using async batch processing
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file  
        api_key: OpenAI API key
        model: Model name to use
        start_row: Row to start processing from (for resuming)
        max_rows: Maximum number of rows to process
        batch_size: Number of prompts to process in each batch
        max_concurrent: Maximum number of concurrent requests
    """
    # Setup client
    client, model_name = setup_async_client(api_key, model)
    
    # Create semaphore for rate limiting
    semaphore = asyncio.Semaphore(max_concurrent)
    
    # Read CSV
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} rows from {input_file}")
    
    # Handle resuming from a specific row
    if start_row > 0:
        print(f"Starting from row {start_row}")
    
    # Handle max rows
    end_row = min(len(df), start_row + max_rows) if max_rows else len(df)
    
    # Initialize search_keywords column if it doesn't exist
    if 'search_keywords' not in df.columns:
        df['search_keywords'] = ''
    
    # Prepare data for processing
    data_to_process = []
    for idx in range(start_row, end_row):
        row = df.iloc[idx]
        
        # Skip if already tagged
        if pd.notna(row['search_keywords']) and row['search_keywords'].strip():
            print(f"Row {idx} already tagged, skipping...")
            continue
            
        data_to_process.append((idx, row['prompt']))
    
    if not data_to_process:
        print("No rows to process!")
        return
    
    print(f"Processing {len(data_to_process)} rows in batches of {batch_size}")
    print(f"Maximum concurrent requests: {max_concurrent}")
    
    # Create batches
    batches = create_batches(data_to_process, batch_size)
    
    # Process batches with progress tracking
    processed_count = 0
    save_frequency = max(1, len(batches) // 10)  # Save 10 times throughout processing
    
    for batch_idx, batch in enumerate(tqdm(batches, desc="Processing batches")):
        print(f"\nProcessing batch {batch_idx + 1}/{len(batches)} with {len(batch)} prompts...")
        
        try:
            # Process batch
            results = await process_batch(client, model_name, batch, semaphore)
            
            # Update dataframe with results
            for result in results:
                if isinstance(result, Exception):
                    print(f"Error in batch processing: {result}")
                    continue
                    
                idx, keywords = result
                keywords_str = ', '.join(keywords)
                df.at[idx, 'search_keywords'] = keywords_str
                
                print(f"Row {idx}: {keywords_str}")
                processed_count += 1
            
            # Save progress periodically
            if (batch_idx + 1) % save_frequency == 0 or batch_idx == len(batches) - 1:
                df.to_csv(output_file, index=False)
                print(f"Progress saved to {output_file} ({processed_count} rows processed)")
                
        except Exception as e:
            print(f"Error processing batch {batch_idx}: {e}")
            continue
    
    # Final save
    df.to_csv(output_file, index=False)
    print(f"\nCompleted! Tagged data saved to {output_file}")
    print(f"Total rows processed: {processed_count}")
    
    # Show some examples
    print("\nExample tagged prompts:")
    tagged_count = 0
    for i in range(len(df)):
        if pd.notna(df.iloc[i]['search_keywords']) and df.iloc[i]['search_keywords'].strip():
            print(f"Prompt: {df.iloc[i]['prompt'][:100]}...")
            print(f"Keywords: {df.iloc[i]['search_keywords']}\n")
            tagged_count += 1
            if tagged_count >= 3:
                break

def process_csv(input_file: str, output_file: str, api_key: str = None, 
                base_url: str = None, model: str = "gpt-4o-mini", 
                start_row: int = 0, max_rows: int = None, batch_size: int = 5,
                max_concurrent: int = 10):
    """
    Wrapper function to run async processing
    """
    asyncio.run(process_csv_async(
        input_file=input_file,
        output_file=output_file,
        api_key=api_key,
        model=model,
        start_row=start_row,
        max_rows=max_rows,
        batch_size=batch_size,
        max_concurrent=max_concurrent
    ))

def main():
    parser = argparse.ArgumentParser(description="Tag patient prompts using LLM with async batch processing")
    parser.add_argument("--input", default="data/pair_data.csv", help="Input CSV file path")
    parser.add_argument("--output", default="data/pair_data_tagged.csv", help="Output CSV file path")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model name to use")
    parser.add_argument("--start-row", type=int, default=0, help="Row to start processing from")
    parser.add_argument("--max-rows", type=int, help="Maximum number of rows to process")
    parser.add_argument("--batch-size", type=int, default=5, help="Number of prompts to process in each batch")
    parser.add_argument("--max-concurrent", type=int, default=10, help="Maximum number of concurrent requests")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found!")
        return
    
    print(f"Using model: {args.model}")
    print(f"Available search keywords: {len(search_keywords)} categories")
    print(f"Batch size: {args.batch_size}")
    print(f"Max concurrent requests: {args.max_concurrent}")
    
    process_csv(
        input_file=args.input,
        output_file=args.output,
        api_key=args.api_key,
        model=args.model,
        start_row=args.start_row,
        max_rows=args.max_rows,
        batch_size=args.batch_size,
        max_concurrent=args.max_concurrent
    )

if __name__ == "__main__":
    main() 