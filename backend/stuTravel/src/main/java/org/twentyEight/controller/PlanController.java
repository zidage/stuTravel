package org.twentyEight.controller;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.twentyEight.pojo.*;
import org.twentyEight.service.PlanService;

import java.util.List;

@RestController
@RequestMapping("/plans")
public class PlanController {
    @Autowired
    private PlanService planService;

    @PostMapping("/createPlan")
    public Result<Integer> createPlan(@RequestBody PlanRequest planRequest) {
        planService.createPlanWithVenues(planRequest.getPlan(), planRequest.getPlaceId(), planRequest.getVenueIds());
        return Result.success(planRequest.getPlan().getId());
    }

    @GetMapping("/place/{placeId}/venues")
    public Result<PageBean<Venue>> listVenuesByPlaceIdAndQuery(@PathVariable Long placeId,
                                                               @RequestParam Integer pageNum,
                                                               @RequestParam Integer pageSize,
                                                               @RequestParam(required = false) String venueName,
                                                               @RequestParam(required = false) String type) {
        PageBean<Venue> pb = planService.listVenuesByPlaceId(placeId, pageNum, pageSize, venueName, type);
        return Result.success(pb);
    }

    @GetMapping("/place/{placeId}/{venueId}/nearestVenue")
    public Result<List<Venue>> listNearestVenuesByPlaceVenueId(@PathVariable Long placeId,
                                                               @PathVariable Long venueId,
                                                               @RequestParam(required = false) String venueName,
                                                               @RequestParam(required = false) String type,
                                                               @RequestParam(defaultValue = "200") String radius) {
        List<Venue> nearestVenues = planService.listNearestVenuesByPlaceVenueId(placeId, venueId, venueName, type, Integer.parseInt(radius));
        return Result.success(nearestVenues);
    }

    @GetMapping("/places")
    public Result<PageBean<Place>> listPlace(
            @RequestParam Integer pageNum,
            @RequestParam Integer pageSize,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String address
    ) {
        PageBean<Place> pb = planService.listPlace(pageNum, pageSize, name, address);
        return Result.success(pb);
    }

    @GetMapping("/listPlaceNoPaging")
    public Result<List<Place>> listPlaceWithoutPaging(
            @RequestParam(required = false) String name
    ) {
        List<Place> places = planService.listPlaceNoPaging(name);
        return Result.success(places);
    }

    @GetMapping("/place/{placeId}")
    public Result<Place> getPlaceById(@PathVariable Long placeId) {
        Place place = planService.getPlaceById(placeId);
        return Result.success(place);
    }

    @DeleteMapping("/deletePlan")
    public Result deletePlan(@RequestParam Integer planId) {
        planService.deletePlan(planId);
        return Result.success();
    }

    @PutMapping("/editPlan/{id}")
    public Result updatePlan(@PathVariable Integer id, @RequestBody PlanRequest planRequest) {
        Plan plan = planRequest.getPlan();
        plan.setId(id);
        List<Long> venueIds = planRequest.getVenueIds();
        Long placeId = planRequest.getPlaceId();
        planService.updatePlanWithVenues(plan, placeId, venueIds);
        return Result.success();
    }

    @PutMapping("/optimizePlan/{id}")
    public Result optimizePlan(@PathVariable Integer id, @RequestBody PlanRequest planRequest) {
        Plan plan = planRequest.getPlan();
        plan.setId(id);
        List<Long> venueIds = planRequest.getVenueIds();
        Long placeId = planRequest.getPlaceId();
        planService.optimizePlan(plan, venueIds, placeId);
        return Result.success();
    }

    @GetMapping("/myPlans")
    public Result<PageBean<Plan>> listMyPlan(
            @RequestParam Integer pageNum,
            @RequestParam Integer pageSize,
            @RequestParam(required = false) Integer planId,
            @RequestParam(required = false) Long placeId,
            @RequestParam(required = false) String planTitle
    ) {
        PageBean<Plan> pb = planService.listMyPlan(pageNum, pageSize, placeId, planId, planTitle);
        return Result.success(pb);
    }


    @GetMapping("/myPlansNoPaging")
    public Result<List<Plan>> listMyPlanNoPaging(

            @RequestParam(required = false) Long placeId,
            @RequestParam(required = false) String planTitle
    ) {
        List<Plan> plans = planService.listMyPlanNoPaging(placeId, planTitle);
        return Result.success(plans);
    }


    @GetMapping("/myPlans/{planId}")
    public Result<PlanResponse> getPlanById(
            @PathVariable Integer planId
    ) {
        PlanResponse planResponse = new PlanResponse();
        Plan plan = planService.getPlanById(planId);
        if (plan == null) {
            return Result.error("计划不存在或访问的计划不属于该用户");
        }
        Long placeId = plan.getPlaceId();
        List<Long> venueIds = planService.getVenuesByPlanId(planId);
        List<Venue> venues = planService.getVenuesByVenueIds(venueIds);
        planResponse.setPlan(plan);
        planResponse.setPlaceId(placeId);
        planResponse.setVenues(venues);
        return Result.success(planResponse);
    }

    @Data
    static
    class PlanRequest {
        private Plan plan;
        private Long placeId;
        private List<Long> venueIds;
    }

    @Data
    static
    class PlanResponse {
        private Plan plan;
        private Long placeId;
        private List<Venue> venues;
    }
}


