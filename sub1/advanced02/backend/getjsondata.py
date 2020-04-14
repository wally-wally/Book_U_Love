import json
import pandas as pd
import os
import shutil
from datetime import datetime # 현재 년도를 구하기 위해 import 함

def get_parsing_data() :
    DATA_DIR = "../../../data"
    DATA_FILE = os.path.join(DATA_DIR, "data.json")
    DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

    # 각 DataFrame의 column명 지정
    store_columns = (
        "id",  # 음식점 고유번호
        "store_name",  # 음식점 이름
        "branch",  # 음식점 지점 여부
        "area",  # 음식점 위치
        "tel",  # 음식점 번호
        "address",  # 음식점 주소
        "latitude",  # 음식점 위도
        "longitude",  # 음식점 경도
        "category",  # 음식점 카테고리
        "review_cnt"  # req2-2를 수행하기 위해 리뷰 개수 컬럼 추가
    )

    menu_columns = (
        "id",  # 메뉴 고유번호
        "store",  # 해당 메뉴를 판매하는 가게이름(store 테이블에서 정의한 음식점 고유번호)
        "menu_name",  # 해당 메뉴 이름,
        "price"  # 해당 메뉴 가격
    )

    review_columns = (
        "id",  # 리뷰 고유번호
        "store",  # 음식점 고유번호(store 테이블에서 정의한 음식점 고유번호)
        "user",  # 유저 고유번호
        "score",  # 평점
        "content",  # 리뷰 내용
        "reg_time",  # 리뷰 등록 시간
    )

    user_columns = (
        "id",  # 작성자 고유번호
        "gender",  # 성별
        "age"  # 나이(출생년도)
    )


    def import_data(data_path=DATA_FILE):
        """
        Req. 1-1-1 음식점 데이터 파일을 읽어서 Pandas DataFrame 형태로 저장합니다
        """

        try:
            with open(data_path, encoding="utf-8") as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            print(f"`{data_path}` 가 존재하지 않습니다.")
            exit(1)

        stores = []  # 음식점 테이블
        reviews = []  # 리뷰 테이블
        menus = [] # 메뉴 테이블
        users = [] # 유저 테이블

        menu_id = 1
        for d in data:

            categories = [c["category"] for c in d["category_list"]]

            # 음식점 데이터 전처리 과정
            stores.append(
                [
                    d["id"],
                    d["name"],
                    d["branch"],
                    d["area"],
                    d["tel"],
                    d["address"],
                    d["latitude"],
                    d["longitude"],
                    "|".join(categories),
                    d["review_cnt"]
                ]
            )

            # 메뉴 데이터 전처리 과정
            for menu in d["menu_list"]:
                menu_name = menu["menu"]
                price = menu["price"]

                menus.append(
                    [menu_id, d["id"], menu_name, price]
                )
                menu_id += 1

            # 리뷰 데이터 전처리 과정
            for review in d["review_list"]:
                r = review["review_info"]
                u = review["writer_info"]

                reviews.append(
                    [r["id"], d["id"], u["id"], r["score"], r["content"], r["reg_time"]]
                )

                # 유저 데이터 전처리 과정
                users.append(
                    [u["id"], u["gender"], u["born_year"]]
                )

        # pandas의 dataframe 형태로 저장
        store_frame = pd.DataFrame(data=stores, columns=store_columns)
        menu_frame = pd.DataFrame(data=menus, columns=menu_columns)
        review_frame = pd.DataFrame(data=reviews, columns=review_columns)
        user_frame = pd.DataFrame(data=users, columns=user_columns)

        return {
            "stores": store_frame,
            "menus": menu_frame,
            "reviews": review_frame,
            "users": user_frame
        }


    def dump_dataframes(dataframes):
        pd.to_pickle(dataframes, DUMP_FILE)


    def load_dataframes():
        return pd.read_pickle(DUMP_FILE)

    print("[*] Parsing data...")
    data = import_data()
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print("[+] Done\n")

    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    print("[음식점]")
    print(f"{separater}\n")
    print(data["stores"].head())
    print(f"\n{separater}\n\n")

    print("[메뉴]")
    print(f"{separater}\n")
    print(data["menus"].head())
    print(f"\n{separater}\n\n")

    print("[리뷰]")
    print(f"{separater}\n")
    print(data["reviews"].head())
    print(f"\n{separater}\n\n")

    print("[유저]")
    print(f"{separater}\n")
    print(data["users"].head())
    print(f"\n{separater}\n\n")

    return data


def analyze_data_1(dataframes):
    df = dataframes["stores"]
    over_twenty_reviews_stores = df[(df["review_cnt"] >= 20)]
    review_df = dataframes["reviews"]
    groupped_reviews = review_df.groupby(["store"])
    groupped_mean_reviews = groupped_reviews["score"].agg(["mean"])

    merged_data = pd.merge(over_twenty_reviews_stores, groupped_mean_reviews, left_on="id", right_on="store")
    return merged_data.sort_values(by=["mean"], ascending=False)


def analyze_data_2(dataframes):
    df = dataframes["stores"]
    review_df = dataframes["reviews"]
    groupped_reviews = review_df.groupby(["store"])
    groupped_mean_reviews = groupped_reviews["score"].agg(["mean"])
    merged_df = pd.merge(df, groupped_mean_reviews, left_on="id", right_on="store")

    # 서울 음식점 데이터
    seoul_store_count = len(df[(df["review_cnt"] >= 0) & (df["address"].str.contains('서울특별시'))])  # 서울 음식점 수
    seoul_filtering_store_count = len(merged_df[(merged_df["mean"] >= 3.5) & (merged_df["address"].str.contains('서울특별시'))])  # 서울 음식점 중 평점 3.5 이상인 음식점 수

    # 대전 음식점 데이터
    daejeon_store_count = len(df[(df["review_cnt"] >= 0) & (df["address"].str.contains('대전광역시'))])  # 대전 음식점 수
    daejeon_filtering_store_count = len(merged_df[(merged_df["mean"] >= 3.5) & (merged_df["address"].str.contains('대전광역시'))])  # 대전 음식점 중 평점 3.5 이상인 음식점 수

    # 광주 음식점 데이터
    gwangju_store_count = len(df[(df["review_cnt"] >= 0) & (df["address"].str.contains('광주광역시'))])  # 광주 음식점 수
    gwangju_filtering_store_count = len(merged_df[(merged_df["mean"] >= 3.5) & (merged_df["address"].str.contains('광주광역시'))])  # 광주 음식점 중 평점 3.5 이상인 음식점 수

    # 구미 음식점 데이터
    gumi_store_count = len(df[(df["review_cnt"] >= 0) & (df["address"].str.contains('구미시'))])  # 구미 음식점 수
    gumi_filtering_store_count = len(merged_df[(merged_df["mean"] >= 3.5) & (merged_df["address"].str.contains('구미시'))])  # 구미 음식점 중 평점 3.5 이상인 음식점 수

    counts_data = {
        'seoul': {
            'total_stores_count': seoul_store_count,
            'filtering_stores_count': seoul_filtering_store_count
        },
        'daejeon': {
            'total_stores_count': daejeon_store_count,
            'filtering_stores_count': daejeon_filtering_store_count
        },
        'gwangju': {
            'total_stores_count': gwangju_store_count,
            'filtering_stores_count': gwangju_filtering_store_count
        },
        'gumi': {
            'total_stores_count': gumi_store_count,
            'filtering_stores_count': gumi_filtering_store_count
        },
    }

    return counts_data


def analyze_data_3(dataframes):
    dataset = pd.merge(dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store")
    groupped_dataset = dataset.groupby(["store", "store_name"])
    mean_scores = groupped_dataset.mean().sort_values(by=["score"], ascending=False)
    score_distribution = [0 for _ in range(5)]
    references = []

    for score_idx in range(1, 6):
        score_distribution[score_idx - 1] = len(mean_scores[(mean_scores["score"] >= score_idx) & (mean_scores["score"] < score_idx + 1)])
        if (score_idx == 5):
            references.append('5점')
        else:
            references.append(f'{score_idx}점 이상 {score_idx + 1}점 미만')
    
    mean_stores_data = {}
    mean_stores_data["score_distribution"] = score_distribution
    mean_stores_data["chart_labels"] = references
    return mean_stores_data


def save_json_file(analyzed_data, idx):
    stores_data = []

    if (idx == 1):
        for data in analyzed_data.iterrows():
            store_dict = {}
            store_dict["store_name"] = data[1]["store_name"]
            store_dict["tel"] = data[1]["tel"]
            store_dict["address"] = data[1]["address"]
            store_dict["latitude"] = data[1]["latitude"]
            store_dict["longitude"] = data[1]["longitude"]
            store_dict["category"] = data[1]["category"]
            store_dict["review_cnt"] = data[1]["review_cnt"]
            store_dict["review_mean"] = data[1]["mean"]
            stores_data.append(store_dict)
    else:
        stores_data = analyzed_data

    with open(f'../frontend/src/assets/json/data_0{idx}.json', 'w',  encoding='UTF-8-sig') as f:
        f.write(json.dumps(stores_data, indent=2, ensure_ascii=False))


dataframes = get_parsing_data()

# 1. 리뷰 작성 개수가 20개 이상인 음식점들의 리뷰 평균 평점 데이터
analyzed_data = analyze_data_1(dataframes)

save_json_file(analyzed_data, 1)

# 2. 서울, 대전, 광주, 구미의 각 지역 전체 음식점 수에 대한 평균 평점 3.5점 이상인 음식점 수 비율 분포
analyzed_data = analyze_data_2(dataframes)

save_json_file(analyzed_data, 2)

# 3. req3-2에서 구현한 각 음식점의 평균 평점 분포
analyzed_data = analyze_data_3(dataframes)

save_json_file(analyzed_data, 3)