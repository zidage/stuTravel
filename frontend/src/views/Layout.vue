<script setup>
  import {
    Management,
    Promotion,
    Share,
    UserFilled,
    User,
    Crop,
    EditPen,
    SwitchButton,
    CaretBottom,
    Reading
  } from '@element-plus/icons-vue'
  import avatar from '@/assets/default.png'
  import { userInfoService } from '@/api/user.js'
  import { useUserInfoStore } from '@/stores/userInfo.js'
  import { useTokenStore } from '@/stores/token.js'
  import { useRouter } from 'vue-router'
  import { ElMessageBox, ElMessage } from 'element-plus'
  const router = useRouter()
  const tokenStore = useTokenStore()
  const userInfoStore = useUserInfoStore()
  //调用函数，获取用户详细信息
  const getUserInfo = async () => {
    let result = await userInfoService();
    userInfoStore.setInfo(result.data);
  }
  getUserInfo();
  console.log(userInfoStore.info);
  const handleCommand = (command) => {
    if (command === 'logout') {
      ElMessageBox.confirm('确定退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userInfoStore.removeInfo();
        tokenStore.removeToken();
        router.push('/login');
      }).catch(() => {
        ElMessage.info('已取消退出');
      });
    } else {
      router.push(`/user/${command}`);
    }
  }
</script>

<template>
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <el-aside width="200px">
      <div class="el-aside__logo"></div>
      <el-menu active-text-color="#ffd04b" background-color="#232323" text-color="#fff" router>
        <!-- 菜单标签 -->
        <el-menu-item index="/plan/PlanWorkbench">
          <el-icon>
            <Promotion />
          </el-icon>
          <span>新建计划</span>
        </el-menu-item>
        <el-menu-item index="/community">
          <el-icon>
            <Share />
          </el-icon>
          <span>游学社区</span>
        </el-menu-item>
        <!-- 子菜单 -->
        <el-sub-menu>
          <template #title>
            <el-icon>
              <UserFilled />
            </el-icon>
            <span>个人中心</span>
          </template>
          <el-menu-item index="/user/diaryManage">
            <el-icon>
              <Reading />
            </el-icon>
            <span>我的日记</span>
          </el-menu-item>
          <el-menu-item index="/plan/planManagement">
            <el-icon>
              <Promotion />
            </el-icon>
            <span>我的计划</span>
          </el-menu-item>
          <el-menu-item index="/user/info">
            <el-icon>
              <User />
            </el-icon>
            <span>基本资料</span>
          </el-menu-item>
          <el-menu-item index="/user/avatar">
            <el-icon>
              <Crop />
            </el-icon>
            <span>更换头像</span>
          </el-menu-item>
          <el-menu-item index="/user/resetPassword">
            <el-icon>
              <EditPen />
            </el-icon>
            <span>重置密码</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <!-- 右侧主区域 -->
    <el-container>
      <!-- 头部区域 -->
      <el-header>
        <div>游学用户：<strong>{{ userInfoStore.info.nickname }}</strong></div>
        <!-- 下拉菜单 -->
        <el-dropdown placement="bottom-end" @command="handleCommand">
          <span class="el-dropdown__box">
            <!-- 头像 -->
            <el-avatar :src="userInfoStore.info.userPic ? userInfoStore.info.userPic : avatar" />
            <el-icon>
              <CaretBottom />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="info" :icon="User">基本资料</el-dropdown-item>
              <el-dropdown-item command="avatar" :icon="Crop">更换头像</el-dropdown-item>
              <el-dropdown-item command="resetPassword" :icon="EditPen">重置密码</el-dropdown-item>
              <el-dropdown-item command="logout" :icon="SwitchButton">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <!-- 中间区域 -->
      <el-main>
        <router-view></router-view>
      </el-main>
      <!-- 底部区域 -->
      <el-footer>stuTravel ©2023 Created by 28组</el-footer>
    </el-container>
  </el-container>
</template>

<style lang="scss" scoped>
  .layout-container {
    height: 100vh;

    .el-aside {
      background-color: #232323;

      &__logo {
        height: 120px;
        background: url('@/assets/logo.png') no-repeat center / 120px auto;
      }

      .el-menu {
        border-right: none;
      }
    }

    .el-header {
      background-color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;

      .el-dropdown__box {
        display: flex;
        align-items: center;

        .el-icon {
          color: #999;
          margin-left: 10px;
        }

        &:active,
        &:focus {
          outline: none;
        }
      }
    }

    .el-footer {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      color: #666;
    }
  }
</style>