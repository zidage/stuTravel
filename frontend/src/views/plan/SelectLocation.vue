

<script setup>
  import { useLocationStore } from '@/stores/location.js';  // 导入大学存储
  import { ref, watch, toRaw } from 'vue';
  import { ElMessage } from 'element-plus';
  import { useRouter } from 'vue-router';
  import { getAllPlacesService } from '@/api/plan.js';
  const router = useRouter();

  const locationStore = useLocationStore();

  // 测试数据
  const locations = ref([]);

  const query = ref('');
  const selectedLocation = ref(locationStore.location ? locationStore.location.name : '');
  const selectedLocationData = ref(locationStore.location ? locationStore.location : null);

  const filteredLocations = ref(locations.value);

  const onInput = () => {
    if (query.value) {
      filteredLocations.value = locations.value.filter((university) =>
        university.name.toLowerCase().includes(query.value.toLowerCase())
      );
    } else {
      filteredLocations.value = locations.value;
    }
  };

  const onSelect = (value) => {
    selectedLocation.value = value;
    selectedLocationData.value = locations.value.find(university => university.name === value);
    console.log('Selected university:', toRaw(selectedLocationData.value)); // 控制台输出选中的大学json数据
  };

  //确认选择
  const confirmSelection = () => {
    if (selectedLocationData.value) {
      locationStore.setLocation(selectedLocationData.value); // 存储选中的大学
      console.log('stored1 university:', toRaw(locationStore.location)); // 控制台输出选中的大学json数据
      console.log(locationStore.location.name); // 控制台输出选中的大学json数据
      router.push('/plan');
      ElMessage.success(`已选择: ${selectedLocationData.value.name}`);
    } else {
      ElMessage.warning('请先选择一个大学或公园');
    }
  };

  // 选中热门大学
  const selectUniversity = (curLocation) => {
    selectedLocation.value = curLocation.name;
    selectedLocationData.value = curLocation;
    locationStore.setLocation(curLocation); // 存储选中的大学
    console.log('Selected university from hot list:', toRaw(curLocation)); // 控制台输出选中的大学json数据
    ElMessage.success(`已选择: ${curLocation.name}`);
  };

  // 获取所有地点
  const fetchTotalLocations = async () => {
    let result = await getAllPlacesService();
    locationStore.setTotalLocations(result.data);
    locations.value = result.data.items;
    filteredLocations.value = locations.value;
  }
  fetchTotalLocations();

  watch(query, onInput);
</script>

<template>
  <!-- 选择大学 -->
  <el-card style="width: 630px; margin: 20px auto;" shadow="always">
    <el-form class="form-container">
      <el-form-item label="请选择大学或公园">
        <div class="input-container">
          <el-select v-model="selectedLocation" filterable placeholder="请输入地点名称" @change="onSelect" @input="onInput"
            class="input">
            <el-option v-for="university in filteredLocations" :key="university.id" :label="university.name"
              :value="university.name" />
          </el-select>
          <el-button type="primary" @click="confirmSelection">确认</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-card>

  <!-- 展示选中大学图片 -->
  <el-carousel :interval="4000" type="card" height="200px" class="carousel-margin">
    <el-carousel-item v-for="item in 6" :key="item">
      <h3 text="2xl" justify="center">{{ item }}</h3>
    </el-carousel-item>
  </el-carousel>

  <!-- 热门大学展示 -->
  <div class="demo-image hot-university-margin">
    <div v-for="university in locations" :key="university.id" class="block" @click="selectUniversity(university)">
      <span class="demonstration">{{ university.name }}</span>
      <el-image style="width: 100px; height: 100px" :src="university.images[0]" fit="cover" />
    </div>
  </div>
</template>

<style scoped>
  .page-container {
    padding: 20px;
  }

  .form-container {
    position: relative;
  }

  .input-container {
    display: flex;
    align-items: center;
  }

  .input {
    flex-grow: 1;
    margin-right: 10px;
    width: 400px;
    /* 设置输入框的宽度 */
  }

  /* 选中大学 */
  .carousel-margin {
    margin-top: 35px;
  }

  .el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
    text-align: center;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
  }

  /* 热门大学 */
  .hot-university-margin {
    margin-top: 50px;
  }

  .demo-image .block {
    padding: 30px 0;
    text-align: center;
    border-right: solid 1px var(--el-border-color);
    display: inline-block;
    width: 20%;
    box-sizing: border-box;
    vertical-align: top;
  }

  .demo-image .block:last-child {
    border-right: none;
  }

  .demo-image .demonstration {
    display: block;
    color: var(--el-text-color-secondary);
    font-size: 14px;
    margin-bottom: 20px;
  }
</style>
