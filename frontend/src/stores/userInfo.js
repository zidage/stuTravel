// src/stores/userInfo.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserInfoStore = defineStore('userInfo', () => {
  const info = ref(null);

  // 定义函数，修改userInfo的值
  const setInfo = (newUserInfo) => {
    info.value = newUserInfo;
  };

  // 定义函数，移除userInfo的值
  const removeInfo = () => {
    info.value = null;
  };

  return {
    info, setInfo, removeInfo
  };
}, {
  persist: true // 持久化存储
});
