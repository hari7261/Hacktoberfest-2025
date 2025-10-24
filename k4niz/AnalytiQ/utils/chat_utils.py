"""
Chat Utilities for AnalytiQ
Gemini API integration for AI explanations and chat
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None


def ask_ai(df, target_col, question):
    """
    Ask AI a question about the dataset
    """
    if not model:
        return "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in .env file."
    
    # Prepare dataset context
    context = f"""
Dataset Information:
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Target Column: {target_col if target_col else 'Not specified'}

First few rows:
{df.head(3).to_string()}

Statistical Summary:
{df.describe().to_string()}

Missing Values:
{df.isnull().sum().to_string()}

Data Types:
{df.dtypes.to_string()}

User Question: {question}

Provide a clear, concise answer based on the dataset information above.
"""
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"


def explain_model_results(df, target_col, model_type, metrics):
    """
    Generate AI explanation of model results
    """
    if not model:
        return "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in .env file."
    
    # Prepare context
    metrics_str = "\n".join([f"- {k}: {v:.4f}" for k, v in metrics.items()])
    
    context = f"""
I trained a {model_type} model on a dataset with {df.shape[0]} rows and {df.shape[1]} columns.
The target variable is: {target_col}

Model Performance Metrics:
{metrics_str}

Dataset columns: {', '.join(df.columns.tolist())}

Please provide:
1. A brief interpretation of these results (2-3 sentences)
2. What the metrics tell us about model performance
3. One suggestion for potential improvement

Keep the explanation simple and actionable.
"""
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"


def get_data_insights(df):
    """
    Get AI-generated insights about the dataset
    """
    if not model:
        return "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in .env file."
    
    context = f"""
Analyze this dataset and provide 3-5 key insights:

Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns

Columns and Types:
{df.dtypes.to_string()}

Statistical Summary:
{df.describe().to_string()}

Missing Values:
{df.isnull().sum().to_string()}

First few rows:
{df.head(5).to_string()}

Provide insights about:
- Data quality
- Interesting patterns
- Potential relationships between variables
- Any anomalies or concerns
"""
    
    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"
