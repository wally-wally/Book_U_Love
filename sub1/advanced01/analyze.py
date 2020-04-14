from parse import load_dataframes
import pandas as pd
import shutil


def analyze_data(dataframes):
    df = dataframes["stores"]
    seoul_sushi_stores = df[(df["review_cnt"] >= 5) & (df["address"].str.contains("서울특별시")) & (df["category"].str.contains("초밥"))]

    review_df = dataframes["reviews"]
    groupped_reviews = review_df.groupby(["store"])
    groupped_mean_reviews = groupped_reviews["score"].agg(["mean"])

    seoul_sushi_stores_reviews = pd.merge(
        seoul_sushi_stores, groupped_mean_reviews, left_on="id", right_on="store"
    )

    seoul_sushi_df = seoul_sushi_stores_reviews

    upper_score_stores = seoul_sushi_df[(seoul_sushi_df["mean"] >= 3.5)].sort_values(by=["mean"], ascending=False)

    return upper_score_stores



def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    analyzed_data = analyze_data(data)

    print("[리뷰가 5개 이상 등록된 서울 초밥 음식점들의 평균 평점 분포]")
    print(f"{separater}\n")

    rank_idx = 1
    for data in analyzed_data.iterrows():
        print(f'{rank_idx}위: {data[1]["store_name"]} (주소-{data[1]["address"]} / Tel.{data[1]["tel"]} / {data[1]["review_cnt"]}개 리뷰 / {round(data[1]["mean"], 2)}점)')
        rank_idx += 1
    print(f"\n{separater}\n\n")

if __name__ == "__main__":
    main()
