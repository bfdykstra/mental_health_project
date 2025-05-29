# Patient Prompt Tagging Script

This script uses an LLM with Python Instructor to generate 1-4 tags for each patient prompt in your CSV data. The tags are designed to be used as search keyword metadata within a vector database to help mental health counselors find relevant examples.

## Features

- **Structured Outputs**: Uses Python Instructor with Pydantic models to ensure consistent tag generation
- **Flexible LLM Support**: Works with OpenAI API or local models (like Ollama)
- **Resume Capability**: Can resume processing from any row if interrupted
- **Progress Tracking**: Shows progress and saves incrementally
- **Error Handling**: Graceful error handling with fallback tags

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Choose Your LLM Option**

   ### Option A: OpenAI API

   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - Set the environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - Or pass it directly using `--api-key` parameter

   ### Option B: Local Model (Ollama)

   - Install [Ollama](https://ollama.ai/)
   - Pull a model: `ollama pull llama2` or `ollama pull mistral`
   - Start Ollama: `ollama serve`

## Usage

### Basic Usage (with OpenAI)

```bash
python tag_prompts.py
```

### With Custom Parameters

```bash
python tag_prompts.py \
  --input data/pair_data.csv \
  --output data/pair_data_tagged.csv \
  --model gpt-3.5-turbo \
  --max-rows 50
```

### Resume from Specific Row

```bash
python tag_prompts.py --start-row 100 --max-rows 50
```

## Command Line Options

- `--input`: Input CSV file path (default: `data/pair_data.csv`)
- `--output`: Output CSV file path (default: `data/pair_data_tagged.csv`)
- `--api-key`: OpenAI API key (or set `OPENAI_API_KEY` env var)
- `--base-url`: Custom base URL for local models (e.g., `http://localhost:11434/v1`)
- `--model`: Model name to use (default: `gpt-3.5-turbo`)
- `--start-row`: Row to start processing from (default: 0)
- `--max-rows`: Maximum number of rows to process

## Testing

Before running on the full dataset, test with a few samples:

```bash
python test_tagging.py
```

This will process 3 sample prompts and show you the generated tags.

## Example Output

The script adds a new `tags` column to your CSV with comma-separated tags:

| prompt                                                         | tags                                                   |
| -------------------------------------------------------------- | ------------------------------------------------------ |
| "I know I am too big, and I probably should exercise more..."  | weight management, exercise barriers, time constraints |
| "I don't trust doctors. I don't trust the CDC..."              | vaccine hesitancy, medical distrust, COVID-19          |
| "Of course, I would like to lose weight and not feel gross..." | body image, diet frustration, weight loss              |

## Tag Quality

The generated tags are designed to be:

- **Concise**: 1-3 words each
- **Specific**: Relevant to healthcare/mental health contexts
- **Searchable**: Useful for finding similar cases in a vector database
- **Comprehensive**: Cover main themes in each prompt

## Troubleshooting

1. **OpenAI API Key Issues**

   - Ensure your API key is set correctly
   - Check your OpenAI account has sufficient credits

2. **Local Model Issues**

   - Ensure Ollama is running: `ollama serve`
   - Check model is pulled: `ollama list`
   - Verify the base URL: `http://localhost:11434/v1`

3. **Memory Issues**

   - Process in smaller batches using `--max-rows`
   - Use `--start-row` to resume processing

4. **Network Issues**
   - The script saves progress every 10 rows
   - Resume from the last saved point using `--start-row`

## File Structure

```
.
├── tag_prompts.py          # Main tagging script
├── test_tagging.py         # Test script for verification
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── data/
    ├── pair_data.csv      # Input data
    └── pair_data_tagged.csv # Output with tags
```
