<script setup>
import {
  Edit,
  Timer,
  Guide,
  Bicycle,
  Finished
} from '@element-plus/icons-vue'
import { ref, computed, onMounted } from 'vue';
import { ElMessage, ElLoading } from 'element-plus';
import { getDiaryByIdService, updateDiaryService } from '@/api/diary.js';
import { rateDiaryService } from '@/api/diary.js';
import { useRouter } from 'vue-router';
import { usePlanStore } from '@/stores/plan.js';
import { QuillEditor } from '@vueup/vue-quill'
import placeTypes from '@/assets/placeTypes.js';
import testData from '@/assets/testData.js';
import { getVenuesByPlaceIdService, getSurroundingPlacesService, createPlanService, updatePlanService, optimizePlanService, getAllPlacesService } from '@/api/plan.js';
import { getPlanByIdService } from '@/api/plan.js';
import '@vueup/vue-quill/dist/vue-quill.snow.css'
const value2 = ref(0)
const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900'])
const currentRating = ref(0)


const planResponse = ref(null);
let place = ref(null);
const myRating = ref(0);
let route = useRouter();

let planStore = usePlanStore();



const places = ref([])
const findPlaceVisible = ref(false)
const placeDetailVisible = ref(false)
const detailedDisplayPlace = ref()

const placePageNum = ref(1)//当前地点页
const placeTotal = ref(20)//每页地点总树
const placePageSize = ref(3)//每页条数

const planRequestModel = ref(
  {
    "plan": {
      "title": '',
      "transport": '',
      "strategy": ''
    },
    "placeId": '',
    "venueIds": []
  }
)

const mapView = ref('')
const placeName = ref('')
const placeAddress = ref('')
const selectedPlace = ref('请选择游学目的地（编辑后显示）')

const fetchPlan = async () => {
  planRequestModel.value.venueIds = []
  const planId = planStore.currentPlanId;
  if (planId) {
    // console.log(planId)
    const response = await getPlanByIdService(planId);
    planResponse.value = response.data;
    planRequestModel.value.plan.title = planResponse.value.plan.title;
    planRequestModel.value.plan.transport = planResponse.value.plan.transport;
    planRequestModel.value.plan.strategy = planResponse.value.plan.strategy;
    planRequestModel.value.placeId = planResponse.value.placeId;
    planRequestModel.value.plan.mapView = planResponse.value.plan.mapView;
    mapView.value = planRequestModel.value.plan.mapView
    selectedVenues.value = planResponse.value.venues;
    for (let i = 0; i < planResponse.value.venues.length; i++) {
      planRequestModel.value.venueIds.push(planResponse.value.venues[i].id);
    }
    
  }

};

fetchPlan()

const getPlaces = async () => {
  const response = await getAllPlacesService({
    pageNum: placePageNum.value,
    pageSize: placePageSize.value,
    name: placeName.value,
    address: placeAddress.value
  });
  places.value = response.data.items;
  placeTotal.value = response.data.total;

};

const placeOnSizeChange = (size) => {
  placePageSize.value = size
  getPlaces()
  // location.reload()
}
//当前页码发生变化，调用此函数
const placeOnCurrentChange = (num) => {
  placePageNum.value = num
  getPlaces()
  // location.reload()
}

const venues = ref([])

const selectedVenues = ref([])
const venueSelectorVisible = ref(false)
const venueSelectedVisible = ref(false)
const venueSurroundingVisible = ref(false)
const centeredVenue = ref(false)

const venuePageNum = ref(1)//当前地点页
const venueTotal = ref(20)//每页地点总树
const venuePageSize = ref(3)//每页条数
const venueName = ref('')
const venueType = ref('')

const getVenues = async () => {
  if (planRequestModel.value.placeId == '') {
    ElMessage.error("请选择一个游学目的地")
    return;
  }
  // console.log(planRequestModel.placeId)
  const response = await getVenuesByPlaceIdService(planRequestModel.value.placeId, {
    pageNum: venuePageNum.value,
    pageSize: venuePageSize.value,
    venueName: venueName.value,
    type: venueType.value
  });
  venues.value = response.data.items;
  venueTotal.value = response.data.total;

};
// getVenues()

const venueOnSizeChange = (size) => {
  venuePageSize.value = size
  getVenues()
}
//当前页码发生变化，调用此函数
const venueOnCurrentChange = (num) => {
  venuePageNum.value = num
  getVenues()
}


// 表单数据
const title = ref('');
const transport = ref('');
const strategy = ref('');
const departure = ref(null);
// const selectedPlace = ref(null);
const selectedRadius = ref('');
const category = ref('');
const type = ref('');

// 原始数据
const originalItems = ref(testData);

// 已选地点
const selectedItems = ref([]);

// 周边场所
const surroundingItems = ref([]);

// 筛选符合类别的地点
const filteredItems = computed(() => {
  return category.value
    ? originalItems.value.filter((item) => item.type === category.value)
    : originalItems.value;
});

// 选择地点
const selectItem = (item) => {
  if (!selectedItems.value.some(selected => selected.id === item.id)) {
    selectedItems.value.push(item);
  } else {
    ElMessage.error('已添加');
  }
};

// 删除已选地点
const removeItem = (index) => {
  selectedVenues.value.splice(index, 1);
  planRequestModel.value.venueIds.splice(index, 1);
};

// 获取原始数据
const fetchOriginalItems = async () => {
  const placeId = locationStore.location.id;
  console.log(placeId);
  const result = await getVenuesByPlaceIdService(placeId, {});
  originalItems.value = result.data.items;
};

// 获取周边场所数据
const fetchSurroundingPlaces = async () => {
  const placeId = planRequestModel.value.placeId; // 获取 placeId
  const venueId = centeredVenue.value.id; // 获取选定场所的 id
  console.log(placeId);
  console.log(venueId);

  if (!selectedPlace.value) {
    ElMessage.error('未选择中心场所');
    return;
  }
  const query = {
    type: type.value,
    radius: selectedRadius.value,
  };

  const response = await getSurroundingPlacesService(placeId, venueId, query);
  surroundingItems.value = response.data;
};

const getLabelByValue = (value) => {
  const type = placeTypes.find(type => type.value === value);
  return type ? type.label : value;
}

const updatePlan = async () => {
  const loadingScreen = ElLoading.service({ fullscreen: true })
  
  let response = await updatePlanService(planStore.currentPlanId, planRequestModel.value);
  if (response.code == 1) {
    ElMessage.error("更新失败")
  }
  // let newPlanId = response.data;
  route.push("/plan/show")
  ElMessage.success("更新成功")
  loadingScreen.close()
}

const optimizePlan = async () => {
  if (planRequestModel.value.venueIds[0] != planRequestModel.value.venueIds[planRequestModel.value.venueIds.length - 1]) {
    ElMessage.error("只有回到出发点的方案可以被优化");
    return
  }
  const loadingScreen = ElLoading.service({ fullscreen: true })
  
  let response = await optimizePlanService(planStore.currentPlanId, planRequestModel.value);

  route.push("/plan/show")
  ElMessage.success("优化成功")
  loadingScreen.close()
}


</script>



<template>
  <el-row style="height: 100vh;" v-if="planResponse">
    <!-- 左侧可滑动部分 -->
    <el-col :span="12" class="left-column">
      <el-scrollbar class="scrollbar">
        <!-- 第一个卡片 -->
        <el-card class="card">
          <template #header>
            <div class="card-header">
              <h3>stuTravel™游学计划</h3>
              <el-button type="primary" class="next-button" @click="optimizePlan">
                优化计划
                <el-icon class="el-icon--right">
                  <Finished />
                </el-icon>
              </el-button>
              <el-button type="primary" class="next-button" @click="updatePlan">
                更新计划
                <el-icon class="el-icon--right">
                  <Edit />
                </el-icon>
              </el-button>
            </div>
          </template>
          <div class="card1-content">
            <div style="display: flex;">
              <div style="flex: 30%;"><el-button type="primary"
                  @click="findPlaceVisible = true; getPlaces()">选择游学目的地</el-button>
              </div>
              <div></div>
              <div style="flex: 70%;">
                {{ planResponse.plan.title }} {{ selectedPlace }}
              </div>
            </div>
          </div>
        </el-card>



        <el-dialog v-model="findPlaceVisible" title="选择游学目的地" width="90%">
          <el-form inline>
            <el-form-item label="名称">
              <el-input v-model="placeName" placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item label="地址">
              <el-input v-model="placeAddress" placeholder="请输入地址"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="placePageNum = 1; getPlaces();">提交</el-button>
              <el-button @click="placeName = ''; placeAddress = ''; getPlaces()">重置</el-button>
            </el-form-item>
          </el-form>


          <el-scrollbar style="height: 400px;">
            <el-row v-for="(item, index) in places" :key="index">
              <el-card style="width: 80%" shadow="hover" :style="{ marginBottom: '20px' }">
                <div style="display: flex;">
                  <div style="flex: 30%;"><img
                      :src="JSON.parse(item.images)[0] != null && JSON.parse(item.images)[0] !== 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Platopainting.jpg' ? JSON.parse(item.images)[0] : 'https://picsum.photos/640/360'"
                      style="width: 100%;" /></div>
                  <div style="flex: 60%; padding: 0 10px;">
                    <h2>
                      <el-icon>
                        <Place />
                      </el-icon>
                      {{ item.name }}
                    </h2>
                    <p>
                      <el-icon>
                        <View />
                      </el-icon>
                      热度:
                      {{ item.popularity }}
                    </p>
                    <p>评分：
                      <el-rate v-model="item.rating" disabled show-score text-color="#ff9900"
                        score-template="{value} 分" />
                    </p>
                  </div>
                  <div style="flex: 20%; padding: 0 10px;">
                    <p>
                      <el-button @click="placeDetailVisible = true; detailedDisplayPlace = item">查看详情</el-button>
                    </p>
                    <p>
                      <el-button type="primary"
                        @click="selectedPlace = item.name; planRequestModel.placeId = item.id; selectedVenues = []; findPlaceVisible = false, planRequestModel.venueIds = []">添加为游学目的地</el-button>
                    </p>
                  </div>
                </div>
              </el-card>
            </el-row>
          </el-scrollbar>




          <el-drawer v-model="placeDetailVisible" title="地点详情" direction="rtl" size="80%">
            <h2>{{ detailedDisplayPlace.name }}</h2>
            <h3>地址：{{ detailedDisplayPlace.address }}</h3>
            <el-row>
              <el-col>
                <el-icon>
                  <View />
                </el-icon>
                热度:
                {{ detailedDisplayPlace.popularity }}
              </el-col>
              <el-col>
                评分：
                <el-rate v-model="detailedDisplayPlace.rating" disabled show-score text-color="#ff9900"
                  score-template="{value} 分" />
              </el-col>
            </el-row>
            <h3>简介</h3>
            <p>
              {{ detailedDisplayPlace.description }}
            </p>
            <h3>精彩图片</h3>
            <div class="block text-center">
              <el-carousel height="300px" type="card">
                <el-carousel-item v-for="item in JSON.parse(detailedDisplayPlace.images)" :key="item">
                  <img
                    :src="item != null && item !== 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Platopainting.jpg' ? item : 'https://picsum.photos/640/360'"
                    style="height: 100%;" />
                </el-carousel-item>
              </el-carousel>
            </div>
          </el-drawer>





          <el-pagination v-model:current-page="placePageNum" v-model:page-size="placePageSize"
            :page-sizes="[3, 5, 10, 15]" layout="jumper, total, sizes, prev, pager, next" background :total="placeTotal"
            @size-change="placeOnSizeChange" @current-change="placeOnCurrentChange"
            style="margin-top: 20px; justify-content: center" />

        </el-dialog>




        <el-card class="card">
          <div class="card1-content">
            <div class="form-container">
              <div class="form-item title-item">
                <div class="form-label">计划标题</div>
                <el-input v-model="planRequestModel.plan.title" class="input-title" placeholder="你想叫你的计划什么呢" />
              </div>
              <div class="form-item select-item">
                <div class="form-label">交通工具</div>
                <el-select v-model="planRequestModel.plan.transport" placeholder="选择交通工具" clearable
                  class="select-inline">
                  <el-option label="走路" value="WALK" />
                  <el-option label="骑行" value="BIKE" />
                </el-select>
              </div>
              <div class="form-item select-item">
                <div class="form-label">策略</div>
                <el-select v-model="planRequestModel.plan.strategy" placeholder="选择策略" clearable class="select-inline">
                  <el-option label="时间优先" value="TIME" />
                  <el-option label="距离优先" value="DIST" />
                </el-select>
              </div>
            </div>
          </div>
        </el-card>



        <el-card class="card">
          <el-card class="hoverable-card" @click='venueSelectorVisible = true; getVenues()'>
            <p class="card-text">场所规划器</p>
          </el-card>
        </el-card>




        <el-dialog v-model="venueSelectorVisible" title="添加浏览场所" width="90%">
          <el-form inline>
            <el-form-item label="名称">
              <el-input v-model="venueName" placeholder="请输入场所名称"></el-input>
            </el-form-item>
            <el-form-item>
              <el-select v-model="venueType" placeholder="选择场所类别" clearable class="select-inline" style="width: 100px;">
                <el-option v-for="option in placeTypes" :key="option.value" :label="option.label"
                  :value="option.value" />
              </el-select></el-form-item>
            <el-form-item>
              <el-button type="primary" @click="venuePageNum = 1; getVenues();">提交</el-button>
              <el-button @click="venueName = ''; venueType = ''; getVenues()">重置</el-button>
            </el-form-item>
          </el-form>

          <el-scrollbar style="height: 400px;">

            <el-row v-for="(item, index) in venues" :key="index">
              <el-card style="width: 80%" shadow="hover" :style="{ marginBottom: '20px' }">
                <div style="display: flex; justify-content: center;">
                  <div style="flex: 60%; padding: 0 10px;">
                    <h2>{{ getLabelByValue(item.type) }}</h2>
                  </div>
                  <div style="flex: 60%; padding: 0 10px;">
                    <h2>
                      <el-icon>
                        <Place />
                      </el-icon>
                      {{ item.name }}
                    </h2>
                    <p>
                      <el-icon>
                        <View />
                      </el-icon>
                      热度:
                      {{ item.popularity }}
                    </p>
                    <p>评分：
                      <el-rate v-model="item.rating" disabled show-score text-color="#ff9900"
                        score-template="{value} 分" />
                    </p>
                  </div>
                  <div style="flex: 20%; padding: 0 10px;">
                    <p>
                      <el-button type="primary"
                        @click="selectedVenues.push(item); planRequestModel.venueIds.push(item.id); ElMessage.success('添加成功')">添加到浏览路线末尾</el-button>
                    </p>
                  </div>
                </div>
              </el-card>
            </el-row>
          </el-scrollbar>

          <el-pagination v-model:current-page="venuePageNum" v-model:page-size="venuePageSize"
            :page-sizes="[3, 5, 10, 15]" layout="jumper, total, sizes, prev, pager, next" background :total="venueTotal"
            @size-change="venueOnSizeChange" @current-change="venueOnCurrentChange"
            style="margin-bottom: 20px; justify-content: center" />

          <div style="display: flex; justify-content: center;">
            <el-button type="primary" @click="venueSelectorVisible = false">完成</el-button>
            <el-button type="primary" @click="venueSelectedVisible = true">查看已添加地点</el-button>
          </div>



          <el-drawer v-model="venueSelectedVisible" title="已选场所" direction="rtl" size="30%">
            <el-scrollbar style="height: 100%;">

              <el-row v-for="(item, index) in selectedVenues" :key="index">
                <el-card style="width: 80%" shadow="hover" :style="{ marginBottom: '5px' }">
                  <div style="flex: 20%; padding: 0 10px;">
                    <p>类型：{{ getLabelByValue(item.type) }}</p>
                  </div>
                  <div style="flex: 60%; padding: 0 10px;">
                    <p>{{ item.name }}</p>
                  </div>
                  <div style="flex: 20%; padding: 0 10px;">
                    <el-button type="danger" @click="removeItem(index)">
                      移除场所
                    </el-button>
                  </div>
                </el-card>
              </el-row>
            </el-scrollbar>

          </el-drawer>




        </el-dialog>





        <!-- 第二个卡片 -->
        <el-card class="card">
          <template #header>
            <div class="card-header">
              <span class="left-text">浏览顺序</span>

            </div>
          </template>
          <div>
            <el-scrollbar style="height: 400px;">

              <el-row v-for="(item, index) in selectedVenues" :key="index">
                <el-card style="width: 80%" shadow="hover" :style="{ marginBottom: '5px' }">
                  <div style="flex: 20%; padding: 0 10px;">
                    <p>类型：{{ getLabelByValue(item.type) }}</p>
                  </div>
                  <div style="flex: 60%; padding: 0 10px;">
                    <p>{{ item.name }}</p>
                  </div>
                  <div style="flex: 20%; padding: 0 10px;">
                    <el-button @click="centeredVenue = item; venueSurroundingVisible = true">
                      查看周边
                    </el-button>
                    <el-button type="danger" @click="removeItem(index)">
                      移除场所
                    </el-button>
                  </div>
                </el-card>
              </el-row>
            </el-scrollbar>
          </div>
        </el-card>




        <el-dialog v-model="venueSurroundingVisible" title="周边地点" width="90%">
          <el-card class="card">
            <template #header>
              <div class="card-header">
                <span class="left-text">筛选周边场所</span>
                <div class="right-container">
                  <el-button :icon="Search" @click="fetchSurroundingPlaces">查询</el-button>
                </div>
                <!-- 搜索内容 -->
              </div>
            </template>
            <div class="button-container">
              <div>
                <span class="departure-label">场所</span>
                <el-select v-model="centeredVenue.name" placeholder="选定场所" disabled class="select-inline"
                  style="width: 200px;">
                  <el-option v-for="item in selectedItems" :key="item.id" :label="item.name" :value="item" />
                </el-select>
                <span class="departure-label" style="padding-left: 10px;">距离</span>
                <el-select v-model="selectedRadius" placeholder="距离" clearable class="select-inline"
                  style="width: 90px;">
                  <el-option label="50m" value="50" />
                  <el-option label="150m" value="150" />
                  <el-option label="250m" value="250" />
                  <el-option label="500m" value="500" />
                  <el-option label="1000m" value="1000" />
                  <el-option label="2000m" value="2000" />
                </el-select>
                <span class="departure-label" style="padding-left: 10px;">类别</span>
                <el-select v-model="type" placeholder="选择场所类别" clearable class="select-inline" style="width: 100px;">
                  <el-option v-for="option in placeTypes" :key="option.value" :label="option.label"
                    :value="option.value" />
                </el-select>
              </div>
              <el-scrollbar style="height: 400px;">
                <el-row v-for="(item, index) in surroundingItems" :key="index">
                  <el-card style="width: 80%" shadow="hover" :style="{ marginBottom: '20px' }">
                    <div style="display: flex; justify-content: center;">
                      <div style="flex: 60%; padding: 0 10px;">
                        <h2>{{ getLabelByValue(item.type) }}</h2>
                      </div>
                      <div style="flex: 60%; padding: 0 10px;">
                        <h2>
                          <el-icon>
                            <Place />
                          </el-icon>
                          {{ item.name }}
                        </h2>
                        <p>
                          <el-icon>
                            <View />
                          </el-icon>
                          热度:
                          {{ item.popularity }}
                        </p>
                        <p>评分：
                          <el-rate v-model="item.rating" disabled show-score text-color="#ff9900"
                            score-template="{value} 分" />
                        </p>
                      </div>
                      <div style="flex: 20%; padding: 0 10px;">
                        <p>
                          <el-button type="primary"
                            @click="selectedVenues.push(item); planRequestModel.venueIds.push(item.id); ElMessage.success('添加成功')">添加到浏览路线末尾</el-button>
                        </p>
                      </div>
                    </div>
                  </el-card>
                </el-row>
              </el-scrollbar>
            </div>
          </el-card>
        </el-dialog>




        <!-- 第四个卡片 -->

      </el-scrollbar>
    </el-col>




    <!-- 右侧固定部分 -->
    <el-col :span="12" class="right-column">
      <iframe :src="mapView == '' ? 'http://127.0.0.1:8080/upload/place_holder.html' : mapView" frameborder="0"
        height="100%" width="100%"></iframe>
    </el-col>
  </el-row>
</template>





<style scoped>
.left {
  width: 200px;
}

.right {
  flex: 1;
}

.left-column {
  height: 100%;
  padding-right: 10px;
}

.scrollbar {
  padding-right: 10px;
}

.right-column {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  position: sticky;
  top: 0;
  height: 100vh;
}

.placeholder-image {
  width: 100%;
  height: auto;
  max-width: 600px;
  max-height: 400px;
}

.card {
  width: calc(100% - 10px);
  margin-bottom: 20px;
  margin-right: 10px;
}

.place-select-button {
  /* 按钮样式 */
  display: inline-block;
  /* 将按钮作为内联元素显示，以便水平居中 */
}

.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.button-container .el-button {
  margin-bottom: 5px;
  margin-left: 5px;
}

.card-header {
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: auto;
}

.university-name {
  display: inline-block;
  font-weight: bold;
  font-size: 18px;
}

.form-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.form-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-item {
  flex: 2.5;
}

.select-item {
  flex: 1;
}

.form-label {
  margin-bottom: 5px;
}

.input-title {
  width: 100%;
}

.select-inline {
  width: 100%;
}

.back-button {
  margin-right: 30px;
}

.next-button {
  margin-left: auto;
}

.departure-label {
  display: inline-block;
  margin-right: 5px;
}

.left-text {
  display: inline-block;
  margin-right: auto;
}

.right-container {
  display: flex;
  align-items: center;
}

.hoverable-card:hover {
  cursor: pointer;
  background-color: #409EFF !important;
  box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1) !important;
}

.hoverable-card:hover .card-text {
  color: white;
  /* 设置文字颜色为白色 */
}

.card-text {
  text-align: center;
}
</style>