from base import Base
from sklearn.neural_network import MLPClassifier

class MLP(Base):
    def __init__(self, file, filename, i, data, epochs, batch, learning_rate, 
            layers_n, layer_size):
        Base.__init__(self, file, filename, i)
        self.data = data
        self.epochs = epochs
        self.batch = batch
        self.learning_r = learning_rate
        self.layers_n = layers_n
        self.layer_size = layer_size
        self.__run()

    def __run(self):
        clf = MLPClassifier(batch_size=self.batch, 
                hidden_layer_sizes=(self.layer_size, self.layers_n), 
                learning_rate_init=self.learning_r, random_state=1)
        clf.fit(self.data.X_train, self.data.y_train)
        self.prediction = clf.predict(self.data.X_test)
        pass

    def scores(self, out):
        super(MLP, self).scores(self.prediction, self.data.y_test, out, 
                self.epochs, self.batch, self.learning_r, self.layers_n,
                self.layer_size)
        pass
    

    # epochs = [10, 50, 100, 500, 5000]
    # batch = [10, 50, 200]
    # learning_rate = [0.1, 0.01, 0.001, 0.0001]
    # layers_n = [1, 2]
    # layer_size = [10, 50, 100, 500, 1000]
    