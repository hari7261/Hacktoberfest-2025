**Contributor:** k4niz


# AnalytiQ - Predictive DataChat 📊

**An intelligent ML chatbot that analyzes datasets, trains predictive models, and answers your questions using AI.**

AnalytiQ combines automated machine learning with conversational AI to make data analysis accessible to everyone. Upload a CSV, and let AnalytiQ handle the rest!

---

## ✨ Features

- ** Easy Data Upload**: Simply upload a CSV file to get started
- ** Automatic Analysis**: Detects data types, identifies missing values, and generates statistics
- ** Auto ML**: Automatically selects the best model (regression or classification)
- ** Interactive Visualizations**: Beautiful charts and plots powered by Plotly
- ** AI Chat Interface**: Ask questions about your data using Gemini AI
- ** Model Evaluation**: Comprehensive metrics and performance insights
- ** Model Download**: Save trained models for later use
- ** Example Datasets**: Includes sample datasets to try out

---

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   cd Domains/AI-ML/MiniProjects/AnalytiQ
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Upload Dataset
- Click "Browse files" in the sidebar
- Select a CSV file from your computer
- Or try the example datasets (`data/student_marks.csv` or `data/stock_data.csv`)

### 2. Explore Data
- View the **Data Preview** tab to see your dataset
- Check statistics, missing values, and data types

### 3. Train Model
- Go to the **Train Model** tab
- Select the target column you want to predict
- Click " Train Model"
- AnalytiQ will automatically:
  - Detect if it's regression or classification
  - Handle missing values
  - Encode categorical features
  - Train the best model

### 4. View Results
- Check the **Results** tab for:
  - Performance metrics (RMSE, R², Accuracy, F1, etc.)
  - Visualizations (Actual vs Predicted, Confusion Matrix, Feature Importance)
  - AI-generated explanations
  - Download trained model as `.pkl` file

### 5. Ask AI
- Navigate to the **Ask AI** tab
- Use quick questions or ask custom questions
- Get insights about your data, patterns, and recommendations

---

## 🛠️ Project Structure

```
AnalytiQ/
├── app.py                    # Main Streamlit application
├── utils/
│   ├── model_utils.py       # ML model training and evaluation
│   └── chat_utils.py        # Gemini AI integration
├── data/
│   ├── student_marks.csv    # Example dataset 1
│   └── stock_data.csv       # Example dataset 2
├── models/                   # Saved models (gitignored)
├── templates/                # Future HTML templates
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

##  How It Works

### Auto ML Pipeline

1. **Data Detection**: Analyzes data types and target variable
2. **Preprocessing**: 
   - Fills missing values (median for numerical, mode for categorical)
   - Encodes categorical features using LabelEncoder
   - Scales features using StandardScaler
3. **Model Selection**:
   - **Regression**: RandomForestRegressor (for continuous targets)
   - **Classification**: RandomForestClassifier (for categorical targets)
4. **Training**: 80-20 train-test split with random state for reproducibility
5. **Evaluation**: 
   - Regression: RMSE, MAE, R² Score
   - Classification: Accuracy, Precision, Recall, F1 Score

### AI Chat

- Powered by **Gemini Pro** model
- Provides insights on:
  - Dataset summaries
  - Feature relationships
  - Data quality issues
  - Model performance explanations
  - Improvement suggestions

---

##  Example Datasets

### 1. Student Marks Dataset (`student_marks.csv`)
- **Use Case**: Predicting total marks based on subject scores
- **Type**: Regression
- **Features**: Math, Science, English
- **Target**: Total_Marks

### 2. Stock Data Dataset (`stock_data.csv`)
- **Use Case**: Predicting stock closing price
- **Type**: Regression
- **Features**: Open, High, Low, Volume, Date
- **Target**: Close

---

##  Configuration

### Supported Models

Currently, AnalytiQ uses:
- `RandomForestRegressor` for regression tasks
- `RandomForestClassifier` for classification tasks

You can modify `utils/model_utils.py` to add more models.

### Model Parameters

Default settings in `select_model()`:
- `n_estimators=100`: Number of trees in the forest
- `random_state=42`: For reproducibility

---

##  Contributing

Contributions are welcome! This project is part of **Hacktoberfest 2024**.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Ideas for Contribution

- Add more ML algorithms (XGBoost, LightGBM, Neural Networks)
- Implement hyperparameter tuning
- Add data preprocessing options (outlier removal, feature engineering)
- Support for more file formats (Excel, JSON, Parquet)
- Create more example datasets
- Improve UI/UX
- Add unit tests

---

##  License

This project is open source and available under the MIT License.

---

##  Acknowledgments

- **Streamlit** for the amazing web framework
- **Google Gemini** for AI capabilities
- **scikit-learn** for ML tools
- **Plotly** for interactive visualizations
- **ProjectHive** community for support

---

##  Contact

For questions or suggestions, please open an issue on GitHub.

---

##  Star This Project

If you find AnalytiQ useful, please give it a ⭐ on GitHub!

---

**Happy Analyzing! 📊✨**
