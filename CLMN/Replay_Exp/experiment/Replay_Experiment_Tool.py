
"""
1차 분석 개요

Preprocessing
-> 시퀀스 데이터만 뽑아냄
-> 세션 별로 그룹화

Mapping
-> 시퀀스 데이터와 스텝이 같거나 한 스텝 뒤에 (ISI 혹은 bundle Interval 부분) 에서의 시퀀스 입력을 보고 stimulus와 매핑한다.(여러가지 입력이 들어갈 수 있으니, step 별로 여러 반응이 나올것임)

Measure
-> 자극 이벤트에 매핑되는 응답이벤트에 대하여 첫번째 Multi processing 이벤트가 일어난 응답을 가지고 정확도 및 반응 시간을 측정한다.
-> 정확도는 자극 step에서 어떤 이벤트를 주었느냐와 자극 이벤트에 매핑되는 응답 이벤트에서 어떤 응답을 했는지를 비교한다.
-> 반응 시간은 자극 step에서의 시간과 자극 이벤트에 매핑되는 응답 이벤트에서 어떤 응답을 했는지를 비교한다.

그래프
-> 평균 반응 시간 측정
-> 정확도 ratio 측정
"""

import numpy as np
import pandas as pd

def mapping_data(stimuluses, responses):
    """
    Mapping
    -> 시퀀스 데이터와 스텝이 같거나 한 스텝 뒤에 (ISI 혹은 bundle Interval 부분) 에서의 시퀀스 입력을 보고 stimulus와 매핑한다.(여러가지 입력이 들어갈 수 있으니, step 별로 여러 반응이 나올것임)

    stimuluses: list of stimulus per session
    responses: list of response per session
    """
    mapped_datas = []
    for session_index in range(0, len(stimuluses)):
        target_session_sti = stimuluses[session_index]  # Session 구분
        target_session_sti_seqs = target_session_sti[target_session_sti["Event_Type"] == "seq texts"]

        target_res = responses[session_index]

        mapped_sti_response = pd.DataFrame()
        for row_index in range(0, len(target_session_sti_seqs)): # stimulus의 row마다 response와의 join 연산 수행
            seq_sti = target_session_sti_seqs.iloc[row_index]
            target_step = seq_sti["Step"]

            response_by_step = target_res[np.logical_or(target_res["Step"] == target_step, target_res[
                "Step"] == target_step + 1)]  # mapping step 다음 까지 생각하는 이유는 대기 중일떄 입력이 들어올수 있기 때문이다.

            mapping_by_step = response_by_step.merge(pd.DataFrame(seq_sti).T, left_on="Step", right_on="Step")
            mapping_by_step.columns = ["Step", "Response", "response_seconds", "Event_Type", "Stimulus", "display_seconds",
                                       "stimulus_start_seconds"]
            mapped_sti_response = mapped_sti_response.append(mapping_by_step)
        mapped_datas.append(mapped_sti_response)
    return mapped_datas

def multi_response_only(mapped_datas):
    # Multi response 데이터만 남겨둠
    for session_index in range(0, len(mapped_datas)):
        mapped_datas[session_index] = mapped_datas[session_index][mapped_datas[session_index]["Response"].apply(lambda x: len(x)) > 1]
    return mapped_datas

def time_difference(mapped_datas):
    # Time Difference 계산(반응 - 자극)
    for session_index in range(0, len(mapped_datas)):
        time_difference = mapped_datas[session_index]["response_seconds"] - mapped_datas[session_index]["stimulus_start_seconds"]
        mapped_datas[session_index]["Time Difference"] = time_difference
    return mapped_datas

def avg_time_difference_per_sessions(mapped_datas):
    # Average Time Difference Per session
    averages = []
    for session_index in range(0, len(mapped_datas)):
        averages.append(np.average(mapped_datas[session_index]["Time Difference"]))
    return averages

def accuracy(mapped_datas):
    accuracies_ratio = []
    for session_index in range(0, len(mapped_datas)):
        accuracy_freq = len(mapped_datas[session_index][mapped_datas[session_index]["Stimulus"] == mapped_datas[session_index]["Response"]])
        print(accuracy_freq)
        accuracies_ratio.append(accuracy_freq / len(mapped_datas[session_index]))
    return accuracies_ratio

"""
2차 분석 개요
Preprcessing
-> 전체 데이터를 합침
-> 시퀀스 데이터만 뽑아냄
-> 세션 별로 그룹화

그래프
-> 평균 반응 시간 측정
-> 정확도 ration 측정
"""