
"""
Configuration
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pylab as plt

pd.set_option("display.width", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)

"""
Load Data
"""
home_dir = os.getcwd()
data_dir = os.path.join(home_dir, "Company_test", "Data")

d_concept_path = os.path.join(data_dir, "concept.csv")
d_condition_occur_path = os.path.join(data_dir, "condition_occurrence.csv")
d_drug_exposure_path = os.path.join(data_dir, "drug_exposure.csv")
d_person_path = os.path.join(data_dir, "person.csv")
d_visit_occur_path = os.path.join(data_dir, "visit_occurrence.csv")

d_concept = pd.read_csv(d_concept_path)
d_condition_occur = pd.read_csv(d_condition_occur_path)
d_drug_exposure = pd.read_csv(d_drug_exposure_path)
d_person = pd.read_csv(d_person_path)
d_visit_occur = pd.read_csv(d_visit_occur_path)

"""
기본 전처리

불필요 데이터 제거, NaN이 너무 많은 컬럼 제거
"""
d_condition_occur = d_condition_occur.drop(["condition_start_date",
                        "condition_end_date",
                        "stop_reason",
                        "provider_id",
                        "visit_detail_id",
                        "condition_source_value",
                        "condition_status_source_value"], axis=1)

d_person = d_person.drop(["month_of_birth", # year_of_birth, month_of_birth, day_of_birth, birth_datatime중 year_of_birth만 남김
                          "day_of_birth",
                          "birth_datetime"], axis=1)
d_person = d_person.drop(["location_id",
                          "provider_id",
                          "care_site_id",
                          "person_source_value",
                          "gender_source_value",
                          "race_source_value",
                          "ethnicity_source_value",], axis=1)

d_visit_occur = d_visit_occur.drop(["visit_start_date", "visit_end_date", "provider_id", "care_site_id", "visit_source_value", "discharge_to_source_value", "discharge_to_concept_id", "admitting_source_value", "preceding_visit_occurrence_id"], axis=1)

"""
gender_concept_id
    8507: MALE
    8537: FEMALE
"""

"""
race_concept_id
    
    0: no maching
    8515: Asian
    8516: Black or African American
    8527: White
"""

"""
ethnicity_concept_id
    0: no maching
"""

"""
visit_concept_id
    9201: Inpatient Visit 
    9202: Outpatient Visit
    9203: Emergency Room Visit
"""

"""
30일 이내 재방문 정의

1000명에 대한 방문기록이 데이터에 있음 

30일 이내 재방문을 정의하기 위하여
먼저 방문 데이터를 PersonID로 그룹화한 다음, 방문 기록에 대하여 정렬을 한후,
특정한 row의 visit_end_datetime과 그 다음 row의 visit_start_datetime을 비교하여 30일이 경과했는지를 체크한다.
->  만약 비교할 대상이 없다면(맨 끝의 방문기록의 경우) 음의 값이 나오게 세팅한다.\

또한 다음 방문시 응급실에 방문했는지 파악
"""
def unix_timestamp_ms(x, date_format):
    if pd.isna(x) != True:
        from datetime import datetime

        dt_obj = datetime.strptime(x, date_format)
        millisec = dt_obj.timestamp() * 1000

        return millisec
    else:
        return np.nan

def convert_from_ms( milliseconds ):
	seconds, milliseconds = divmod(milliseconds,1000)
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	seconds = seconds + milliseconds/1000
	return days, hours, minutes, seconds

results = []
is_next_emergencies = []
date_format = "%Y-%m-%d %H:%M:%S"
for key, partial_df in d_visit_occur.groupby("person_id"):
    partial_df.sort_values(by=["visit_start_datetime"])
    compare_df = partial_df.shift(-1)
    end = compare_df["visit_end_datetime"].map(lambda x: unix_timestamp_ms(x, date_format))
    start = partial_df["visit_start_datetime"].map(lambda x: unix_timestamp_ms(x, date_format))
    result = end.subtract(start, fill_value = 0).apply(convert_from_ms).apply(lambda x: x[0])
    results.append(result)

    is_next_emergencies.append(compare_df["visit_concept_id"] == 9203)

re_visits_inner_30 = np.repeat(0, len(d_visit_occur))
for e1, e2 in zip(results, is_next_emergencies):
    for index in e1.index.tolist():
        re_visits_inner_30[index] = (int(e1.get(index)) > 0) and (int(e1.get(index)) <= 30) and (e2.get(index) == True)

concat_revisit_data = pd.concat([d_visit_occur, pd.Series(re_visits_inner_30)], axis=1)
concat_revisit_data = concat_revisit_data.rename(columns={0: 'revisit inner 30'})

"""
condition 시간 정의
"""
end_times = d_condition_occur["condition_end_datetime"].apply(lambda x: unix_timestamp_ms(x, date_format))
start_times = d_condition_occur["condition_start_datetime"].apply(lambda x: unix_timestamp_ms(x, date_format))

results = []
for i in range(0, len(end_times)):
    results.append(end_times[i] - start_times[i])

conditions = pd.Series(results).map(convert_from_ms).apply(lambda x: x[0])
d_condition_occur_revise = pd.concat([d_condition_occur, conditions], axis=1)
d_condition_occur_revise = d_condition_occur_revise.rename(columns={0: 'condition days'})
d_condition_occur_revise = d_condition_occur_revise.drop(columns=["condition_start_datetime", "condition_end_datetime"], axis=1)

"""
visit_hours 정의 (visit_start_datetime ~ visit_end_datetime)
"""
visit_times = (d_visit_occur["visit_end_datetime"].apply(lambda x: unix_timestamp_ms(x, date_format)) - d_visit_occur["visit_start_datetime"].apply(lambda x: unix_timestamp_ms(x, date_format))).apply(convert_from_ms)
visit_minutes = visit_times.apply(lambda x: x[0] * 3600 + x[1] * 60 + x[2])
concat_revisit_data = pd.concat([concat_revisit_data, visit_minutes], axis=1) # visit minutes 추가
concat_revisit_data = concat_revisit_data.drop(columns=["visit_start_datetime", "visit_end_datetime"], axis=1)
concat_revisit_data = concat_revisit_data.rename(columns={0: 'visit minutes'})

"""
여러 처방을 같이 받은 경우를 전처리 해주어야함
몇개의 처방을 같이 받았는지에 대한 데이터 추가
"""
visit_occur_ids_multi_cond = {}
for key, partial_df in d_condition_occur_revise.groupby("visit_occurrence_id"):
    visit_occur_ids_multi_cond[key] = len(partial_df)

results = []
for e in d_condition_occur_revise.iterrows():
    results.append(visit_occur_ids_multi_cond[e[1]["visit_occurrence_id"]])

d_condition_occur_revise = pd.concat([d_condition_occur_revise, pd.Series(results)], axis=1)
d_condition_occur_revise = d_condition_occur_revise.rename(columns={0: 'multiple condition'})

"""
Join Tables (visit, person, condition, drug)
"""
j_person_visit = concat_revisit_data.merge(d_person, on="person_id" , how = "inner")
j_person_visit_condition = d_condition_occur_revise.merge(j_person_visit, on="visit_occurrence_id")
j_person_visit_condition = j_person_visit_condition.drop(columns = ["person_id_y"], axis=1)

"""
Apply Model
"""
datas = j_person_visit_condition
datas = datas.dropna()
datas = datas.drop(columns=["person_id_x", "visit_occurrence_id"])

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

len(datas[datas["revisit inner 30"] == 1]) / len(datas)
X_train, X_test, y_train, y_test = train_test_split(datas.drop(columns=["revisit inner 30"], axis=1), datas["revisit inner 30"], random_state=0) # 75% - training, 25% test

"""
logistic = LogisticRegression(random_state=0)
logistic.fit(X_train, y_train)
print(classification_report(y_test, logistic.predict(X_test)))
"""
from sklearn.metrics import classification_report

depts = []
precisions_0 = []
recalls_0 = []
precisions_1 = []
recalls_1 = []
for d in range(1,40):
    depts.append(d)
    dt_clf = DecisionTreeClassifier(random_state=0, max_depth=d)
    dt_clf.fit(X_train, y_train)

    precision_0 = classification_report(y_test, dt_clf.predict(X_test), output_dict=True)["0"]["precision"]
    recall_0 = classification_report(y_test, dt_clf.predict(X_test), output_dict=True)["0"]["recall"]
    precisions_0.append(precision_0)
    recalls_0.append(recall_0)

    precision_1 = classification_report(y_test, dt_clf.predict(X_test), output_dict=True)["1"]["precision"]
    recall_1 = classification_report(y_test, dt_clf.predict(X_test), output_dict=True)["1"]["recall"]
    precisions_1.append(precision_1)
    recalls_1.append(recall_1)


plt.plot(depts, precisions_1)
plt.plot(depts, recalls_1)
plt.xlabel("depth")
plt.ylabel("metric")
plt.title("About 1")

plt.plot(depts, precisions_0)
plt.plot(depts, recalls_0)
plt.xlabel("depth")
plt.ylabel("metric")
plt.title("About 0")

from sklearn.tree import export_graphviz
dt_clf = DecisionTreeClassifier(random_state=0, max_depth=20)
dt_clf.fit(X_train, y_train)

print(classification_report(y_test, dt_clf.predict(X_test)))

export_graphviz(dt_clf, out_file="dicisionTree1.dot", class_names=["0","1"],
                feature_names=X_train.columns, impurity=False, filled=True)

import pydot
(graph,) = pydot.graph_from_dot_file("dicisionTree1.dot", encoding="utf8")

graph.write_png("dicisionTree1.png")


