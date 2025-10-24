"""
Model Utilities for AnalytiQ
Auto ML model selection, training, and evaluation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)
import plotly.graph_objects as go
import plotly.express as px


def detect_feature_types(df, target_col):
    """
    Detect numerical and categorical features
    """
    features = df.drop(columns=[target_col])
    
    numerical_features = features.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = features.select_dtypes(include=['object', 'category']).columns.tolist()
    
    return {
        'numerical': numerical_features,
        'categorical': categorical_features
    }


def select_model(df, target_col):
    """
    Auto-select model based on target column type
    Returns: (model_type, model_instance)
    """
    target = df[target_col]
    
    # Determine problem type
    if target.dtype == 'object' or target.nunique() < 10:
        # Classification
        model_type = 'classification'
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        # Regression
        model_type = 'regression'
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    return model_type, model


def preprocess_data(df, target_col):
    """
    Preprocess data: handle missing values, encode categoricals
    """
    df_processed = df.copy()
    
    # Handle missing values
    for col in df_processed.columns:
        if df_processed[col].dtype in ['int64', 'float64']:
            df_processed[col].fillna(df_processed[col].median(), inplace=True)
        else:
            df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    
    # Separate features and target
    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col]
    
    # Encode categorical features
    label_encoders = {}
    for col in X.select_dtypes(include=['object', 'category']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    # Encode target if categorical
    if y.dtype == 'object':
        target_encoder = LabelEncoder()
        y = target_encoder.fit_transform(y)
    else:
        target_encoder = None
    
    return X, y, label_encoders, target_encoder


def train_model(df, target_col, model):
    """
    Train the selected model
    Returns: trained_model, X_train, X_test, y_train, y_test
    """
    # Preprocess data
    X, y, label_encoders, target_encoder = preprocess_data(df, target_col)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model.fit(X_train_scaled, y_train)
    
    # Store preprocessors with model
    model.scaler = scaler
    model.label_encoders = label_encoders
    model.target_encoder = target_encoder
    
    return model, X_train_scaled, X_test_scaled, y_train, y_test


def evaluate_model(model, X_test, y_test, model_type):
    """
    Evaluate model performance
    """
    y_pred = model.predict(X_test)
    
    if model_type == 'regression':
        metrics = {
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'MAE': mean_absolute_error(y_test, y_pred),
            'R² Score': r2_score(y_test, y_pred)
        }
    else:
        # For multiclass, use weighted average
        avg_type = 'weighted' if len(np.unique(y_test)) > 2 else 'binary'
        metrics = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, average=avg_type, zero_division=0),
            'Recall': recall_score(y_test, y_pred, average=avg_type, zero_division=0),
            'F1 Score': f1_score(y_test, y_pred, average=avg_type, zero_division=0)
        }
    
    return {
        'metrics': metrics,
        'y_pred': y_pred,
        'y_test': y_test,
        'X_test': X_test
    }


def generate_visualizations(model, X_test, y_test, y_pred, model_type):
    """
    Generate visualizations based on model type
    """
    figs = []
    
    if model_type == 'regression':
        # Actual vs Predicted
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=y_test,
            y=y_pred,
            mode='markers',
            name='Predictions',
            marker=dict(color='blue', size=8)
        ))
        fig1.add_trace(go.Scatter(
            x=[y_test.min(), y_test.max()],
            y=[y_test.min(), y_test.max()],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        fig1.update_layout(
            title='Actual vs Predicted Values',
            xaxis_title='Actual',
            yaxis_title='Predicted',
            height=400
        )
        figs.append(fig1)
        
        # Residual plot
        residuals = y_test - y_pred
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=y_pred,
            y=residuals,
            mode='markers',
            marker=dict(color='green', size=8)
        ))
        fig2.add_hline(y=0, line_dash="dash", line_color="red")
        fig2.update_layout(
            title='Residual Plot',
            xaxis_title='Predicted Values',
            yaxis_title='Residuals',
            height=400
        )
        figs.append(fig2)
        
    else:
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        fig1 = go.Figure(data=go.Heatmap(
            z=cm,
            x=[f'Pred {i}' for i in range(cm.shape[1])],
            y=[f'True {i}' for i in range(cm.shape[0])],
            colorscale='Blues',
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 16}
        ))
        fig1.update_layout(
            title='Confusion Matrix',
            xaxis_title='Predicted Label',
            yaxis_title='True Label',
            height=400
        )
        figs.append(fig1)
    
    # Feature Importance (for tree-based models)
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[-10:]  # Top 10
        
        fig3 = go.Figure(go.Bar(
            x=importances[indices],
            y=[f'Feature {i}' for i in indices],
            orientation='h',
            marker=dict(color='purple')
        ))
        fig3.update_layout(
            title='Top 10 Feature Importances',
            xaxis_title='Importance',
            yaxis_title='Feature',
            height=400
        )
        figs.append(fig3)
    
    return figs
