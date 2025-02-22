// src/stores/plan.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const usePlanStore = defineStore('plan', () => {
  const currentPlanId = ref(null); // 存储当前计划的ID

  // 定义函数，设置当前计划的ID
  const setCurrentPlanId = (newPlanId) => {
    currentPlanId.value = newPlanId;
  };

  // 定义函数，移除当前计划的ID
  const removeCurrentPlanId = () => {
    currentPlanId.value = null;
  };

  return {
    currentPlanId,
    setCurrentPlanId,
    removeCurrentPlanId,
  };
}, {
  persist: true // 持久化存储
});
