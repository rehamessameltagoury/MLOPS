import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("taxi-expirement-HW")

@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    with mlflow.start_run():
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        mlflow.sklearn.autolog()
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        params = {
        'max_depth': 10,
        'random_state': 0
        }
        mlflow.log_params(params)
       
if __name__ == '__main__':
    run_train()
