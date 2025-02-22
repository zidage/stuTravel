package org.twentyEight.service;

import org.twentyEight.pojo.PageBean;
import org.twentyEight.pojo.Place;
import org.twentyEight.pojo.Plan;
import org.twentyEight.pojo.Venue;

import java.util.List;

public interface PlanService {
    public void createPlanWithVenues(Plan plan, Long placeId, List<Long> venueIds);
    public Place getPlaceById(Long placeId);


    void deletePlan(Integer planId);

    void updatePlanWithVenues(Plan plan, Long placeId, List<Long> venueIds);

    PageBean<Place> listPlace(Integer pageNum, Integer pageSize, String name, String address);

    PageBean<Venue> listVenuesByPlaceId(Long placeId, Integer pageNum, Integer pageSize, String venueName, String type);

    PageBean<Plan> listMyPlan(Integer pageNum, Integer pageSize, Long placeId, Integer planId, String planTitle);


    List<Venue> listNearestVenuesByPlaceVenueId(Long placeId, Long venueId, String venueName, String type, Integer radius);


    void optimizePlan(Plan plan, List<Long> venueIds, Long placeId);

    Plan getPlanById(Integer planId);

    List<Long> getVenuesByPlanId(Integer planId);

    List<Venue> getVenuesByVenueIds(List<Long> venueIds);

    List<Place> listPlaceNoPaging(String name);

    List<Plan> listMyPlanNoPaging(Long placeId, String planTitle);
}
