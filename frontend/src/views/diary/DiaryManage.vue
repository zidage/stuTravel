<script setup>
import {
    Edit,
    Delete
} from '@element-plus/icons-vue'

import { onMounted, ref } from 'vue'

const places = ref([])
const diaries = ref([])
const plans = ref([])

//分页条数据模型
const pageNum = ref(1)//当前页
const total = ref(20)//总条数
const pageSize = ref(3)//每页条数
const title = ref('')
const title_p = ref('')
//用户搜索时选中的分类id
const placeId = ref()
//用户搜索时选中的发布状态
const state = ref('')
//当每页条数发生了变化，调用此函数
const onSizeChange = (size) => {
    pageSize.value = size
    diaryList()
}
//当前页码发生变化，调用此函数
const onCurrentChange = (num) => {
    pageNum.value = num
    diaryList()
}

// 回显文章分类
import { getAllPlacesServiceNoPaging } from '@/api/plan.js';

const placeList = async () => {
    let result = await getAllPlacesServiceNoPaging();
    console.log(result)
    places.value = result.data
}
placeList();
// console.log(places.value);

// 获取文章列表
import { getMyDiaries, diaryAddService, updateDiaryService, diaryDeleteService } from '@/api/diary.js'

const diaryList = async () => {
    let params = {
        pageNum: pageNum.value,
        pageSize: pageSize.value,
        placeId: placeId.value ? placeId.value : null,
        state: state.value ? state.value : null
    }
    let result = await getMyDiaries(params);
    // 渲染视图
    total.value = result.data.total;
    diaries.value = result.data.items;
    // 处理数据，给数据模型扩展一个属性。
    for (let i = 0; i < diaries.value.length; i++) {
        let diary = diaries.value[i];
        for (let j = 0; j < places.value.length; j++) {
            if (diary.placeId == places.value[j].id) {
                diaries.value[i].placeName = places.value[j].name;
            }
        }
    }
}
diaryList();






import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { Plus } from '@element-plus/icons-vue'
//控制抽屉是否显示
const visibleDrawer = ref(false)
//添加表单数据模型
const diaryModel = ref({
    title: '',
    placeId: '',
    planId: '',
    coverImg: '',
    content: '',
    state: ''
})

const editFormVisible = ref(false)


const editDiaryForm = ref({
    id: '',
    title: '',
    placeId: '',
    planId: '',
    coverImg: '',
    content: '',
    state: ''
})



import { getPlansNoPagingService } from '@/api/plan.js'
import { ElMessage, ElMessageBox } from 'element-plus';

const planList = async () => {
    let params = {
        placeId: diaryModel.value.placeId ? diaryModel.value.placeId : null,
        planTitle: title_p.value ? title_p.value : null
    }
    let result = await getPlansNoPagingService(params);
    // 渲染视图
    plans.value = result.data;
    console.log(plans)
}

const planListEdit = async () => {
    let params = {
        placeId: editDiaryForm.value.placeId ? editDiaryForm.value.placeId : null,
        planTitle: title_p.value ? title_p.value : null
    }
    let result = await getPlansNoPagingService(params);
    // 渲染视图
    plans.value = result.data;
    // console.log(plans)
}

planList();


const uploadSuccess = (result) => {
    diaryModel.value.coverImg = result.data;
    console.log(result);
}

// 添加文章
const addDiary = async (clickState) => {
    // 把发布状态赋值给数据模型
    diaryModel.value.state = clickState;
    let result = await diaryAddService(diaryModel.value);

    ElMessage.success(result.data ? result.data : "添加成功");

    // 让抽屉消失
    visibleDrawer.value = false;

    // 刷新当前列表
    diaryList();
}

const showEditBox = (row) => {
    editFormVisible.value = true
    editDiaryForm.value.id = row.id
    editDiaryForm.value.title = row.title
    editDiaryForm.value.placeId = row.placeId
    editDiaryForm.value.planId = row.planId
    editDiaryForm.value.state = row.state
    editDiaryForm.value.content = row.content
    editDiaryForm.value.coverImg = row.coverImg
    planListEdit()
    console.log(editDiaryForm)
}

const editDiary = async () => {
    let res = await updateDiaryService(editDiaryForm.value)
    ElMessage.success(res.message ? res.message : '修改成功')
    editFormVisible.value = false
    diaryList();
}

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
            diaryDeleteService(row.id)
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
            diaryList();
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '删除取消',
            })
        })
}
onMounted(() => {
    placeList()
    planList()
    diaryList()
})
</script>
<template>
    <el-dialog v-model="editFormVisible" title="编辑文章">
        <el-form :model="editDiaryForm" label-width="100px">
            <el-form-item label="日记标题">
                <el-input v-model="editDiaryForm.title" placeholder="请输入标题"></el-input>
            </el-form-item>
            <el-form-item label="目的地">
                <el-select placeholder="请选择" v-model="editDiaryForm.placeId" filterable @change="planListEdit">
                    <el-option v-for="c in places" :key="c.id" :label="c.name" :value="c.id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="关联计划">
                <el-select placeholder="请选择" v-model="editDiaryForm.planId">
                    <el-option v-for="p in plans" :key="p.id" :label="p.title" :value="p.id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="文章封面">
                <el-upload class="avatar-uploader" :auto-upload="true" :show-file-list="false" action="/api/upload"
                    name="file" :on-success="uploadSuccess">
                    <img v-if="editDiaryForm.coverImg" :src="editDiaryForm.coverImg" class="avatar" />
                    <el-icon v-else class="avatar-uploader-icon">
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
            <el-form-item label="文章内容">
                <div class="editor">
                    <quill-editor theme="snow" v-model:content="editDiaryForm.content" contentType="html">
                    </quill-editor>
                </div>
            </el-form-item>
            <el-form-item label="状态">
                <el-select v-model="editDiaryForm.state" placeholder="日记状态">
                    <el-option label="草稿" value="草稿" />
                    <el-option label="已发布" value="已发布" />
                    <el-option label="仅自己可见" value="私密" />
                </el-select>
            </el-form-item>
        </el-form>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="editFormVisible = false, ElMessage({ message: '编辑已取消' })">取消</el-button>
                <el-button type="primary" @click="editDiary">
                    确认
                </el-button>
            </span>
        </template>
    </el-dialog>

    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>日记管理</span>
                <div class="extra">
                    <el-button type="primary" @click="visibleDrawer = true">添加日记</el-button>
                </div>
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

            <el-form-item label="发布状态：">
                <el-select placeholder="请选择" v-model="state" style="width: 120px">
                    <el-option label="已发布" value="已发布"></el-option>
                    <el-option label="草稿" value="草稿"></el-option>
                    <el-option label="私密" value="私密"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="日记标题：">
                <el-input v-model="title" style="width: 240px" placeholder="请输入日记标题" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="diaryList">搜索</el-button>
                <el-button @click="placeId = null; state = ''; title = ''; diaryList()">重置</el-button>
            </el-form-item>
        </el-form>
        <!-- 文章列表 -->
        <el-table :data="diaries" style="width: 100%" v-if="places" >
            <el-table-column label="日记标题" width="400" prop="title"></el-table-column>
            <el-table-column label="地点" prop="placeName"></el-table-column>
            <el-table-column label="发表时间" prop="createTime"> </el-table-column>
            <el-table-column label="状态" prop="state"></el-table-column>
            <el-table-column label="操作" width="100">
                <template #default="{ row }">
                    <el-button :icon="Edit" circle plain type="primary" @click="showEditBox(row)"></el-button>
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

        <!-- 抽屉 -->
        <el-drawer v-model="visibleDrawer" title="添加日记" direction="rtl" size="50%">
            <!-- 添加文章表单 -->
            <el-form :model="diaryModel" label-width="100px">
                <el-form-item label="日记标题">
                    <el-input v-model="diaryModel.title" placeholder="请输入标题"></el-input>
                </el-form-item>
                <el-form-item label="目的地">
                    <el-select placeholder="请选择" v-model="diaryModel.placeId" filterable @change="planList()">
                        <el-option v-for="c in places" :key="c.id" :label="c.name" :value="c.id">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="关联计划">
                    <el-select placeholder="请选择" v-model="diaryModel.planId">
                        <el-option v-for="p in plans" :key="p.id" :label="p.title" :value="p.id">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="文章封面">
                    <!--
                        auto-upload:设置是否上传
                        action：设置服务器接口路径
                        name: 设置上传的文件字段名
                        headers: 设置上传的请求头
                        on-success:设置上传成功的回调函数
                    -->
                    <el-upload class="avatar-uploader" :auto-upload="true" :show-file-list="false" action="/api/upload"
                        name="file" :on-success="uploadSuccess">
                        <img v-if="diaryModel.coverImg" :src="diaryModel.coverImg" class="avatar" />
                        <el-icon v-else class="avatar-uploader-icon">
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-form-item label="文章内容">
                    <div class="editor">
                        <quill-editor theme="snow" v-model:content="diaryModel.content" contentType="html">
                        </quill-editor>
                    </div>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="addDiary('已发布')">发布</el-button>
                    <el-button type="info" @click="addDiary('草稿')">草稿</el-button>
                    <el-button type="info" @click="addDiary('私密')">发布仅自己可见</el-button>
                </el-form-item>
            </el-form>
        </el-drawer>
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