import request from '@/utils/request.js'
// import { useTokenStore } from '@/stores/token.js'

export const articleCategoryListService = () => {
  // const tokenStore = useTokenStore();
  //pinia中定义的响应式数据不需要.value
  // return request.get('/category', { headers: { 'Authorization': tokenStore.token } })
  return request.get('/category')

}

export const articleCategoryAddService = (categoryData) => {
  console.log(categoryData)
  return request.post('/category', categoryData)
}

//文章修改
export const articleCategoryUpdateService = (categoryData) => {
  return request.put('/category', categoryData)
}

//文章删除
export const articleCategoryDeleteService = (categoryId) => {
  return request.delete('category', categoryId)
}

// 