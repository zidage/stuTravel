package org.twentyEight.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.twentyEight.mapper.DiaryMapper;
import org.twentyEight.mapper.PlaceMapper;
import org.twentyEight.mapper.PlanMapper;
import org.twentyEight.mapper.VenueMapper;
import org.twentyEight.pojo.PageBean;
import org.twentyEight.pojo.Place;
import org.twentyEight.pojo.Plan;
import org.twentyEight.pojo.Venue;
import org.twentyEight.service.PlanService;
import org.twentyEight.utils.MapViewGenerationUtil;
import org.twentyEight.utils.NearestVenueUtil;
import org.twentyEight.utils.ThreadLocalUtil;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class PlanServiceImpl implements PlanService {

    @Autowired
    private PlanMapper planMapper;
    @Autowired
    private VenueMapper venueMapper;
    @Autowired
    private PlaceMapper placeMapper;
    @Autowired
    private DiaryMapper diaryMapper;



    @Override
    public void createPlanWithVenues(Plan plan, Long placeId, List<Long> venueIds) {
        Map<String, Object> map = ThreadLocalUtil.get();
        Integer userId = (Integer) map.get("id");
        plan.setCreateUser(userId);
        plan.setCreateTime(LocalDateTime.now());
        plan.setUpdateTime(LocalDateTime.now());
        plan.setPlaceId(placeId);
        planMapper.insertPlan(plan);
        if (venueIds != null && !venueIds.isEmpty()) {
            planMapper.insertPlanVenues(plan.getId(), venueIds);
            for (Long venueId : venueIds) {
                venueMapper.incrementPopularityByVenueId(venueId);
            }
        }
        updatePlanMapView(plan, placeId, venueIds);
    }

    @Override
    public Place getPlaceById(Long placeId) {
        return placeMapper.findPlaceById(placeId);
    }

    @Override
    public void deletePlan(Integer planId) {
        // 删除关联的Plan-Venue记录
        planMapper.deletePlanVenuesByPlanId(planId);
        diaryMapper.deleteDiaryForeignKey(planId);
        // 然后删除计划本身
        planMapper.deletePlan(planId);
    }

    @Override
    public void updatePlanWithVenues(Plan plan, Long placeId, List<Long> venueIds) {
        plan.setPlaceId(placeId);
        planMapper.updatePlan(plan);
        planMapper.deletePlanVenuesByPlanId(plan.getId());

        if (venueIds != null && !venueIds.isEmpty()) {
            planMapper.insertPlanVenues(plan.getId(), venueIds);
        }
        updatePlanMapView(plan, placeId, venueIds);
    }

    @Override
    public void optimizePlan(Plan plan, List<Long> venueIds, Long placeId) {
        try {
            MapViewGenerationUtil mapGenerator = new MapViewGenerationUtil();
            Place place = placeMapper.findPlaceById(placeId);

            String place_formatted = place.getFormattedName();
            StringBuilder queryString = new StringBuilder("-o " + plan.getId() +
                    (plan.getStrategy().equals("DIST") ? " 0" : " 1") +
                    (plan.getTransport().equals("WALK") ? " 0 " : " 1 ") +
                    place_formatted + " ");
            for (Long venueId : venueIds) {
                queryString.append(venueId.toString()).append(" ");
            }
            mapGenerator.creatQuery(queryString.toString());
            try {
                String response = mapGenerator.endProcess();
                String[] venueIdStrings = response.split(",");
                List<Long> newVenueIds = new ArrayList<>();
                for (String venueIdString : venueIdStrings) {
                    newVenueIds.add(Long.parseLong(venueIdString));
                }
                updatePlanWithVenues(plan, placeId, newVenueIds);
            } catch (Exception e) {
                e.printStackTrace();
            }



        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Override
    public Plan getPlanById(Integer planId) {
        Map<String, Object> map = ThreadLocalUtil.get();
        Integer userId = (Integer) map.get("id");
        return planMapper.getPlanById(planId, userId);
    }

    @Override
    public List<Long> getVenuesByPlanId(Integer planId) {
        return venueMapper.listByPlanId(planId);
    }

    @Override
    public List<Venue> getVenuesByVenueIds(List<Long> venueIds) {
        List<Venue> venues = new ArrayList<>();
        for (Long venueId : venueIds) {
            venues.add(venueMapper.findVenueByVenueId(venueId));
        }
        return venues;
    }

    @Override
    public List<Place> listPlaceNoPaging(String name) {
        return placeMapper.list(name, null);
    }

    @Override
    public List<Plan> listMyPlanNoPaging(Long placeId, String planTitle) {
        Map<String, Object> map = ThreadLocalUtil.get();
        Integer userId = (Integer) map.get("id");
        return planMapper.listPlan(userId, null, placeId, planTitle);
    }

    @Override
    public PageBean<Place> listPlace(Integer pageNum, Integer pageSize, String name, String address) {
        PageBean<Place> pb = new PageBean<>();
        PageHelper.startPage(pageNum, pageSize);
        List<Place> as = placeMapper.list(name, address);
        Page<Place> p = (Page<Place>) as;

        pb.setTotal(p.getTotal());
        pb.setItems(p.getResult());
        return pb;
    }



    @Override
    public PageBean<Venue> listVenuesByPlaceId(Long placeId, Integer pageNum, Integer pageSize, String venueName, String type) {
        PageBean<Venue> pb = new PageBean<>();
        PageHelper.startPage(pageNum, pageSize);
        List<Venue> as = venueMapper.listByPlaceId(placeId, venueName, type);
        Page<Venue> p = (Page<Venue>) as;

        pb.setTotal(p.getTotal());
        pb.setItems(p.getResult());
        return pb;
    }


    @Override
    public PageBean<Plan> listMyPlan(Integer pageNum, Integer pageSize, Long placeId, Integer planId, String planTitle) {
        PageBean<Plan> pb = new PageBean<>();
        PageHelper.startPage(pageNum, pageSize);
        Map<String, Object> map = ThreadLocalUtil.get();
        Integer userId = (Integer) map.get("id");
        List<Plan> plans = planMapper.listPlan(userId, planId, placeId, planTitle);
        Page<Plan> p = (Page<Plan>) plans;

        pb.setTotal(p.getTotal());
        pb.setItems(p.getResult());
        return pb;
    }

    @Override
    public List<Venue> listNearestVenuesByPlaceVenueId(Long placeId, Long venueId, String venueName, String type, Integer radius) {
        PageBean<Venue> pb = new PageBean<>();
        List<Venue> venues = venueMapper.listByPlaceId(placeId, venueName, type);
        Venue targetVenue = venueMapper.findVenueByVenueId(venueId);

        return NearestVenueUtil.findNearestVenues(venues, targetVenue.getLatitude(), targetVenue.getLongitude(), radius);
    }




    private void updatePlanMapView(Plan plan, Long placeId, List<Long> venueIds) {
        try {
            MapViewGenerationUtil mapGenerator = new MapViewGenerationUtil();
            Place place = placeMapper.findPlaceById(placeId);

            String place_formatted = place.getFormattedName();
            StringBuilder queryString = new StringBuilder("-r " + plan.getId() +
                    (plan.getStrategy().equals("DIST") ? " 0" : " 1") +
                    (plan.getTransport().equals("WALK") ? " 0 " : " 1 ") +
                    place_formatted + " ");
            for (Long venueId : venueIds) {
                queryString.append(venueId.toString()).append(" ");
            }
            mapGenerator.creatQuery(queryString.toString());
            Integer requiredTime = 0; // (int) Double.parseDouble(result);
            Integer distance = 0;
            try {
                String[] response = mapGenerator.endProcess().split(",");
                distance = (int) Double.parseDouble(response[1]);
                requiredTime = (int) Double.parseDouble(response[0]);
                String savePath = "http://localhost:8080/upload/"
                        + plan.getId() + ".html";
                planMapper.insertPlanMapViewAndTime(plan.getId(), savePath, requiredTime, distance);
            } catch (Exception e) {
                e.printStackTrace();
            }



        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
