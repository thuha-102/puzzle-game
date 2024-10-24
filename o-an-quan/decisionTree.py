import numpy as np

class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.num_classes = len(set(y))
        self.tree = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_samples_per_class = [np.sum(y == i) for i in range(self.num_classes)]
        predicted_class = np.argmax(num_samples_per_class)

        if depth == self.max_depth or self.num_classes == 1 or num_samples_per_class[predicted_class] == num_samples:
            return Node(value=predicted_class)

        best_info_gain = -float('inf')
        best_feature_index = None
        best_threshold = None
        for feature_index in range(num_features):
            thresholds, classes = zip(*sorted(zip(X[:, feature_index], y)))
            num_left = [0] * self.num_classes
            num_right = num_samples_per_class.copy()
            for i in range(1, num_samples):
                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                info_gain_left = self._entropy(num_left, i)
                info_gain_right = self._entropy(num_right, num_samples - i)
                info_gain = self._information_gain(num_samples, info_gain_left, info_gain_right)
                if thresholds[i] == thresholds[i - 1]:
                    continue
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_feature_index = feature_index
                    best_threshold = (thresholds[i] + thresholds[i - 1]) / 2

        left_mask = X[:, best_feature_index] < best_threshold
        X_left, y_left = X[left_mask], y[left_mask]
        X_right, y_right = X[~left_mask], y[~left_mask]

        left = self._grow_tree(X_left, y_left, depth + 1)
        right = self._grow_tree(X_right, y_right, depth + 1)

        return Node(feature_index=best_feature_index, threshold=best_threshold, left=left, right=right)

    def predict(self, X):
        return np.array([self._predict(x, self.tree) for x in X])

    def _predict(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature_index] < node.threshold:
            return self._predict(x, node.left)
        else:
            return self._predict(x, node.right)

    def _entropy(self, counts, total):
        entropy = 0
        for count in counts:
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        return entropy

    def _information_gain(self, total_samples, left_entropy, right_entropy):
        p_left = total_samples / 2
        p_right = total_samples / 2
        total_entropy = (p_left * left_entropy + p_right * right_entropy) / total_samples
        return total_entropy
