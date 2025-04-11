# Comment Moderation System

This Python application analyzes user comments for offensive content using OpenAI's GPT model and generates detailed reports.

## Features

- Reads comments from JSON files
- Uses OpenAI's GPT model for content analysis
- Pre-filters content using better-profanity library
- Generates detailed reports with offense types and explanations
- Creates interactive visualizations of offense distribution
- Command-line interface for easy use
- Supports filtering of offensive content
- Multiple output formats (JSON, HTML)

## Deliverables

### 1. Python Scripts
- `comment_moderator.py`: Main script for comment analysis
- `test_openai.py`: Script for testing OpenAI API connection

### 2. Sample Input File
- `data/comments.json`: Sample input file containing comments to analyze

### 3. Sample Output Files
- `output/analyzed_comments.json`: JSON file containing analyzed comments
- `output/analyzed_comments_offense_distribution.html`: Interactive bar chart showing offense type distribution
- `output/analyzed_comments_severity_distribution.html`: Interactive pie chart showing severity distribution
- `output/analyzed_comments_offensive.json`: Filtered output containing only offensive comments

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Basic Usage
```bash
python comment_moderator.py
```

### Custom Options
```bash
python comment_moderator.py \
    --input-file path/to/comments.json \
    --output-file path/to/output.json \
    --filter-offensive \
    --create-plots \
    --plot-format html  # or png
```

### Available Options
- `--input-file`: Path to input JSON file (default: data/comments.json)
- `--output-file`: Path to output JSON file (default: output/analyzed_comments.json)
- `--filter-offensive`: Filter output to only include offensive comments
- `--create-plots`: Create visualization plots (default: True)
- `--plot-format`: Format for visualization plots (html/png, default: html)

## Input Format

The input JSON file should have the following structure:
```json
{
    "comments": [
        {
            "comment_id": 1,
            "username": "user123",
            "comment_text": "Comment content here"
        }
    ]
}
```

## Output Format

The output JSON will contain:
```json
{
    "comment_id": 1,
    "username": "user123",
    "comment_text": "Comment content here",
    "contains_profanity": true,
    "is_offensive": true,
    "offense_type": "hate_speech",
    "severity": 4,
    "explanation": "The comment contains hate speech and is directed towards a group of people based on their origin, which is discriminatory and offensive."
}
```

## Visualizations

The script generates two interactive visualizations:
1. **Offense Type Distribution**: Bar chart showing the distribution of different offense types
2. **Severity Distribution**: Pie chart showing the distribution of severity levels among offensive comments

## Requirements

- Python 3.12+
- OpenAI API key
- Required packages listed in `requirements.txt`

## Sample Analysis

The script provides:
1. Total number of comments analyzed
2. Number of offensive comments found
3. Breakdown of offense types
4. List of all offensive comments with details
5. Top 5 most severe offensive comments
6. Interactive visualizations

## Troubleshooting

1. If you encounter API errors:
   - Check your OpenAI API key
   - Verify internet connection
   - Check rate limits

2. If visualizations don't work:
   - Ensure you have the required dependencies
   - Try using a different plot format (html/png)


