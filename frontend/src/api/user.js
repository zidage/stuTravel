//导入request.js请求工具
import request from '@/utils/request.js'

//提供调用注册接口的函数 
export const userRegisterService = (registerData) => {
  const params = new URLSearchParams();
  for (let key in registerData) {
    params.append(key, registerData[key]);
  }
  return request.post('/user/regist', params);
}

//提供调用登录接口的函数
export const userLoginService = (loginData) => {
  const params = new URLSearchParams();
  for (let key in loginData) {
    params.append(key, loginData[key]);
  }
  return request.post('/user/login', params);
}

//获取用户详细信息
export const userInfoService = () => {
  return request.get('/user/userInfo');
}

//修改个人信息
export const userInfoUpdateService = (userInfoData) => {
  return request.put('/user/update', userInfoData);
}

export const userPwdUpdate = (updatePwdData) => {
  return request.patch('/user/updatePwd', updatePwdData)
}

export const getNickname = (userId) => {
  // 创建一个新的 URLSearchParams 对象
  console.log(userId)
  const params = new URLSearchParams();
  // 添加 'id' 参数
  params.append('id', userId);
  // 发送 GET 请求到 '/user/nickname' 端点，并附带参数
  return request.get('/user/nickname', { params });
};
