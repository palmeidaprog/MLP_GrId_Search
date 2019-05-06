from base import Base
from sklearn.neural_network import MLPClassifier
from joblib import dump

class MLP(Base):
    def __init__(self, file, filename, i, data, epochs, learning_rate, 
            layer_size, preprocess_name, file_id, 
            save_folder='../saved_models/', batch='auto'):
        Base.__init__(self, file, filename, i)
        self.data = data
        self.epochs = epochs
        self.batch = batch
        self.learning_r = learning_rate
        self.layer_size = layer_size
        self.prepocess_name = preprocess_name
        self.file_id = file_id
        self.save_folder = save_folder
        self.__run()

    def __run(self):
        print('Inside run MLP: ' + str(self.learning_r))
        clf = MLPClassifier(batch_size=self.batch, max_iter=self.epochs,
                hidden_layer_sizes=self.layer_size, 
                learning_rate_init=self.learning_r, random_state=1)
        clf.fit(self.data.X_train, self.data.y_train)
        self.clf = clf
        self.prediction = clf.predict(self.data.X_test)
        pass

    def scores(self, out):
        print('lr inside scores MLP: ' + str(self.learning_r))
        super(MLP, self).scores(self.prediction, self.data.y_test, out, 
                self.epochs, self.learning_r, self.layer_size, 
                self.prepocess_name, self.file_id)
        pass
