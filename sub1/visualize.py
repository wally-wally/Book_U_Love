import itertools
from collections import Counter
from parse import load_dataframes
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from folium.plugins import MarkerCluster
from datetime import datetime # 현재 년도를 구하기 위해 import 함
import webbrowser


def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

    sns.set_palette(sns.color_palette("Spectral"))
    plt.rc("xtick", labelsize=6)


def show_store_categories_graph(dataframes, n=100):
    """
    Tutorial: 전체 음식점의 상위 `n`개 카테고리 분포를 그래프로 나타냅니다.
    """

    stores = dataframes["stores"]

    # 모든 카테고리를 1차원 리스트에 저장합니다
    categories = stores.category.apply(lambda c: c.split("|"))
    categories = itertools.chain.from_iterable(categories)

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    categories_count = Counter(list(categories))
    best_categories = categories_count.most_common(n=n)
    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )

    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show()


def show_store_review_distribution_graph(dataframes):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    dataset = dataframes["stores"].sort_values(by=["review_cnt"], ascending=False)
    min_review_cnt, max_review_cnt = dataset.iloc[-1, -1], dataset.iloc[0, -1]
    try:
        show_type = int(input('보고 싶은 형태를 선택해주세요.(숫자 1 또는 2 선택)(1.outlier를 처리한 그래프 / 2. 구간을 나눠서 보는 그래프)'))
        if (show_type == 1):
            review_cnt_distribution = [0 for _ in range(11)] # 리뷰 개수가 1개 ~ 10개까지 각 구간별 음식점 개수를 따로따로 구하고 11개 이상은 하나로 묶어서 처리
            reference_axis = []
            
            for i in range(11):
                if (i <= 9):
                    review_cnt_distribution[i] = len(dataset[(dataset["review_cnt"] == i + 1)])
                    reference_axis.append(f'{i + 1}개')
                else:
                    review_cnt_distribution[i] = len(dataset[(dataset["review_cnt"] >= i + 1)])
                    reference_axis.append(f'{i + 1}개 이상')

            plt.figure()
            plt.title(f'전체 음식점의 리뷰 개수 분포(리뷰 개수 0개 음식점은 제외)')
            plt.bar(reference_axis, review_cnt_distribution, label="리뷰 개수")
            plt.xlabel('개수 범위')
            plt.ylabel('리뷰 개수')
            plt.xticks(reference_axis, fontsize=9)
            plt.legend()
            for k, l in enumerate(review_cnt_distribution):
                str_val = "%d개" % review_cnt_distribution[k]
                plt.text(k, l, str_val, color="#000000", horizontalalignment="center", verticalalignment="bottom")
            plt.show()
        elif (show_type == 2):
            try:
                range_num = int(input('범위를 설정해주세요.(단, 1 이상 10 이하의 숫자만 작성 가능)(ex.5개 => 0~4개 / 5~9개 / ... 와 같이 범위를 지정해서 분포를 집계함'))
                if (range_num >= 1 and range_num <= 10) :
                    range_min_value = divmod(min_review_cnt, range_num)[0]
                    range_max_value = divmod(max_review_cnt, range_num)[0] + 1
                    review_cnt_distribution = [0 for _ in range(range_min_value, range_max_value)]

                    for i in range(range_min_value, range_max_value):
                        review_cnt_distribution[i] = len(dataset[(dataset["review_cnt"] >= range_num * i) & (dataset["review_cnt"] <= range_num * i + range_num + 1)])

                    plt.figure()
                    plt.title(f'전체 음식점의 리뷰 개수 분포(단위 : {range_num}개)')
                    
                    reference_axis = []
                    for j in range(range_min_value, range_max_value):
                        if (j == range_max_value - 1):
                            reference_axis.append(f'{range_num * j}개 이상')
                        else:
                            reference_axis.append(f'{range_num * j}개~{range_num * j + range_num + 1}개')

                    plt.bar(reference_axis, review_cnt_distribution, label="리뷰 개수")
                    plt.xlabel('개수 범위')
                    plt.ylabel('리뷰 개수')
                    plt.xticks(reference_axis)
                    plt.legend()
                    for k, l in enumerate(review_cnt_distribution):
                        str_val = "%d개" % review_cnt_distribution[k]
                        plt.text(k, l, str_val, color="#000000", horizontalalignment="center", verticalalignment="bottom")
                    plt.show()
                else:
                    print('1 이상 10 이하의 숫자가 아닙니다.')
            except ValueError:
                print('숫자로 입력하지 않았습니다.')
        else:
            print('1 또는 2로 입력해야합니다.')
    except ValueError:
        print('숫자로 입력하지 않았습니다.')



def show_store_average_ratings_graph(dataframes):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    entire_store_cnt = len(dataframes["stores"])
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

    no_score_stores_cnt = entire_store_cnt - sum(score_distribution)

    plt.figure()
    plt.title(f'평균 평점 분포(cf.평점 등록/미등록 음식점 개수 : {sum(score_distribution)}개 / {no_score_stores_cnt}개)', fontsize=15)
    plt.pie(score_distribution, labels=references, autopct='%.2f%%', startangle=90, textprops={'fontsize': 11})
    plt.legend(fontsize=9, loc="lower left")
    plt.show()


def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    total_user_cnt = len(dataframes['users'])  # 전체 유저 수
    reviews_users = dataframes["reviews"].groupby('user').count().sort_values(by=["id"], ascending=False)
    written_user_cnt = len(reviews_users)  # 리뷰를 작성한 유저 수
    min_review_cnt, max_review_cnt = reviews_users.iloc[-1, 0], reviews_users.iloc[0, 0]
    
    reviews_cnt_data = [data for data in reviews_users["id"]]
    
    plt.figure()

    # 전체 유저의 리뷰 개수 분포
    plt.suptitle(f'전체 유저의 리뷰 개수 분포(리뷰 작성 유저 수/전체 유저 수 : {written_user_cnt}명/{total_user_cnt}명)', fontsize=15)
    plt.subplot(221)
    plt.title('전체 유저의 리뷰 개수 분포', fontsize=12)
    plt.xlabel('등록 리뷰 개수')
    plt.ylabel('유저 수')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.hist(reviews_cnt_data, range=(min_review_cnt, max_review_cnt), bins=40)

    # 등록 리뷰 개수가 1 ~ 20개인 유저들
    plt.subplot(222)
    plt.title('등록 리뷰 개수가 1 ~ 20개', fontsize=12)
    plt.xlabel('등록 리뷰 개수')
    plt.ylabel('유저 수')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.hist(reviews_cnt_data, range=(min_review_cnt, 20), bins=20, color="green")

    # 등록 리뷰 개수가 21 ~ 100개인 유저들
    plt.subplot(223)
    plt.title('등록 리뷰 개수가 21 ~ 100개', fontsize=12)
    plt.xlabel('등록 리뷰 개수')
    plt.ylabel('유저 수')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.hist(reviews_cnt_data, range=(21, 100), bins=100 - 21 + 1, color="blue")
    
    # 등록 리뷰 개수가 101개 이상인 유저들
    plt.subplot(224)
    plt.title('등록 리뷰 개수가 101개 이상', fontsize=12)
    plt.xlabel('등록 리뷰 개수')
    plt.ylabel('유저 수')
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)
    plt.hist(reviews_cnt_data, range=(101, max_review_cnt), bins=max_review_cnt - 101 + 1, color="gray")

    plt.show()

def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    df = dataframes["users"].sort_values(by=["age"], ascending=False)
    real_data = df[(pd.to_numeric(df["age"], downcast='signed') != 0000) & (pd.to_numeric(df["age"], downcast='signed') <= datetime.today().year)]
    total_user_count, correct_age_user_count = len(dataframes["users"]), len(real_data)  # 전체 유저 수, 올바른 태어난 년도를 작성한 유저 수
    groupped_data = real_data.groupby(["age", "gender"]).size()

    # (2) 10년 단위로 끊어서 보는 남자, 여자 유저 수 분포 그래프
    oldest_age, youngest_age = divmod(int(groupped_data.index[0][0]), 10)[0] * 10, divmod(int(groupped_data.index[-1][0]), 10)[0] * 10
    age_range = divmod(youngest_age - oldest_age, 10)[0] + 1
    year_label = []
    for year_idx in range(oldest_age, youngest_age + 10, 10):
        if year_idx == youngest_age:
            year_label.append(f'{year_idx}년~{datetime.today().year}년')
        else:
            year_label.append(f'{year_idx}년~{year_idx + 9}년')
    man_cnt = [0 for _ in range(age_range)]
    woman_cnt = [0 for _ in range(age_range)]
    x_position = np.arange(len(year_label))

    for i, j in groupped_data.index:
        year, gender, user_count = divmod(int(i), 10)[0] * 10, j, groupped_data.loc[i, j]
        if (gender == '남'):
            man_cnt[divmod(year - oldest_age, 10)[0]] += user_count
        else:
            woman_cnt[divmod(year - oldest_age, 10)[0]] += user_count

    plt.figure()
    plt.title(f'유저 나이대별 성별 분포 구하기(cf.올바르게 나이를 입력한 유저수/전체 유저수 : {correct_age_user_count}명/{total_user_count}명)', fontsize="14")
    man_graph_data = plt.bar(x_position - 0.1, man_cnt, label="남자 유저 수", width=0.2, color="blue")
    woman_graph_data = plt.bar(x_position + 0.1, woman_cnt, label="여자 유저 수", width=0.2, color="red")
    for man_data in man_graph_data:
        man_cnt = man_data.get_height()
        posx = man_data.get_xy()[0] + 0.1
        posy = man_data.get_height()
        plt.text(posx, posy, f'{man_cnt}명', rotation=0, horizontalalignment="center", verticalalignment="bottom")
    for woman_data in woman_graph_data:
        woman_cnt = woman_data.get_height()
        posx = woman_data.get_xy()[0] + 0.1
        posy = woman_data.get_height()
        plt.text(posx, posy, f'{woman_cnt}명', rotation=0, horizontalalignment="center", verticalalignment="bottom")
    plt.legend()
    plt.xticks(x_position, year_label, fontsize=10)
    plt.xlabel('나이대(출생연도별)')
    plt.ylabel('유저 수')
    plt.show()
    
    # (1) 모든 년도의 남자, 여자 유저 수 분포 그래프(daily_eassy의 '0324.md' 파일에 그래프 스크린샷 첨부)
    oldest_age, youngest_age = int(groupped_data.index[0][0]), int(groupped_data.index[-1][0])
    age_range = youngest_age - oldest_age + 1
    man_cnt = [0 for _ in range(age_range)]
    woman_cnt = [0 for _ in range(age_range)]
    year_label = [f'{i}년' for i in range(oldest_age, youngest_age + 1)]
    x_position = np.arange(len(year_label))

    for i, j in groupped_data.index:
        year, gender, user_count = int(i), j, groupped_data.loc[i, j]
        if (gender == '남'):
            man_cnt[year - oldest_age] = user_count
        else:
            woman_cnt[year - oldest_age] = user_count
    
    plt.figure()
    plt.title(f'유저 나이대별 성별 분포 구하기 - 초기 버전(cf.올바르게 나이를 입력한 유저수/전체 유저수 : {correct_age_user_count}명/{total_user_count}명)', fontsize="14")
    plt.bar(x_position - 0.0, man_cnt, label="남자 유저 수", width=0.2, color="blue")
    plt.bar(x_position + 0.2, woman_cnt, label="여자 유저 수", width=0.2, color="red")
    plt.legend()
    plt.xticks(x_position, year_label, rotation=45)
    plt.xlabel('나이(출생연도)')
    plt.ylabel('유저 수')
    plt.show()


def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    df = dataframes["stores"]
    new_filtering_df = df[(df["review_cnt"] >= 5) & (df["address"].str.contains('대전광역시'))] 
    
    daejeon_init_points = [36.3650325, 127.3475783]
    daejeon_init_zoom = 11.75

    m = folium.Map(
        location = daejeon_init_points,
        zoom_start = daejeon_init_zoom
    )

    marker_cluster = MarkerCluster().add_to(m)
    for data in new_filtering_df.iterrows():
        store_info = {
            'name': data[1]["store_name"],
            'address': data[1]["address"],
            'tel': data[1]["tel"],
            'latitude': data[1]["latitude"],
            'longitude': data[1]["longitude"],
            'category': data[1]["category"],
            'review_cnt': data[1]["review_cnt"]
        }

        address_dong = store_info["address"].split(' ')[2]
        html_text = f"""<h4><strong>{store_info["name"]}</strong>({store_info["category"]})</h4>
                    <table border="1" style="font-size: 14.5px; width: 90%;">
                        <thead>
                            <tr>
                                <td><b><center>분류</center></b></td>
                                <td><b><center>내용</center></b></td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><center>전화번호</center></td>
                                <td><center>{store_info["tel"]}</center></td>
                            </tr>
                            <tr>
                                <td><center>리뷰개수</center></td>
                                <td><center>{store_info["review_cnt"]}개</center></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <a href="https://search.naver.com/search.naver?query=대전+{address_dong}+{store_info["name"]}" target="_blank">네이버 검색 결과로 바로 이동</a>"""
        html_property = folium.Html(html_text, script=True)

        folium.Marker(
            location = [store_info["latitude"], store_info["longitude"]],
            popup = folium.Popup(html_property, parse_html=True, max_width=400),
            icon=folium.Icon(color='red', icon='ok')
        ).add_to(marker_cluster)
    
    file_name = '1-3-5_음식점_분포(리뷰개수_5개이상인_대전음식점).html'
    m.save(file_name)
    webbrowser.open_new(file_name)


def main():
    set_config()
    data = load_dataframes()
    # Tutorial
    # show_store_categories_graph(data)

    # Req. 1-3-1
    show_store_review_distribution_graph(data)

    # Req. 1-3-2
    show_store_average_ratings_graph(data)

    # Req. 1-3-3
    show_user_review_distribution_graph(data)

    # Req. 1-3-4
    show_user_age_gender_distribution_graph(data)

    # Req. 1-3-5
    show_stores_distribution_graph(data)

if __name__ == "__main__":
    main()
