def run():
   import os
   # Google introduced an incompatibility into protobuf-4.21.0
   # that is not backwards compatible with many libraries.  
   # Once those libraries have updated to rebuild their _pb2.py files,
   # this can be removed.
   os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
   import tensorflow as tf
   import tensorflow_hub as hub
   import tensorflow_text as text

   import pandas as pd

   data_path = 'https://wavta-nlp-data.s3.us-east-2.amazonaws.com/comparative3.csv'
   df = pd.read_csv(data_path)
   df.head()

   df.groupby('Category').describe()

   df['cp'] = df['Category'].apply(lambda x: 1 if x=='comp' else 0)
   df.head()

   # train-test split
   from sklearn.model_selection import train_test_split

   X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['cp'], stratify=df['cp'])

   X_train.head()

   bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
   bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

   def get_sentence_embeding(sentences):
      preprocessed_text = bert_preprocess(sentences)
      return bert_encoder(preprocessed_text)['pooled_output']

   # get_sentence_embeding([
   #     "500$ discount. hurry up", 
   #     "Bhavin, are you up for a volleybal game tomorrow?"]
   # )

   # build functional model

   # Bert layers
   text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
   preprocessed_text = bert_preprocess(text_input)
   outputs = bert_encoder(preprocessed_text)

   # Neural network layers
   l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
   l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

   # Use inputs and outputs to construct a final model
   model = tf.keras.Model(inputs=[text_input], outputs = [l])

   model.summary()

   model.compile(optimizer='adam',
               loss='binary_crossentropy',
               metrics=['accuracy'])

   model.fit(X_train, y_train, epochs=15)

   model.evaluate(X_test, y_test)

   test_ct = [
      "Is $O(2^n)$ faster than $O(n!)$?",
      "Compare growth rate of functions $n$, $n^2$, $n^n$.",
      "Is $o(n)$ quicker than $O(\\log_2n)$?",
      "Which is faster, $O(1/n)$ or $O(\\log_10n)$?",
      "What is Strassen's algorithm?",
      "How fast is selection sort?",
      "Time complexity of selection sort.",
      "What is Big-Omega notation?",
            ]

   model.predict(test_ct)
   model.save('src/haystack/pipeline/comp_nn_model')

if __name__ == '__main__':
   run()
