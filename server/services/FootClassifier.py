import tensorflow as tf
from tensorflow.keras import layers, Model

class Classifier(Model):
    def __init__(self):
        super(Classifier, self).__init__()
        self.conv1 = layers.Conv2D(32, (3, 3), activation='relu')
        self.maxpool1 = layers.MaxPooling2D((2, 2))
        self.conv2 = layers.Conv2D(64, (3, 3), activation='relu')
        self.maxpool2 = layers.MaxPooling2D((2, 2))
        self.flatten = layers.Flatten()
        self.d1 = layers.Dense(64, activation='relu')
        self.d2 = layers.Dense(6, activation='softmax')

    def call(self, x):
        x = tf.cast(x, tf.float32)
        x = self.conv1(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)

# Create an instance of the model
model = Classifier()

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])