<template>
  <div>
    <h2>游学社区</h2>
    <el-row :gutter="20">
      <el-col v-for="(item, index) in items" :key="index" :span="4.8">
        <el-card class="custom-card" @click='clickDiary(item.id)'>
          <template #header>{{ item.title }}</template>
          <img :src="item.coverImg"
            style="width: 400px" />
          <template #footer class="footer">
            <div>创建时间：{{item.updateTime}}</div>
            <div>
              <el-icon><User /></el-icon>
              {{ item.createNickname }}
            </div>
            <div>
              <el-icon><View /></el-icon>
              {{ item.popularity }}
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>
  </div>
  <!-- 分页条 -->
  <div class="pagination-container">
    <el-pagination :page-size="pageSize" :pager-count="11" layout="prev, pager, next" :total="total"
      @current-change="handlePageChange" />
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  import { communityListService } from '@/api/diary.js';
  import { useDiaryStore } from '@/stores/diary.js';
  import { useRouter } from 'vue-router'
  import {
      User,
      View
  } from '@element-plus/icons-vue'

  const router = useRouter()


  const diaryStore = useDiaryStore();

  const clickDiary = (id) => {
    diaryStore.setDiaryId(id);
    // ElMessage.success(`Selected Diary ID: ${id}`);
    router.push('/diary/show');
  };

  const items = ref([]);
  const total = ref(0);
  const pageSize = ref(10);
  const pageNum = ref(1);

  const fetchCommunities = async () => {
    const response = await communityListService({
      pageNum: pageNum.value,
      pageSize: pageSize.value,
    });
    items.value = response.data.items;
    total.value = response.data.total;
  };

  const handlePageChange = (newPage) => {
    pageNum.value = newPage;
    fetchCommunities();
  };
  
  onMounted(fetchCommunities);
</script>

<style scoped>
  .el-col {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
    /* 增加下边距 */
  }

  .custom-card {
    width: 100%;
    cursor: pointer;
  }

  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
  }

  .footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
