import json
import os
import click
import plotly.express as px
from better_profanity import profanity
from dotenv import load_dotenv
import openai
from collections import Counter
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_comments(file_path: str) -> List[Dict[str, Any]]:
    """Load comments from JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['comments']

def analyze_comment(comment_text: str) -> Dict[str, Any]:
    """Analyze a comment using OpenAI's API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a content moderation assistant. Analyze the comment and respond with a JSON containing: is_offensive (true/false), offense_type (if applicable: hate_speech, toxicity, profanity, harassment, or none), severity (1-5 where 1 is least severe and 5 is most severe), and a brief explanation."},
                {"role": "user", "content": comment_text}
            ],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Error analyzing comment: {e}")
        return {
            "is_offensive": False,
            "offense_type": "error",
            "severity": 1,
            "explanation": "Error in analysis"
        }

def plot_offense_distribution(offense_types: Dict[str, int], output_file: str):
    """Create a bar chart showing offense type distribution."""
    fig = px.bar(
        x=list(offense_types.keys()),
        y=list(offense_types.values()),
        labels={'x': 'Offense Type', 'y': 'Number of Comments'},
        title='Distribution of Offense Types'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        width=800,
        height=600
    )
    fig.write_html(output_file)

def plot_severity_distribution(comments: List[Dict[str, Any]], output_file: str):
    """Create a pie chart showing severity distribution."""
    severity_counts = Counter(c.get('severity', 1) for c in comments if c['is_offensive'])
    
    fig = px.pie(
        names=[f"Severity {k}" for k in severity_counts.keys()],
        values=list(severity_counts.values()),
        title='Severity Distribution of Offensive Comments'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        width=800,
        height=600
    )
    fig.write_html(output_file)

def generate_report(analyzed_comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a summary report of the analysis."""
    total_comments = len(analyzed_comments)
    offensive_comments = sum(1 for c in analyzed_comments if c['is_offensive'])
    offense_types = Counter(c['offense_type'] for c in analyzed_comments if c['is_offensive'])
    
    # Sort comments by severity (most severe first)
    most_offensive = sorted(
        [c for c in analyzed_comments if c['is_offensive']],
        key=lambda x: x.get('severity', 1),
        reverse=True
    )[:5]
    
    # Get all offensive comments
    all_offensive = [c for c in analyzed_comments if c['is_offensive']]
    
    return {
        'total_comments': total_comments,
        'offensive_comments': offensive_comments,
        'offense_types': dict(offense_types),
        'most_offensive': most_offensive,
        'all_offensive': all_offensive
    }

def export_to_json(analyzed_comments: List[Dict[str, Any]], output_file: str):
    """Export analyzed comments to JSON."""
    with open(output_file, 'w') as f:
        json.dump(analyzed_comments, f, indent=2)

@click.command()
@click.option('--input-file', default='data/comments.json', help='Input JSON file containing comments')
@click.option('--output-file', default='output/analyzed_comments.json', help='Output file name')
@click.option('--filter-offensive/--no-filter-offensive', default=False, help='Filter output to only include offensive comments')
@click.option('--create-plots/--no-create-plots', default=True, help='Create visualization plots')
@click.option('--plot-format', type=click.Choice(['html', 'png']), default='html', help='Format for visualization plots')
def main(input_file: str, output_file: str, filter_offensive: bool, create_plots: bool, plot_format: str):
    """Main function to process and analyze comments."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Load comments
    print("Loading comments...")
    comments = load_comments(input_file)
    print(f"Loaded {len(comments)} comments")
    
    # Pre-filter using profanity check
    profanity.load_censor_words()
    
    # Analyze comments
    print("\nAnalyzing comments...")
    for comment in comments:
        # Pre-filter with profanity check
        comment['contains_profanity'] = profanity.contains_profanity(comment['comment_text'])
        
        # Analyze with OpenAI
        analysis = analyze_comment(comment['comment_text'])
        comment.update(analysis)
    
    # Generate report
    report = generate_report(comments)
    
    # Filter comments if requested
    if filter_offensive:
        comments = [c for c in comments if c['is_offensive']]
        output_file = output_file.replace('.json', '_offensive.json')
    
    # Export results
    export_to_json(comments, output_file)
    
    # Create visualizations if requested
    if create_plots and report['offense_types']:
        # Create offense type distribution plot
        plot_file = os.path.splitext(output_file)[0] + '_offense_distribution.' + plot_format
        plot_offense_distribution(report['offense_types'], plot_file)
        print(f"\nOffense type distribution chart saved as '{plot_file}'")
        
        # Create severity distribution plot
        severity_file = os.path.splitext(output_file)[0] + '_severity_distribution.' + plot_format
        plot_severity_distribution(comments, severity_file)
        print(f"Severity distribution chart saved as '{severity_file}'")
    
    # Print summary
    print("\nAnalysis Summary:")
    print(f"Total comments analyzed: {report['total_comments']}")
    print(f"Offensive comments found: {report['offensive_comments']}")
    print("\nOffense type breakdown:")
    for offense_type, count in report['offense_types'].items():
        print(f"- {offense_type}: {count}")
    
    if report['all_offensive']:
        print("\nAll Offensive Comments:")
        for idx, comment in enumerate(report['all_offensive'], 1):
            print(f"\n{idx}. Username: {comment['username']}")
            print(f"Comment: {comment['comment_text']}")
            print(f"Type: {comment['offense_type']}")
            print(f"Severity: {comment.get('severity', 1)}")
            print(f"Explanation: {comment['explanation']}")
    
    if report['most_offensive']:
        print("\nTop 5 Most Severe Offensive Comments:")
        for idx, comment in enumerate(report['most_offensive'], 1):
            print(f"\n{idx}. Username: {comment['username']}")
            print(f"Comment: {comment['comment_text']}")
            print(f"Type: {comment['offense_type']}")
            print(f"Severity: {comment.get('severity', 1)}")
            print(f"Explanation: {comment['explanation']}")
    
    print(f"\nFull analysis saved to {output_file}")

if __name__ == '__main__':
    main()
