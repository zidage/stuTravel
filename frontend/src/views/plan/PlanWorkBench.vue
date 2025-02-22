<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useLocationStore } from '@/stores/location.js';
import { ArrowLeft, ArrowRight, Delete, Search, Place, View } from '@element-plus/icons-vue';
import placeTypes from '@/assets/placeTypes.js';
import testData from '@/assets/testData.js';
import { getVenuesByPlaceIdService, getSurroundingPlacesService, createPlanService } from '@/api/plan.js';
import { getPlanByIdService } from '@/api/plan.js';
import { usePlanStore } from '@/stores/plan.js';
import { ElLoading } from 'element-plus'



const router = useRouter();
const locationStore = useLocationStore();

// 返回上一页事件

const findPlaceVisible = ref(false)
const placeDetailVisible = ref(false)
const detailedDisplayPlace = ref()

const placePageNum = ref(1)//当前地点页
const placeTotal = ref(20)//每页地点总树
const placePageSize = ref(3)//每页条数





const places = ref([
  {
    "id": 3087627617,
    "name": "北京邮电大学",
    "popularity": 96,
    "rating": 4.6,
    "formattedName": "Beijing_University_of_Posts_and_Telecommunications",
    "address": "中国北京市海淀区北太平庄西土城路10号 邮政编码: 100876",
    "description": "北京邮电大学（英語：Beijing University of Posts and Telecommunications，缩写：BUPT），简称北邮，是中华人民共和国的第一所邮电高等学府，是教育部直属、工业和信息化部共建的全国重点大学，是一所以信息科技为特色、工学门类为主体、工管文理交叉融合的研究型大学，是中国信息科技人才的重要培养基地，是“双一流计划”、原“211工程”和原“985工程优势学科创新平台”高校。\n\n",
    "images": "[\"https://upload.wikimedia.org/wikipedia/commons/1/17/BUPT_Gate.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/5/5e/BUPT_Hongfu_Campus_%2820220406141922%29.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/4/47/BUPT_Shahe_Campus_%2820231202143149%29.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/3/3d/BUPT_shahe_all.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/3/33/BUPT_shahe_canteen.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/0c/BUPT_shahe_dormitory.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/f/f6/BUPT_shahe_library.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/03/BUPT_shahe_teaching.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/6/6e/BUPT_xitucheng_library.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/6/6c/BUPT_xitucheng_main.jpg\"]"
  },
  {
    "id": 3254197874,
    "name": "北京科技大学",
    "popularity": 88,
    "rating": 4.6,
    "formattedName": "University_of_Science_and_Technology_Beijing",
    "address": "中国北京市海淀区学院路30号 邮政编码: 100083",
    "description": "北京科技大学（英語：University of Science and Technology Beijing，縮寫：USTB），简称北科、北科大或北京科大，是位于北京市海淀区学院路的一所教育部直属的全国重点大学，是211工程、2011计划、985优势学科创新平台等高水平大学建设方案入选高校。学校占地约80.39万平方米，校舍建筑总面积97万平方米。\n\n",
    "images": "[\"https://upload.wikimedia.org/wikipedia/commons/5/50/Mechanical_and_Information_Engineering_Building_of_USTB.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/0b/Platopainting.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/8/89/School_of_Materials_Science_and_Engineering_USTB.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/2/24/USTB_Gym.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/1/1c/USTB_west_gate.jpg\"]"
  },
  {
    "id": 3380461192,
    "name": "北京师范大学",
    "popularity": 88,
    "rating": 4.5,
    "formattedName": "Beijing_Normal_University",
    "address": "中国北京市海淀区北太平庄新外大街19号 邮政编码: 100875",
    "description": "北京师范大学（英語：Beijing Normal University，縮寫：BNU），简称北师大。学校的前身是1902年创立的京师大学堂师范馆，1908年改称京师优级师范学堂，独立设校，1912年改名为北京高等师范学校。1923年学校更名为北京师范大学，成为中国历史上第一所师范大学。1931年、1952年北平女子师范大学、辅仁大学先后并入北京师范大学。北京师范大学是中华人民共和国顶尖高校之一，是“双一流A类”和原“985工程”、原“211工程”重点建设大学，是以基础文理学科、教育学、心理学为主要特色的中华人民共和国教育部直属全国重点大学。\n北京师范大学是公立综合性研究型大学。2002年，北京师范大学成为首批拥有自主设置本科专业审批权的6所高校之一。学科点覆盖了除军事学以外的12个学科门类，形成了综合性学科布局。根据中华人民共和国教育部学位与研究生教育发展中心发布的2017年一级学科评估（第四轮）结果，北师大教育学、心理学、中国语言文学、中国史、戏剧与影视学、地理学6个一级学科获评A＋，居中国第六位，2个一级学科获评A，7个一级学科获评A-。在英国高等教育调查公司（QS）公布的2024世界大学排行榜中，北师大排名第271位，在中国内地高校中排名第11位。2017年，北京师范大学进入中国“世界一流大学”建设A类名单，11个学科进入中国“世界一流学科”建设名单，位居中国第8位。\n北京师范大学有两个校区：北京校区（海淀校园、西城校园、昌平校园、育荣校园）和珠海校区。同时也成立了北京师范大学珠海分校（将于2024年终止办学）和北京师范大学-香港浸会大学联合国际学院。\n\n",
    "images": "[\"https://upload.wikimedia.org/wikipedia/commons/4/4f/BNU_Gate.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/3/3e/Beijing_road_1.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/7/7e/East_gate_of_Beijing_Normal_University_%2820200921153346%29.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/1/1c/May_Fourth_Movement_students.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/b/b6/Site_of_Fu_Jen_Catholic_University_in_Peking_%2820201009172530%29.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/d/d4/%E5%8C%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6%E7%A0%94%E7%A9%B6%E6%89%80.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/4/4c/%E5%8C%97%E5%B8%88%E5%A4%A7%E5%90%AF%E5%8A%9F%E5%83%8F2.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/9/99/%E5%8C%97%E5%B8%88%E5%A4%A7%E6%9C%A8%E9%93%8E2.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/1/1c/%E5%8C%97%E5%B8%88%E5%A4%A7%E6%A0%A1%E8%AE%AD%E7%A2%91.jpg\"]"
  },
  {
    "id": 2761923711,
    "name": "北京工业大学",
    "popularity": 80,
    "rating": 4.7,
    "formattedName": "Beijing_University_of_Technology",
    "address": "中国北京市朝阳区 邮政编码: 100021",
    "description": "北京工业大学（英語：Beijing University of Technology，缩写：BJUT），简称北工大，创立于1960年，是一所以工学为主，理学、工学、文学、法学、经济学、管理学、教育学、艺术学相结合的综合性市属重点大学，于1981年成为国家教育部批准的第一批硕士学位授予单位，1985年成为博士学位授予单位，1996年通过国家“211工程”预审。2017年9月，学校正式进入国家一流学科建设高校行列。2020年8月，2020软科世界大学学术排名发布，北京工业大学首次进入全球500强。2021年，工程学，材料科学，化学，环境科学与生态学、计算机科学、生物学与生物化学共6个学科进入ESI前%1。现时为QS世界大学排名中国内地50强大学，是“双一流”和原“211工程”重点建设大学。\n北京工业大学共有平乐园、通州、中蓝、管庄、花园村、琉璃井和惠新东街7个校区，总占地约96.0151万平方米，其中平乐园校区为校本部，通州校区为大部分大一新生所在校区。学校定期出版《北京工业大学学报》《北京工业大学学报（社会科学版）》等学术刊物。\n校训是“不息为体，日新为道”，取自唐代哲学家刘禹锡的《问大钧赋》“以不息为体，以日新为道”。“不息”源自《周易》“乾”卦的象词“天行健，君子以自强不息”，“体”则有物质存在的状态、本体、本性、禀性之意；“日新”源自《尚书·盘铭》“苟日新，日日新，又日新”，“道”，则有本质、法则、规律、主张、宗旨之意。学校校花为海棠花，校树为银杏树。\n\n",
    "images": "[\"https://upload.wikimedia.org/wikipedia/commons/b/b9/BU_Tech.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/00/BU_Tech2.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/1/15/BU_Tech3.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/b/b9/BU_Tech4.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/a/a0/BU_Tech5.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/d/dc/Beijing_University_of_Technology_Entrance.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/e/e8/Beijing_University_of_Technology_Stadium.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/0b/Platopainting.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/6/6d/%E5%8C%97%E4%BA%AC%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6%28%E9%80%9A%E5%B7%9E%E6%A0%A1%E5%8C%BA%29_%E6%93%8D%E5%9C%BA%E5%90%8E%E6%96%B9%E5%B0%8F%E8%B7%AF_01.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/4/43/%E5%8C%97%E4%BA%AC%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6_%E6%B1%B2%E5%AD%A6%E6%A5%BC_01.jpg\"]"
  },
  {
    "id": 2866460375,
    "name": "北京交通大学",
    "popularity": 72,
    "rating": 4.7,
    "formattedName": "Beijing_Jiaotong_University",
    "address": "中国北京市海淀区交大东路",
    "description": "北京交通大学（英語：Beijing Jiaotong University，縮寫：BJTU），简称北京交大、北交大，原名北方交通大学，校本部座落在北京市海淀区西直门外上园村3号，是中国第一所专门培养管理人才的高等学校，是中国近代铁路管理、电信教育的发祥地。\n北京交通大学是教育部直属、教育部、交通运输部、北京市人民政府和中国国家铁路集团有限公司共建的全国重点大学，“211工程”、“985工程优势学科创新平台”（小985）项目建设高校、国家首批“双一流”建设高校，首轮建设任务已顺利完成，“智慧交通”一流学科领域建设得到评审专家高度评价。牵头的“2011计划”“轨道交通安全协同创新中心”是国家首批14个认定的协同创新中心之一。校训为王阳明之“知行”。\n\n",
    "images": "[\"https://upload.wikimedia.org/wikipedia/commons/e/ea/BJTUgate.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/4/4c/Bjtu_siyuan_building.JPG\", \"https://upload.wikimedia.org/wikipedia/commons/5/54/Bjtudoor1920.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/02/Bjtugingko.JPG\", \"https://upload.wikimedia.org/wikipedia/commons/4/41/Bjtulibrary.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/7/7c/Fanghua_park_bjtu.JPG\", \"https://upload.wikimedia.org/wikipedia/commons/1/14/Graduation_Jiaoda.JPG\", \"https://upload.wikimedia.org/wikipedia/commons/9/95/Maoyishengbjtu.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/2/2f/Ming_pool_bjtu.jpg\", \"https://upload.wikimedia.org/wikipedia/commons/0/0b/Platopainting.jpg\"]"
  }
])


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




const venues = ref([
  {
    "id": 399008789,
    "name": "主教学楼",
    "type": "nan",
    "latitude": 39.95992864753576,
    "longitude": 116.35219703998455,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008789
  },
  {
    "id": 399008790,
    "name": "图书馆",
    "type": "nan",
    "latitude": 39.96145138789443,
    "longitude": 116.35189501307093,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008790
  },
  {
    "id": 399008979,
    "name": "教一楼",
    "type": "nan",
    "latitude": 39.96053895523992,
    "longitude": 116.35179344616746,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008979
  },
  {
    "id": 399008980,
    "name": "行政办公楼",
    "type": "nan",
    "latitude": 39.960700489509705,
    "longitude": 116.351777726217,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008980
  },
  {
    "id": 399008981,
    "name": "财务处",
    "type": "nan",
    "latitude": 39.96077154667922,
    "longitude": 116.35140472766149,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008981
  },
  {
    "id": 399008982,
    "name": "后勤处",
    "type": "nan",
    "latitude": 39.96070367196975,
    "longitude": 116.35141965603697,
    "placeId": 3087627617,
    "popularity": 0,
    "osmid": 399008982
  }
]
)





const mapView = ref('')
const placeName = ref('')
const placeAddress = ref('')

const selectedPlace = ref('请选择游学目的地')

import { getAllPlacesService } from '@/api/plan.js';

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



onMounted(getPlaces)



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

const createPlan = async () => {
  const loadingScreen = ElLoading.service({ fullscreen: true })
  loadingScreen.close()
  let response = await createPlanService(planRequestModel.value);
  let newPlanId = response.data;
  
  let planResponse = await getPlanByIdService(newPlanId);
  mapView.value = planResponse.data.plan.mapView
  ElMessage.success("添加成功")
}








//fetchOriginalItems();
</script>

<template>
  <el-row style="height: 100vh;">
    <!-- 左侧可滑动部分 -->
    <el-col :span="12" class="left-column">
      <el-scrollbar class="scrollbar">
        <!-- 第一个卡片 -->
        <el-card class="card">
          <template #header>
            <div class="card-header">
              <h3>stuTravel™游学计划</h3>
              <el-button type="primary" class="next-button" @click="createPlan">
                生成计划
                <el-icon class="el-icon--right">
                  <ArrowRight />
                </el-icon>
              </el-button>
            </div>
          </template>
          <div class="card1-content">
            <div style="display: flex;">
              <div style="flex: 30%;"><el-button type="primary"
                  @click="findPlaceVisible = true; getPlaces()">选择游学目的地</el-button>
              </div>
              <div style="flex: 70%;">
                {{ selectedPlace }}
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
                        @click="selectedPlace = item.name; planRequestModel.placeId = item.id; selectedVenues = []; findPlaceVisible = false">添加为游学目的地</el-button>
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
      <iframe :src="mapView == '' ? 'http://127.0.0.1:8080/upload/place_holder.html' : mapView" frameborder="0" height="100%" width="100%"></iframe>
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
