import tensorflow as tf
import random


class BaseAttention(tf.keras.layers.Layer):
  def __init__(self, **kwargs):
    super().__init__()
    self.mha = tf.keras.layers.MultiHeadAttention(**kwargs)
    self.layernorm = tf.keras.layers.LayerNormalization()
    self.add = tf.keras.layers.Add()

class GlobalSelfAttention(BaseAttention):
  def call(self, x):
    attn_output = self.mha(
        query=x,
        value=x,
        key=x)
    x = self.add([x, attn_output])
    x = self.layernorm(x)
    return x
  

class FeedForward(tf.keras.layers.Layer):
  def __init__(self, d_model, dff, dropout_rate=0.1):
    super().__init__()
    self.seq = tf.keras.Sequential([
      tf.keras.layers.Dense(dff, activation='relu'),
      tf.keras.layers.Dense(d_model),
      tf.keras.layers.Dropout(dropout_rate)
    ])
    self.add = tf.keras.layers.Add()
    self.layer_norm = tf.keras.layers.LayerNormalization()

  def call(self, x):
    x = self.add([x, self.seq(x)])
    x = self.layer_norm(x) 
    return x
  


class Selector(tf.keras.Model):
  def __init__(self, *, d_model, num_heads, dff, output_size, dropout_rate=0.1):
    super().__init__()
    self.first_att = GlobalSelfAttention(num_heads=num_heads, key_dim=d_model, dropout=dropout_rate)
    self.first_ffn = FeedForward(d_model, dff)

    self.final_layer = tf.keras.layers.Dense(output_size)

  def call(self, inputs):
    x = self.first_att(inputs)
    x = self.first_ffn(x)
    logits = self.final_layer(x)

    return logits


selector = Selector(d_model=3, num_heads=8, dff=32, output_size=1)


test_data = tf.constant([[[random.random() for i in range(3)] for j in range(60)]], dtype='float32')
target_out = [[0.0] for j in range(10)]
target_out.append([1.0])
for j in range(6):
    target_out.append([0.0])
target_out.append([1.0])
for j in range(24):
    target_out.append([0.0])
target_out.append([1.0])
for j in range(17):
    target_out.append([0.0])
target_out = tf.constant([target_out], dtype="float32")


optimizer = tf.keras.optimizers.Adam(weight_decay=1e-4)

selector.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=optimizer)
selector.fit(x=test_data, y=target_out, epochs=10000)

for x in selector(test_data):
  for y in x:
    for z in y:
      tf.print(z)
