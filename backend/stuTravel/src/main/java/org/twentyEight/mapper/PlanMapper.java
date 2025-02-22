package org.twentyEight.mapper;

import org.apache.ibatis.annotations.*;
import org.twentyEight.pojo.Plan;

import java.util.List;

@Mapper
public interface PlanMapper {
    @Select("select * from plan where id = #{planId}")
    Plan getPlanById(Integer planId, Integer userId);

    @Insert("insert into " +
            "plan (create_user, title, transport, place_id, create_time, update_time, strategy) " +
            "values (#{createUser}, #{title}, #{transport}, #{placeId}, #{createTime}, #{updateTime}, #{strategy})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    void insertPlan(Plan plan);

    @Insert({"<script>",
            "INSERT INTO plan_venue (plan_id, venue_id) VALUES ",
            "<foreach collection='venueIds' item='venueId' separator=','>",
            "(#{planId}, #{venueId})",
            "</foreach>",
            "</script>"
    })
    void insertPlanVenues(Integer planId, List<Long> venueIds);

    @Delete("DELETE FROM plan_venue WHERE plan_id = #{planId}")
    void deletePlanVenuesByPlanId(@Param("planId") Integer planId);

    @Delete("DELETE FROM plan WHERE id = #{id}")
    void deletePlan(@Param("id") Integer id);

    @Update("update plan set title=#{title}, transport=#{transport}, strategy=#{strategy}, update_time=now() where id=#{id}")
    void updatePlan(Plan plan);

    List<Plan> listPlan(Integer userId, Integer planId, Long placeId, String planTitle);

    @Update("update plan set map_view=#{savePath}, required_time=#{requiredTime}, distance=#{distance}, update_time=now() where id=#{id}")
    void insertPlanMapViewAndTime(Integer id, String savePath, int requiredTime, Integer distance);
}
