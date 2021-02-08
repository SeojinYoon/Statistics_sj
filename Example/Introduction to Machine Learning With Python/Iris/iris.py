
#-0 데이터 적재
from sklearn.datasets import load_iris
iris_dataset = load_iris() # Bunch class

#-1 데이터의 형태가 어떤 것인지 분석
print("iris_dataset의 키: \n{}".format(iris_dataset.keys()))
print("타깃의 이름: {}".format(iris_dataset["target_names"]))
print("특성의 이름: {}".format(iris_dataset["feature_names"]))
print("data의 타입: {}".format(type(iris_dataset["data"])))
print("data의 크기: {}".format(iris_dataset["data"].shape))
print("data의 처음 다섯 행:\n {}".format(iris_dataset["data"][:5]))
print("target의 타입: {}".format(type(iris_dataset["target"])))
print("target의 크기: {}".format(iris_dataset["target"].shape))

#-2 성과 측정: 훈련 데이터와 테스트 데이터
from sklearn.model_selection import  train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset["data"], iris_dataset["target"], random_state=0) # 75% - training, 25% test

print("X_train 크기: {}".format(X_train.shape))
print("Y_train 크기: {}".format(y_train.shape))

print("X_test 크기: {}".format(X_test.shape))
print("y_test 크기: {}".format(y_test.shape))

#-3 데이터 살펴보기
import pandas as pd
import mglearn
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(8,8), marker="o", hist_kwds={"bins":20}, s=60, alpha=.8, cmap=mglearn.cm3)
# check scatter_matrix

#-4 알고리즘 적용
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

#-5 예측하기
import numpy as np
X_new = np.array([[5, 2.9, 1, 0.2]])
print("X_new.shape: {}".format(X_new.shape))

prediction = knn.predict(X_new)
print("예측: {}".format(prediction))
print("예측한 타깃의 이름: {}".format(iris_dataset["target_names"][prediction]))

#-6 평가하기
y_pred = knn.predict(X_test)
print("테스트 세트에 대한 예측값:\n {}".format(y_pred))
print("테스트 세트의 정확도: {:.2f}".format(np.mean(y_pred == y_test)))


