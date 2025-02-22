<script setup>
import {
  Edit,
  Timer,
  Guide,
  Bicycle
} from '@element-plus/icons-vue'
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getDiaryByIdService, updateDiaryService } from '@/api/diary.js';
import { rateDiaryService } from '@/api/diary.js';
import { getPlanByIdService } from '@/api/plan.js';
import { useRouter } from 'vue-router';
import { usePlanStore } from '@/stores/plan.js';
import placeTypes from '@/assets/placeTypes.js';
import '@vueup/vue-quill/dist/vue-quill.snow.css'
// import router from '@/router';
const value2 = ref(0)
const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900'])
const currentRating = ref(0)

const router = useRouter();
let planStore = usePlanStore();

const planResponse = ref(null)
const mapView = ref('')
const placeName = ref('')
const placeAddress = ref('')
const selectedPlace = ref('请选择游学目的地')
const selectedVenues = ref([])
const planId = planStore.currentPlanId;

const fetchPlan = async () => {
  console.log(planId)
  if (planId) {
    // console.log(planId)
    const response = await getPlanByIdService(planId);
    planResponse.value = response.data;
    // console.log(plan.value.plan.mapView)
    selectedVenues.value = planResponse.value.venues
    mapView.value = planResponse.value.plan.mapView
  }

};

fetchPlan()
// onMounted(fetchPlan);


const getLabelByValue = (value) => {
  const type = placeTypes.find(type => type.value === value);
  return type ? type.label : value;
}

const goToPlanEdition = () => {
  router.push('/plan/edit')
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
              <h3>{{ planResponse.plan.title }}</h3>
              <el-button type="primary" class="next-button" @click="goToPlanEdition">
                编辑计划
                <el-icon class="el-icon--right">
                  <Edit />
                </el-icon>
              </el-button>
            </div>
          </template>
        </el-card>



        <el-card class="card">
          <div class="card1-content">
            <div class="form-container">
              <div class="form-item title-item">
                <div class="form-label">路线长度</div>
                <el-card>{{ planResponse.plan.distance }}m</el-card>
              </div>
              <div class="form-item title-item">
                <div class="form-label">路线耗时</div>
                <el-card>{{ Math.floor(planResponse.plan.requiredTime / 60) }}min{{
                  Math.floor(planResponse.plan.requiredTime%60)
                  }}s</el-card>
              </div>
              <div class="form-item title-item">
                <div class="form-label">交通工具</div>
                <el-card>{{ planResponse.plan.transport == 'WALK' ? '步行' : '骑行' }}</el-card>
              </div>
              <div class="form-item title-item">
                <div class="form-label">策略</div>
                <el-card>{{ planResponse.plan.strategy == 'DIST' ? '距离优先' : '时间优先' }}</el-card>
              </div>
            </div>
          </div>
        </el-card>


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
                  <div style="flex: 40%; padding: 0 10px;">
                    <p>类型：{{ getLabelByValue(item.type) }}</p>
                  </div>
                  <div style="flex: 60%; padding: 0 10px;">
                    <p>{{ item.name }}</p>
                  </div>
                </el-card>
              </el-row>
            </el-scrollbar>
          </div>
        </el-card>

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