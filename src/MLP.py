from base import Base
from sklearn.neural_network import MLPClassifier
from joblib import dump

class MLP(Base):
    def __init__(self, file, filename, i, data, epochs, batch, learning_rate, 
            layer_size, preprocess_name, file_id, 
            save_folder='../saved_models/'):
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
        clf = MLPClassifier(batch_size=self.batch, max_iter=50,
                hidden_layer_sizes=self.layer_size, 
                learning_rate_init=self.learning_r, random_state=1)
        clf.fit(self.data.X_train, self.data.y_train)
        self.prediction = clf.predict(self.data.X_test)
        save_file = self.file.split('/')[-1].split('.')[0] + '_MLP_ID' \
            + str(self.file_id) \
            + '_' + self.prepocess_name + '_random_state' + str(self.iter_n)
        dump(clf, self.save_folder + save_file + '.joblib')
        pass

    def scores(self, out):
        super(MLP, self).scores(self.prediction, self.data.y_test, out, 
                self.epochs, self.batch, self.learning_r, self.layer_size, 
                self.prepocess_name, self.file_id)
        pass