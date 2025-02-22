<script setup>
import {
    Edit,
    Delete,
    View
} from '@element-plus/icons-vue'

import { ref } from 'vue'
import { usePlanStore } from '@/stores/plan.js';
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus';

const router = useRouter()

const places = ref([])
const plans = ref([])

//分页条数据模型
const pageNum = ref(1)//当前页
const total = ref(20)//总条数
const pageSize = ref(3)//每页条数
const title = ref('')
//用户搜索时选中的分类id
const placeId = ref()


//当每页条数发生了变化，调用此函数
const onSizeChange = (size) => {
    pageSize.value = size
    planList()
}
//当前页码发生变化，调用此函数
const onCurrentChange = (num) => {
    pageNum.value = num
    planList()
}

// 回显文章分类
import { getAllPlacesServiceNoPaging, deletePlanService } from '@/api/plan.js';

const placeList = async () => {
    let result = await getAllPlacesServiceNoPaging();
    console.log(result)
    places.value = result.data
}
placeList();
// console.log(places.value);

// 获取文章列表
import { getPlansService } from '@/api/plan.js'

const planList = async () => {
    let params = {
        pageNum: pageNum.value,
        pageSize: pageSize.value,
        placeId: placeId.value ? placeId.value : null,
        planTitle: title.value ? title.value : null
    }
    let result = await getPlansService(params);
    // 渲染视图
    total.value = result.data.total;
    plans.value = result.data.items;
    // 处理数据，给数据模型扩展一个属性。
    for (let i = 0; i < plans.value.length; i++) {
        let plan = plans.value[i];
        for (let j = 0; j < places.value.length; j++) {
            if (plan.placeId == places.value[j].id) {
                plans.value[i].placeName = places.value[j].name;
            }
        }
    }
}
planList();

let planStore = usePlanStore();
const clickPlan = (id) => {
    planStore.setCurrentPlanId(id);
    // ElMessage.success(`Selected Diary ID: ${id}`);
    router.push('/plan/show');
};


const showDeleteBox = (row) => {
    ElMessageBox.confirm(
        '确定删除',
        '提醒',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(() => {
            deletePlanService(row.id)
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
            location.reload()
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '删除取消',
            })
        })
}



</script>
<template>
    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>计划管理</span>
            </div>
        </template>
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item label="目的地：">
                <el-select placeholder="请选择" v-model="placeId" style="width: 240px">
                    <el-option v-for="p in places" :key="p.id" :label="p.name" :value="p.id">
                    </el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="计划标题：">
                <el-input v-model="title" style="width: 240px" placeholder="请输入计划标题" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="planList">搜索</el-button>
                <el-button @click="placeId = ''; title = ''; planList()">重置</el-button>
            </el-form-item>
        </el-form>
        <!-- 文章列表 -->
        <el-table :data="plans" style="width: 100%" v-if="places">
            <el-table-column label="计划标题" width="400" prop="title"></el-table-column>
            <el-table-column label="地点" prop="placeName"></el-table-column>
            <el-table-column label="生成时间" prop="createTime"> </el-table-column>
            <el-table-column label="操作" width="100">
                <template #default="{ row }">
                    <el-button :icon="View" circle plain type="primary" @click="clickPlan(row.id)"></el-button>
                    <el-button :icon="Delete" circle plain type="danger" @click="showDeleteBox(row)"></el-button>
                </template>
            </el-table-column>
            <template #empty>
                <el-empty description="没有数据" />
            </template>
        </el-table>

        <!-- 分页条 -->
        <el-pagination v-model:current-page="pageNum" v-model:page-size="pageSize" :page-sizes="[3, 5, 10, 15]"
            layout="jumper, total, sizes, prev, pager, next" background :total="total" @size-change="onSizeChange"
            @current-change="onCurrentChange" style="margin-top: 20px; justify-content: flex-end" />

    </el-card>
</template>
<style lang="scss" scoped>
.page-container {
    min-height: 100%;
    box-sizing: border-box;

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
}

/* 抽屉样式 */
.avatar-uploader {
    :deep() {
        .avatar {
            width: 178px;
            height: 178px;
            display: block;
        }

        .el-upload {
            border: 1px dashed var(--el-border-color);
            border-radius: 6px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: var(--el-transition-duration-fast);
        }

        .el-upload:hover {
            border-color: var(--el-color-primary);
        }

        .el-icon.avatar-uploader-icon {
            font-size: 28px;
            color: #8c939d;
            width: 178px;
            height: 178px;
            text-align: center;
        }
    }
}

.editor {
    width: 100%;

    :deep(.ql-editor) {
        min-height: 200px;
    }
}
</style>