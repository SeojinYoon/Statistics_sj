from  sklearn.datasets import load_breast_cancer
import numpy as np

cancer = load_breast_cancer()
print("cancer.keys(): \n{}".format(cancer.keys()))

print("유방암 데이터의 형태: {}".format(cancer.data.shape))
print("클래스별 샘플 개수: \n{}".format({n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
print("특성 이름:\n{}".format(cancer.feature_names))

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import  train_test_split

np.bincount(cancer.target) # cancer.target[cancer.target==0].shape

print('data =>',cancer.data.shape)
print('target =>',cancer.target.shape)

malignant = cancer.data[cancer.target==0]
benign = cancer.data[cancer.target==1]

print('malignant(악성) =>',malignant.shape)
print('benign(양성) =>',benign.shape)

_, bins=np.histogram(cancer.data[:,0], bins=20)
np.histogram(cancer.data[:,0], bins=20)

import matplotlib.pylab as plt
plt.hist(malignant[:,0],bins=bins, alpha=0.3)
plt.hist(benign[:,0], bins=bins ,alpha=0.3)
plt.title(cancer.feature_names[0])

"""
Performance evaluation
"""
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(cancer.data,
                                                    cancer.target,
                                                    stratify=cancer.target,
                                                    random_state=66)
training_accuracy = []
test_accuracy = []
neighbors_settings = range(1, 11)

from sklearn.neighbors import KNeighborsClassifier
import mglearn
for n_neighbors in neighbors_settings:
    clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X,y)
    clf.fit(X_train, y_train)

    # 훈련 데이터 정확도 저장
    training_accuracy.append(clf.score(X_train, y_train))

    # 일반화 정확도 저장
    test_accuracy.append(clf.score(X_test, y_test))

plt.plot(neighbors_settings, training_accuracy, label="훈련 정확도")
plt.plot(neighbors_settings, test_accuracy, label="테스트 정확도")
plt.ylabel("정확도")
plt.xlabel("n_neighbors")
plt.legend()
