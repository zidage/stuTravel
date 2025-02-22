import request from '@/utils/request.js';

// 获取所有地点
export const getAllPlacesService = (params) => {
  // 创建一个新的对象来保存非空参数
  const validParams = {};
  for (const key in params) {
    if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
      validParams[key] = params[key];
    }
  }
  return request.get('/plans/places', {
    params: validParams
  });
};

export const getAllPlacesServiceNoPaging = () => {
  return request.get(`/plans/listPlaceNoPaging`);
};

// 获取周边地点
export const getSurroundingPlacesService = (placeId, venueId, params) => {
  if (!placeId || !venueId) {
    throw new Error("Place ID or Venue ID is missing");
  }

  // 创建一个新的对象来保存非空参数
  const validParams = {};
  for (const key in params) {
    if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
      validParams[key] = params[key];
    }
  }

  return request.get(`/plans/place/${placeId}/${venueId}/nearestVenue`, {
    params: validParams
  });
};


// 获取地点内场所
export const getVenuesByPlaceIdService = (placeId, params) => {
  if (!placeId) {
    throw new Error("Place ID is missing");
  }

  const validParams = {};
  for (const key in params) {
    if (params[key] !== null && params[key] !== undefined && params[key] !== '') {
      validParams[key] = params[key];
    }
  }

  return request.get(`/plans/place/${placeId}/venues`, {
    params: validParams
  });
};

// 新建计划服务
export const createPlanService = (data) => {
  if (!data.plan || !data.placeId || !data.venueIds) {
    throw new Error('Missing required fields');
  }

  const { plan } = data;
  if (!plan.title || !plan.transport || !plan.strategy) {
    throw new Error('Missing required plan fields');
  }

  return request.post('/plans/createPlan', data);
};

// 更新计划服务
export const updatePlanService = (planId, data) => {
  if (!planId || !data.plan || !data.placeId || !data.venueIds) {
    throw new Error('Missing required fields');
  }

  const { plan } = data;
  if (!plan.title || !plan.transport || !plan.strategy) {
    throw new Error('Missing required plan fields');
  }

  return request.put(`/plans/editPlan/${planId}`, data);
};


export const optimizePlanService = (planId, data) => {
  if (!planId || !data.plan || !data.placeId || !data.venueIds) {
    throw new Error('Missing required fields');
  }

  const { plan } = data;
  if (!plan.title || !plan.transport || !plan.strategy) {
    throw new Error('Missing required plan fields');
  }

  return request.put(`/plans/optimizePlan/${planId}`, data);
};


// 删除计划服务
export const deletePlanService = (planId) => {
  if (!planId) {
    throw new Error("Plan ID is required");
  }

  return request.delete('/plans/deletePlan', {
    params: { planId }
  });
};

// 获取某个计划服务
export const getPlanByIdService = (id) => {
  if (!id) {
    throw new Error("Plan ID is required");
  }

  return request.get(`/plans/myPlans/${id}`);
};

// 获取已生成全部计划服务
export const getPlansService = (params) => {
  return request.get('/plans/myPlans', {params : params})
};

export const getPlansNoPagingService = (params) => {
  return request.get('/plans/myPlansNoPaging', { params: params })
};
