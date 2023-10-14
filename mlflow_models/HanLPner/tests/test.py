import mlflow
import pandas as pd

loaded_model = mlflow.pyfunc.load_model("")

test_data = pd.DataFrame(
    {
        "text": [
            "米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"
        ]
    }
)

test_predictions = loaded_model.predict(test_data)
print(test_predictions)
