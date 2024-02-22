from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from tensorflow import keras
import pandas as pd
import numpy as np


class DescriptionClassification:
    def __init__(self):
        self.df_career = pd.read_parquet('entities/data/dfs/df_predict_career.parquet', engine='fastparquet')
        self.df_valid = pd.read_parquet('entities/data/dfs/df_validate_desc.parquet', engine='fastparquet')
        self.model_career = ''
        self.model_valid = ''
        self.desc_formatted = ''

    def transform_desc_in_array_tokenized(self, df, text):
        tok = Tokenizer()
        tok.fit_on_texts(df['desc'])
        encd_rev2 = tok.texts_to_sequences([text])
        pad_rev = pad_sequences(encd_rev2, maxlen=50, padding='post')
        self.desc_formatted = pad_rev

    def load_career_classification_model(self):
        json_file = open("entities/models/model_career_desc.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        new_model = model_from_json(loaded_model_json)
        new_model.load_weights("entities/models/model_career_desc.h5")
        self.model_career = new_model

    def load_desc_validation_model(self):
        json_file = open("entities/models/model_desc_valid.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        new_model = model_from_json(loaded_model_json)
        new_model.load_weights("entities/models/model_desc_valid.h5")
        self.model_valid = new_model

    def predict_text_in_desc_is_valid(self):
        y_pred = self.model_valid.predict(self.desc_formatted)
        y_pred = np.argmax(y_pred, axis=1)
        output = 'valid' if y_pred[0] == 1 else 'invalid'
        return output

    def predict_career_in_desc(self):
        y_pred = self.model_career.predict(self.desc_formatted)
        y_pred = np.argmax(y_pred, axis=1)
        if y_pred[0] == 0:
            output = 'backend'
        elif y_pred[0] == 1:
            output = 'frontend'
        elif y_pred[0] == 2:
            output = 'fullstack'
        elif y_pred[0] == 3:
            output = 'mobile'
        else:
            output = 'mobile_fullstack'
        return output