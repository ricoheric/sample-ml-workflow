import pytest
import pandas as pd
import numpy as np
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from ml_pipeline import load_data, preprocess_data, train_model

# 1. Test Data Loading
def test_data_loading():
    # Load the data
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
    
    # Ensure the dataset is loaded correctly
    assert not df.empty, "Dataset failed to load or is empty"
    assert df.shape[1] == 9, "The number of columns is not as expected in the dataset"
    assert "median_house_value" in df.columns, "Target column 'median_house_value' is missing"
    
# 2. Test Data Splitting
def test_data_splitting():
    # Load data
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Ensure data is split correctly
    assert X_train.shape[0] > 0, "Training data is empty"
    assert X_test.shape[0] > 0, "Test data is empty"
    assert X_train.shape[1] == X_test.shape[1], "Number of features doesn't match between training and test sets"

# 3. Test Model Pipeline Creation
def test_pipeline_creation():
    # Create a pipeline with StandardScaler and RandomForestRegressor
    pipe = Pipeline(steps=[
        ("standard_scaler", StandardScaler()),
        ("random_forest", RandomForestRegressor())
    ])
    
    # Check if the pipeline has the expected steps
    assert "standard_scaler" in pipe.named_steps, "Scaler step missing in the pipeline"
    assert "random_forest" in pipe.named_steps, "RandomForestRegressor step missing in the pipeline"
    
# 4. Test GridSearch and Model Training
def test_model_training():
    # Load data
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Create pipeline and parameters for GridSearchCV
    pipe = Pipeline(steps=[
        ("standard_scaler", StandardScaler()),
        ("random_forest", RandomForestRegressor())
    ])
    
    params_grid = {
        "random_forest__n_estimators": 10,
        "random_forest__criterion": ["squared_error"]
    }

    # Run GridSearchCV
    model = GridSearchCV(pipe, params_grid, n_jobs=-1, verbose=1, cv=3)
    model.fit(X_train, y_train)
    
    # Check if model is trained successfully
    assert model.best_params_ is not None, "GridSearchCV did not return best parameters"
    assert model.score(X_test, y_test) >= 0.0, "The model failed to score properly on the test set"

# 5. Test MLflow Logging
def test_mlflow_logging():
    experiment_name = "test_experiment"
    
    # Set experiment and start a new run
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)
    
    with mlflow.start_run(run_id=run.info.run_id) as run:
        # Log some metrics
        mlflow.log_metric("accuracy", 0.85)
        mlflow.log_param("n_estimators", 100)
        
        # Check if the run has been logged successfully
        run_data = client.get_run(run.info.run_id).data
        assert "accuracy" in run_data.metrics, "Metric 'accuracy' not logged to MLflow"
        assert "n_estimators" in run_data.params, "Parameter 'n_estimators' not logged to MLflow"
