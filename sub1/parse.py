import json
import pandas as pd
import os
import shutil

DATA_DIR = "../data"
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
                d["review_cnt"],
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


def main():

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


if __name__ == "__main__":
    main()
