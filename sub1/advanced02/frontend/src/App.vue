<template>
  <v-app>
    <div class="main-title">
      <p data-aos="fade-down" data-aos-duration="1500" data-aos-once="true">심화과제2.데이터 시각화 심화</p>
      <p data-aos="fade-down" data-aos-duration="1500" data-aos-once="true">
        (vue를 이용한 chart.js 라이브러리 실습 과제) <span class="show-outputs" @click.stop="showOutputs = true">(특화 Sub_PJT-Ⅰ 모든 산출물 보기)</span>
      </p>
    </div>
    <div class="select-section">
      <div data-aos="fade-down" data-aos-duration="1500" data-aos-delay="800" data-aos-once="true">
        <v-col class="d-inline-block mr-2" cols="6">
          <v-select
            v-model="selectedData"
            :items="items"
            solo
            label="Choose a Chart Data(Click Me!)"
            :style="{ fontFamily: 'Gothic A1' }"></v-select>
        </v-col>
        <v-col class="d-inline" cols="2">
          <v-btn @click="getChart(selectedData)" :style="{ fontFamily: 'Gothic A1' }" color="#B0BEC5" :disabled="selectedData === undefined">차트 보기</v-btn>
        </v-col>
      </div>
    </div>
    <hr>
    <div class="chart-section" data-aos="fade-up" data-aos-duration="1500" data-aos-delay="1600" data-aos-once="true">
      <transition name="fade" mode="out-in" v-if="showChartSection === 0">
        <SelectAlert></SelectAlert>
      </transition>
      <transition name="fade" mode="out-in" v-else-if="showChartSection === 1">
        <ReviewCountChart></ReviewCountChart>
      </transition>
      <transition name="fade" mode="out-in" v-else-if="showChartSection === 2">
        <RegionalRateChart></RegionalRateChart>
      </transition>
      <transition name="fade" mode="out-in" v-else-if="showChartSection === 3">
        <ReviewAvgDistributionChart></ReviewAvgDistributionChart>
      </transition>
    </div>
    <v-dialog v-model="showOutputs" width="900" persistent>
      <v-card>
        <v-card-title :style="{ fontFamily: 'Nanum Pen Script', fontSize: '24px', fontWeight: 600 }">
          빅데이터 Sub_PJT-Ⅰ 전체 산출물
          </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pb-3" :style="{ fontFamily: 'Noto Sans KR', fontSize: '15px' }">
          <div class="outputs-wrapper">
            <div class="task-title">✔ 기본(공통) 과제</div>
            <div class="outputs">
              <div class="outputs-title">1. 음식점 리뷰 수 분포</div>
              <div class="outputs-contents">
                <img src="./assets/images/req3-1.png" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title">2. 평균 평점 분포 - 파이 차트</div>
              <div class="outputs-contents">
                <img src="./assets/images/req3-2.png" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title">3. 유저 리뷰 수 분포 - 히스토그램</div>
              <div class="outputs-contents">
                <img src="./assets/images/req3-3.png" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title">4. 유저 나이대, 성별 분포(1)(모든 나이 계산) - 이중 막대 그래프</div>
              <div class="outputs-contents">
                <img src="./assets/images/req3-4(2).png" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title">4. 유저 나이대, 성별 분포(2)(10년 단위로 구분) - 이중 막대 그래프</div>
              <div class="outputs-contents">
                <img src="./assets/images/req3-4(1).png" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title">5. 음식점 위치 분포(리뷰 개수가 5개 이상 등록된 대전광역시의 음식점 위치 분포)</div>
              <div class="outputs-contents">
                <img src="https://user-images.githubusercontent.com/52685250/77530639-05a4d780-6ed5-11ea-9d62-018217a6f637.JPG" id="img-tag">
              </div>
            </div>
            <div class="task-title mt-5">✔ 심화 과제</div>
            <div class="outputs">
              <div class="outputs-title">1. 데이터 분석 심화(서울 초밥 음식점들 중 리뷰가 3.5점 이상인 음식점들의 위치 분포)</div>
              <div class="outputs-contents">
                <img src="https://user-images.githubusercontent.com/52685250/77532460-3f2b1200-6ed8-11ea-9fb8-aa4060c0f195.JPG" id="img-tag">
              </div>
            </div>
            <div class="outputs">
              <div class="outputs-title mt-4">2. 데이터 시각화 심화</div>
              <div class="outputs-contents">
                <img src="https://user-images.githubusercontent.com/52685250/77713913-12cbde80-701b-11ea-8b0a-e8238d6298d8.JPG" id="img-tag">
                <img src="https://user-images.githubusercontent.com/52685250/77605564-9cff3e80-6f58-11ea-933a-d47606e79999.JPG" id="img-tag">
                <img src="https://user-images.githubusercontent.com/52685250/77709512-a77c0f80-700e-11ea-9df7-fd570cb8f353.JPG" id="img-tag">
              </div>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn @click.stop="showOutputs = false" small color="warning" :style="{ fontFamily: 'Gothic A1'}">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </v-app>
</template>

<script>
import SelectAlert from '@/components/Common/SelectAlert'
import ReviewCountChart from '@/components/ReviewCount/ReviewCountChart'
import RegionalRateChart from '@/components/RegionalBestStoreRate/RegionalRateChart'
import ReviewAvgDistributionChart from '@/components/ReviewAverage/ReviewAvgDistributionChart'

export default {
  name: 'App',
  components: {
    SelectAlert,
    ReviewCountChart,
    RegionalRateChart,
    ReviewAvgDistributionChart
  },
  data() {
    return {
      selectedData: this.selectedData,
      showChartSection: 0,
      showOutputs: false,
      items: ['1.리뷰 개수가 20개 이상 작성된 음식점 중 BEST 6', '2.지역별 평균 평점 3.5점 이상인 음식점 비율 분포', '3.음식점들의 평균 평점 분포']
    }
  },
  methods: {
    getChart(val) {
      this.showChartSection = Number(val.split('.')[0])
    }
  }
}
</script>

<style scoped>
  * {
    margin: 0;
    padding: 0;
  }

  .main-title {
    font-family: 'Noto Sans KR';
    padding-top: 10px;
    text-align: center;
    background-color: #EFEFEF;
  }

  .main-title > p:first-child {
    font-size: 1.8em;
    font-weight: bold;
    margin-bottom: 7px;
  }

  .main-title > p:last-child {
    font-size: 0.9em;
    color: darkslategrey;
  }

  .show-outputs {
    font-weight: bold;
    color: darkblue;
  }

  .show-outputs:hover {
    cursor: pointer;
  }

  .outputs-wrapper {
    margin: 10px 0;
  }

  .task-title {
    font-size: 19px;
    font-weight: 600;
    font-family: 'Nanum Gothic';
    padding-bottom: 10px;
  }

  .outputs-title {
    font-size: 17px;
    font-weight: 500;
    font-family: 'Noto Sans KR';
    margin-bottom: 6px;
  }

  #img-tag {
    max-width: 100%;
    height: auto;
  }

  .select-section {
    text-align: center;
    height: 80px;
    line-height: 80px;
    background-color: #EFEFEF;
  }

  .chart-section {
    width: 90%;
    margin: 0 auto;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .2s;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>