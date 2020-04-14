from parse import load_dataframes
import pandas as pd
import shutil


def sort_stores_by_score(dataframes, n=20, min_reviews=30):
    """
    Req. 1-2-1 각 음식점의 평균 평점을 계산하여 높은 평점의 음식점 순으로 `n`개의 음식점을 정렬하여 리턴합니다
    Req. 1-2-2 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    """

    df = dataframes["stores"]  # Req. 1-2-2
    new_stores_dataframes = df[(df["review_cnt"] >= 30)]  # Req. 1-2-2
    stores_reviews = pd.merge(
        new_stores_dataframes, dataframes["reviews"], left_on="id", right_on="store"
    )
    scores_group = stores_reviews.groupby(["store", "store_name"])
    scores = scores_group.mean()
    return scores.sort_values(by=["score"], ascending=False).iloc[:n]  # Req. 1-2-1


def get_most_reviewed_stores(dataframes, n=20):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """
    data = dataframes["stores"].sort_values(by=["review_cnt"], ascending=False).iloc[:n]
    return data


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """
    reviews_users = pd.merge(
        dataframes["reviews"], dataframes["users"], left_on="user", right_on="id", right_index=True
    )
    users_group = reviews_users.groupby(["user"])
    users = users_group.count()
    users['gender'] = dataframes["users"]["gender"]
    users['age'] = dataframes["users"]["age"]
    return users.sort_values(by=["store"], ascending=False).iloc[:n]


def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    stores_most_scored = sort_stores_by_score(data)
    stores_most_reviewed = get_most_reviewed_stores(data)
    users_most_written = get_most_active_users(data)

    print("[최고 평점 음식점]")
    print(f"{separater}\n")
    rank_idx = 1  # Req. 1-2-1
    for store in stores_most_scored.iterrows():
        print(
            "{rank}위: {store}({score}점) | (리뷰 개수 : {review_cnt}개)".format(
                rank=rank_idx, store=store[0][1], score=store[1].score, review_cnt=store[1]['review_cnt']  # Req. 1-2-1 + Req. 1-2-2
            )
        )
        rank_idx += 1  # Req. 1-2-1
    print(f"\n{separater}\n\n")

    # Req. 1-2-3
    print("[리뷰 개수 기준 음식점 정렬]")
    print(f"{separater}\n")
    rank_idx = 1
    for store in stores_most_reviewed.iterrows():
        print(
            "{rank}위: {store_name}({review_cnt}개)".format(
                rank=rank_idx, store_name=store[1]["store_name"], review_cnt=store[1]["review_cnt"]
            )
        )
        rank_idx += 1
    print(f"\n{separater}\n\n")

    # Req. 1-2-4
    print("[리뷰 개수 기준 유저 정렬]")
    print(f"{separater}\n")

    rank_idx = 1
    for user in users_most_written.iterrows():
        print(
            "{rank}위: {user_name}({review_cnt}개) - (상세정보 : {gender} / {age}년생)".format(
                rank=rank_idx, user_name=user[0], review_cnt=user[1]["store"], gender=user[1]["gender"], age=user[1]["age"]
            )
        )
        rank_idx += 1
    print(f"\n{separater}\n\n")

if __name__ == "__main__":
    main()
