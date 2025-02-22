//定义store
import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 第一个参数：名字，唯一性
 * 第二个参数：函数，内部定义状态的所有内容
 * 返回函数
 */
export const useTokenStore = defineStore('token', () => {
  const token = ref('')
  //定义函数，修改ttoken的值
  const setToken = (newToken) => {
    token.value = newToken
  }
  //定义函数，移除token的值
  const removeToken = () => {
    token.value = ''
  }
  return {
    token, setToken, removeToken
  }
}, {
  persist: true//持久化存储
});