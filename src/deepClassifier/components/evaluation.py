import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from deepClassifier.entity import EvaluationConfig
from deepClassifier.utils import save_json,load_json
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix,classification_report

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            # validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            # subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )


    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)


    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.pred = self.model.predict(self.valid_generator)
        y=np.concatenate([self.valid_generator.next()[1] for i in range(self.valid_generator.__len__())])
        predicted = np.argmax(self.pred, axis=1)
        
        report = classification_report(np.argmax(y, axis=1), predicted)
        self.precision_score = precision_score(np.argmax(y, axis=1), predicted, average="macro")
        self.recall_score = recall_score(np.argmax(y, axis=1), predicted, average="macro")
        self.f1_score = f1_score (np.argmax(y, axis=1), predicted , average="macro")
        print(report)
        
        if Path("scores.json").exists():
            best_score = self.load_score(path=Path("scores.json"))
            if best_score['f1_score']>self.f1_score:
                self.save_score()
                self.save_model(path=Path(self.config.best_model_path),model=self.model)
        else:
            self.save_score()
            self.save_model(path=Path(self.config.best_model_path),model=self.model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
    @staticmethod
    def load_score(path: Path):
        return load_json(path)

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1],
                 "precision_score":self.precision_score,"recall_score":self.recall_score,"f1_score":self.f1_score}
        save_json(path=Path("scores.json"), data=scores)

    def log_into_mlflow(self):
        # self.CalibrationResults = self.model.calibrate()
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1],
                 "precision_score":self.precision_score,"recall_score":self.recall_score,"f1_score":self.f1_score}
            )
            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(self.model, "model", registered_model_name="EfficientNetV2M")
            else:
                mlflow.keras.log_model(self.model, "model")