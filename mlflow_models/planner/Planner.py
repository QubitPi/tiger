import graphlib
import mlflow.pyfunc
import pandas
import json

class Planner(mlflow.pyfunc.PythonModel):

    def __init__(self):
        pass

    def load_context(self, context):
        pass

    def predict(self, context, model_input):
        return pandas.Series(tuple(graphlib.TopologicalSorter(json.loads(model_input["text"][0])).static_order()))

if __name__ == '__main__':
    conda_env = {
        'channels': ['defaults'],
        'dependencies': [
            'python=3.10.7',
            'pip',
            {
                'pip': [
                    'mlflow',
                    'mlflow-skinny',
                    'mlflow[extras]',
                    'pandas=={}'.format(pandas.__version__)
                ],
            },
        ],
        'name': 'planner'
    }

    # Save the MLflow Model
    mlflow_pyfunc_model_path = "../models/planner"
    mlflow.pyfunc.save_model(path=mlflow_pyfunc_model_path, python_model=Planner(), conda_env=conda_env)

    loaded_model = mlflow.pyfunc.load_model(mlflow_pyfunc_model_path)

    test_data = pandas.DataFrame(
        {
            "text": [
                '{"D": ["B", "C"], "C": ["A"], "B": ["A"]}'
            ]
        }
    )

    test_predictions = loaded_model.predict(test_data)
    print(test_predictions.to_markdown())
