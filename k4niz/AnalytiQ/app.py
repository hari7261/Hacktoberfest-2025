"""
AnalytiQ - Predictive DataChat
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import pickle
from utils.model_utils import (
    detect_feature_types,
    select_model,
    train_model,
    evaluate_model,
    generate_visualizations
)
from utils.chat_utils import ask_ai, explain_model_results

# Page configuration
st.set_page_config(
    page_title="AnalytiQ - Predictive DataChat",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'results' not in st.session_state:
    st.session_state.results = None

# Title and description
st.title("📊 AnalytiQ - Predictive DataChat")
st.markdown("Upload a dataset, and let AI analyze it, train a model, and answer your questions!")

# Sidebar for file upload
with st.sidebar:
    st.header(" Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Load dataset
        df = pd.read_csv(uploaded_file)
        st.session_state.dataset = df
        st.success(f"Loaded: {uploaded_file.name}")
        st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Main content area
if st.session_state.dataset is not None:
    df = st.session_state.dataset
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Preview", "🤖 Train Model", "📈 Results", "💬 Ask AI"])
    
    # Tab 1: Data Preview
    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10))
        
        st.subheader("Dataset Info")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        
        st.subheader("Statistical Summary")
        st.dataframe(df.describe())
    
    # Tab 2: Train Model
    with tab2:
        st.subheader("Model Training")
        
        # Select target column
        target_col = st.selectbox("Select target column for prediction:", df.columns)
        
        if st.button("🚀 Train Model", type="primary"):
            with st.spinner("Analyzing data and training model..."):
                try:
                    # Detect feature types
                    feature_types = detect_feature_types(df, target_col)
                    
                    # Select appropriate model
                    model_type, model = select_model(df, target_col)
                    
                    # Train model
                    trained_model, X_train, X_test, y_train, y_test = train_model(
                        df, target_col, model
                    )
                    
                    # Evaluate model
                    results = evaluate_model(trained_model, X_test, y_test, model_type)
                    
                    # Store in session state
                    st.session_state.model = trained_model
                    st.session_state.results = results
                    st.session_state.model_type = model_type
                    st.session_state.target_col = target_col
                    
                    st.success("✅ Model trained successfully!")
                    
                except Exception as e:
                    st.error(f"Error during training: {str(e)}")
    
    # Tab 3: Results
    with tab3:
        if st.session_state.results is not None:
            st.subheader("Model Performance")
            
            results = st.session_state.results
            model_type = st.session_state.model_type
            
            # Display metrics
            st.write(f"**Model Type:** {model_type.title()}")
            
            metrics_cols = st.columns(len(results['metrics']))
            for idx, (metric, value) in enumerate(results['metrics'].items()):
                with metrics_cols[idx]:
                    st.metric(metric, f"{value:.4f}")
            
            # Visualizations
            st.subheader("Visualizations")
            figs = generate_visualizations(
                st.session_state.model,
                results['X_test'],
                results['y_test'],
                results['y_pred'],
                model_type
            )
            
            for fig in figs:
                st.plotly_chart(fig, use_container_width=True)
            
            # Download model
            st.subheader("Download Trained Model")
            model_pkl = pickle.dumps(st.session_state.model)
            st.download_button(
                label="📥 Download Model (.pkl)",
                data=model_pkl,
                file_name=f"model_{st.session_state.target_col}.pkl",
                mime="application/octet-stream"
            )
            
            # AI Explanation
            st.subheader("🤖 AI Explanation")
            with st.spinner("Generating AI explanation..."):
                explanation = explain_model_results(
                    st.session_state.dataset,
                    st.session_state.target_col,
                    model_type,
                    results['metrics']
                )
                st.info(explanation)
        else:
            st.info("Train a model first to see results!")
    
    # Tab 4: Ask AI
    with tab4:
        st.subheader("💬 Ask AI About Your Data")
        
        # Predefined questions
        st.write("**Quick Questions:**")
        quick_questions = [
            "Summarize this dataset in 2 sentences",
            "What are the top 3 features influencing the output?",
            "Are there any data quality issues?",
            "What patterns do you see in this data?"
        ]
        
        for q in quick_questions:
            if st.button(q):
                with st.spinner("Thinking..."):
                    answer = ask_ai(df, st.session_state.target_col if 'target_col' in st.session_state else None, q)
                    st.success(answer)
        
        # Custom question
        st.write("**Custom Question:**")
        user_question = st.text_input("Ask anything about your dataset:")
        if st.button("Ask") and user_question:
            with st.spinner("Thinking..."):
                answer = ask_ai(df, st.session_state.target_col if 'target_col' in st.session_state else None, user_question)
                st.success(answer)

else:
    # Welcome screen
    st.info("👈 Upload a CSV file from the sidebar to get started!")
    
    st.subheader("Example Datasets")
    st.write("Try these example datasets:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Student Marks Dataset"):
            st.info("Load data/student_marks.csv from the sidebar")
    with col2:
        if st.button("📈 Stock Data Dataset"):
            st.info("Load data/stock_data.csv from the sidebar")
