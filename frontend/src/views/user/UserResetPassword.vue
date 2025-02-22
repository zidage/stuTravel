<script setup>
    import { ref } from 'vue'
    import { userPwdUpdate } from '@/api/user.js'
    import { ElMessage } from 'element-plus'
    
    const rules = {
        old_pwd: [
            { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        new_pwd: [
            { required: true, message: '请输入新密码', trigger: 'blur' },
            {
                pattern: /^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{8,32}$/,
                message: '密码必须是8-32位数字和字母',
                trigger: 'blur'
            }
        ],
        re_pwd: [
            { required: true, message: '请输入确认密码', trigger: 'blur' }
        ]
    }
    const form = ref({
        old_pwd: '',
        new_pwd: '',
        re_pwd: ''
    })

    const clearFormData = () => {
    form.value = {
        old_pwd: '',
        new_pwd: '',
        re_pwd: ''
    }
  }
    //修改用户信息
    const updateUserPwd = async () => {
        let result = await userPwdUpdate(form.value);
        let responseCode = result.code
        if (responseCode == 1) {
            ElMessage.error(result.data)
            clearFormData()
        } else {
            ElMessage.success("修改成功");
        }
        
        
    }
    
</script>
<template>
    <el-card class="page-container">
        <template #header>
            <div class="header">
                <span>密码重置</span>
            </div>
        </template>
        <el-row>
            <el-col :span="12">
                <el-form :model="form" :rules="rules" label-width="100px" size="large">
                    <el-form-item label="旧密码" prop="old_pwd">
                        <el-input type="password" v-model="form.old_pwd"></el-input>
                    </el-form-item>
                    <el-form-item label="新密码" prop="new_pwd">
                        <el-input type="password" v-model="form.new_pwd"></el-input>
                    </el-form-item>
                    <el-form-item label="确认新密码" prop="re_pwd">
                        <el-input type="password" v-model="form.re_pwd"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="updateUserPwd">提交修改</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </el-card>
</template>