from parse import load_dataframes
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import webbrowser


# 3.5점 이상인 데이터들을 평균 평점을 기준으로 내림차순 정렬
def get_analyzed_data(dataframes):
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


def show_map(analyzed_stores_data):
    """
    심화 과제1. 데이터 분석 심화
    (선정 주제 : 리뷰가 5개 이상 등록된 서울 초밥 음식점들 중 리뷰가 3.5점 이상인 음식점들의 위치 분포 나타내기)
    """

    seoul_init_points = [37.5655285, 126.8884828]
    seoul_init_zoom = 12

    m = folium.Map(
        location = seoul_init_points,
        zoom_start = seoul_init_zoom
    )

    marker_cluster = MarkerCluster().add_to(m)
    for data in analyzed_stores_data.iterrows():
        store_info = {
            'name': data[1]["store_name"],
            'address': data[1]["address"],
            'tel': data[1]["tel"],
            'latitude': data[1]["latitude"],
            'longitude': data[1]["longitude"],
            'review_cnt': data[1]["review_cnt"],
            'review_mean_score': round(data[1]["mean"], 2)
        }

        address_gu = store_info["address"].split(' ')[1]
        address_dong = store_info["address"].split(' ')[2]
        html_text = f"""<h4><strong>{store_info["name"]}</strong>({store_info["review_mean_score"]}점)</h4><hr style="margin-top: 10px; margin-bottom: 15px;">
                    <table border="1" style="font-size: 14px; width: 100%;">
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
                                <td><center>주소</center></td>
                                <td><center>{store_info["address"]}</center></td>
                            </tr>
                            <tr>
                                <td><center>리뷰개수</center></td>
                                <td><center>{store_info["review_cnt"]}개</center></td>
                            </tr>
                        </tbody>
                    </table>
                    <div style="margin-top: 5px;">
                        <a href="https://search.naver.com/search.naver?query=서울+{address_gu}+{address_dong}+{store_info["name"]}" target="_blank" style="color: green;">네이버 검색 결과로 바로 이동</a>
                    </div>
                    <div>
                        <a href="https://www.google.com/search?q=서울+{address_gu}+{address_dong}+{store_info["name"]}" target="_blank">구글 검색 결과로 바로 이동</a>
                    </div>"""
        html_property = folium.Html(html_text, script=True)

        folium.Marker(
            location = [store_info["latitude"], store_info["longitude"]],
            popup = folium.Popup(html_property, parse_html=True, max_width=400),
            icon=folium.Icon(color='red', icon='ok')
        ).add_to(marker_cluster)
    
    file_name = '심화과제1_리뷰_5개_이상_3.5점_이상인_서울_초밥_음식점_위치분포.html'
    m.save(file_name)
    webbrowser.open_new(file_name)


def main():
    # 파싱한 데이터 가져오기
    data = load_dataframes()

    # analyze.py에 작성된 코드를 이 파일에서 한 번더 실행함으로써 분석된 데이터 가져오기
    get_data = get_analyzed_data(data)

    # 얻은 데이터를 통해 지도에 보여주기
    show_map(get_data)
    

if __name__ == "__main__":
    main()
