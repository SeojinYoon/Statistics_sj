from sklearn.datasets import load_boston
import mglearn

boston = load_boston()
# origin data
print("데이터의 형태: {}".format(boston.data.shape))

# feature engineering data
X, y = mglearn.datasets.load_extended_boston()
print("X.shape: {}".format(X.shape))
