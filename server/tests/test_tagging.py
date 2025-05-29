#!/usr/bin/env python3
"""
Test script to verify the async tagging functionality on a few sample prompts.
"""

import asyncio
import pandas as pd
from scripts.tag_prompts import setup_async_client, tag_single_prompt_async

async def test_tagging_async():
    """Test the async tagging functionality on sample prompts"""
    
    # Sample prompts from the data
    sample_prompts = [
        "I know I am too big, and I probably should exercise more and eat better, but I am so busy. I've got school, homework, and my job at the mall, so I don't see anywhere to fit it in.",
        "I don't trust doctors. I don't trust the CDC. God gave us an immune system and as a healthy person that is all I need to protect myself from getting COVID.",
        "Of course, I would like to lose weight and not feel gross all the time. But I hate all the diets my mom puts me on."
    ]
    
    print("Setting up async client...")
    client, model = setup_async_client()
    print(f"Using model: {model}")
    
    # Process all prompts concurrently
    tasks = [tag_single_prompt_async(client, model, prompt, i) 
             for i, prompt in enumerate(sample_prompts)]
    
    results = await asyncio.gather(*tasks)
    
    for i, (idx, tags) in enumerate(results):
        print(f"\n--- Sample {i+1} ---")
        print(f"Prompt: {sample_prompts[i]}")
        print(f"Generated tags: {', '.join(tags)}")

def test_tagging():
    """Wrapper to run async test"""
    asyncio.run(test_tagging_async())

if __name__ == "__main__":
    test_tagging() 