#!/usr/bin/env python

# Deep Learning Homework 1

import argparse
import random
import os

import numpy as np
import matplotlib.pyplot as plt

import utils


def configure_seed(seed):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


class LinearModel(object):
    def __init__(self, n_classes, n_features, **kwargs):
        self.W = np.zeros((n_classes, n_features))

    def update_weight(self, x_i, y_i, **kwargs):
        raise NotImplementedError

    def train_epoch(self, X, y, **kwargs):
        for x_i, y_i in zip(X, y):
            self.update_weight(x_i, y_i, **kwargs)

    def predict(self, X):
        """X (n_examples x n_features)"""
        scores = np.dot(self.W, X.T)  # (n_classes x n_examples)
        predicted_labels = scores.argmax(axis=0)  # (n_examples)
        return predicted_labels

    def evaluate(self, X, y):
        """
        X (n_examples x n_features):
        y (n_examples): gold labels
        """
        y_hat = self.predict(X)
        n_correct = (y == y_hat).sum()
        n_possible = y.shape[0]
        return n_correct / n_possible


class Perceptron(LinearModel):
    def update_weight(self, x_i, y_i, **kwargs):
        """
        x_i (n_features): a single training example
        y_i (scalar): the gold label for that example
        other arguments are ignored
        """
        # Q3.1a
        prediction = self.predict(x_i)

        if(prediction != y_i):
            for i in range(x_i.shape[0]):
                self.W[y_i, i] += x_i[i]
                self.W[prediction, i] -= x_i[i]


class LogisticRegression(LinearModel):
    def update_weight(self, x_i, y_i, learning_rate=0.001):
        """
        x_i (n_features): a single training example
        y_i: the gold label for that example
        learning_rate (float): keep it at the default value for your plots
        """
        # Q3.1b
        label_scores = self.W.dot(x_i)[:, None]
        y_one_hot = np.zeros((np.size(self.W, 0), 1))
        y_one_hot[y_i] = 1

        label_probabilities = np.exp(label_scores) / np.sum(np.exp(label_scores))
        self.W += learning_rate * (y_one_hot - label_probabilities) * x_i[None, :]


class MLP(object):
    # Q3.2b. This MLP skeleton code allows the MLP to be used in place of the
    # linear models with no changes to the training loop or evaluation code
    # in main().
    def __init__(self, n_classes, n_features, hidden_size, layers):
        # Initialize an MLP with a single hidden layer.
        units = [n_features] + [hidden_size] * layers + [n_classes]
        self.W1 = np.random.normal(0.1, 0.1) * np.ones((units[1], units[0]))
        self.b1 = np.zeros(units[1])
        self.W2 = np.random.normal(0.1, 0.1) * np.ones((units[2], units[1]))
        self.b2 = np.zeros(units[2])

        self.weights = [self.W1, self.W2]
        self.biases = [self.b1, self.b2]

    def predict(self, X):
        # Compute the forward pass of the network. At prediction time, there is
        # no need to save the values of hidden nodes, whereas this is required
        # at training time.

        predicted_labels = []
        for x in X:
            output, _ = self.forward(x)
            y_hat = self.predict_label(output)
            predicted_labels.append(y_hat)
        predicted_labels = np.array(predicted_labels)
        return predicted_labels

    def predict_label(self, output):
        # The most probable label is also the label with the largest logit.
        # y_hat = np.zeros_like(output)
        return np.argmax(output)

    def evaluate(self, X, y):
        """
        X (n_examples x n_features)
        y (n_examples): gold labels
        """
        # Identical to LinearModel.evaluate()
        y_hat = self.predict(X)
        print(y_hat)
        print(y)
        n_correct = (y == y_hat).sum()
        n_possible = y.shape[0]
        print(n_correct / n_possible)
        return n_correct / n_possible

    def train_epoch(self, X, y, learning_rate=0.001):
        for x_i, y_i in zip(X, y):
            output, hiddens = self.forward(x_i)
            grad_weights, grad_biases = self.backward(x_i, y_i, output, hiddens)
            self.update_parameters(grad_weights, grad_biases, learning_rate)

    def update_parameters(self, grad_weights, grad_biases, learning_rate):
        num_layers = len(self.weights)
        for i in range(num_layers):
            self.weights[i] -= learning_rate*grad_weights[i]
            self.biases[i] -= learning_rate*grad_biases[i]

    def forward(self, x):
        num_layers = len(self.weights)
        g = lambda x: np.maximum(x, 0)
        hiddens = []
        for i in range(num_layers):
            h = x if i == 0 else hiddens[i-1]
            z = self.weights[i].dot(h) + self.biases[i]
            if i < num_layers-1:  # Assume the output layer has no activation.
                hiddens.append(g(z))
        output = z
        # For classification this is a vector of logits (label scores).
        # For regression this is a vector of predictions.
        return output, hiddens

    def backward(self, x, y, output, hiddens):
        num_layers = len(self.weights)

        # softmax transformation.
        probs = self.compute_label_probabilities(output)
        grad_z = probs - y  # Grad of loss wrt last z.
        grad_weights = []
        grad_biases = []
        for i in range(num_layers-1, -1, -1):
            # Gradient of hidden parameters.
            h = x if i == 0 else hiddens[i-1]
            grad_weights.append(grad_z[:, None].dot(h[:, None].T))
            grad_biases.append(grad_z)

            # Gradient of hidden layer below.
            grad_h = self.weights[i].T.dot(grad_z)

            # Gradient of hidden layer below before activation.
            grad_z = grad_h * (1-h**2)   # Grad of loss wrt z3.

        grad_weights.reverse()
        grad_biases.reverse()
        return grad_weights, grad_biases

    def compute_label_probabilities(self, output):
        # softmax transformation.
        output -= output.max()
        probs = np.exp(output) / np.sum(np.exp(output))
        return probs


def plot(epochs, valid_accs, test_accs):
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.xticks(epochs)
    plt.plot(epochs, valid_accs, label='validation')
    plt.plot(epochs, test_accs, label='test')
    plt.legend()
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model',
                        choices=['perceptron', 'logistic_regression', 'mlp'],
                        help="Which model should the script run?")
    parser.add_argument('-epochs', default=20, type=int,
                        help="""Number of epochs to train for. You should not
                        need to change this value for your plots.""")
    parser.add_argument('-hidden_size', type=int, default=200,
                        help="""Number of units in hidden layers (needed only
                        for MLP, not perceptron or logistic regression)""")
    parser.add_argument('-layers', type=int, default=1,
                        help="""Number of hidden layers (needed only for MLP,
                        not perceptron or logistic regression)""")
    parser.add_argument('-learning_rate', type=float, default=0.001,
                        help="""Learning rate for parameter updates (needed for
                        logistic regression and MLP, but not perceptron)""")
    opt = parser.parse_args()

    utils.configure_seed(seed=42)

    add_bias = opt.model != "mlp"
    data = utils.load_classification_data(bias=add_bias)
    train_X, train_y = data["train"]
    dev_X, dev_y = data["dev"]
    test_X, test_y = data["test"]

    n_classes = np.unique(train_y).size  # 10
    n_feats = train_X.shape[1]

    # initialize the model
    if opt.model == 'perceptron':
        model = Perceptron(n_classes, n_feats)
    elif opt.model == 'logistic_regression':
        model = LogisticRegression(n_classes, n_feats)
    else:
        model = MLP(n_classes, n_feats, opt.hidden_size, opt.layers)
    epochs = np.arange(1, opt.epochs + 1)
    valid_accs = []
    test_accs = []
    for i in epochs:
        print('Training epoch {}'.format(i))
        train_order = np.random.permutation(train_X.shape[0])
        train_X = train_X[train_order]
        train_y = train_y[train_order]
        model.train_epoch(
            train_X,
            train_y,
            learning_rate=opt.learning_rate
        )
        valid_accs.append(model.evaluate(dev_X, dev_y))
        test_accs.append(model.evaluate(test_X, test_y))
        print(valid_accs[-1], test_accs[-1])

    # plot
    plot(epochs, valid_accs, test_accs)


if __name__ == '__main__':
    main()
