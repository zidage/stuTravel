package org.twentyEight.mapper;

import org.apache.ibatis.annotations.*;
import org.twentyEight.pojo.Venue;

import java.util.List;

@Mapper
public interface VenueMapper {
    @Insert("INSERT INTO venue(id, name, type, latitude, longitude, place_id, osmid) VALUES(#{osmid}, #{name}, #{type}, #{latitude}, #{longitude}, #{placeId}, #{osmid})")
    void insertVenue(Venue venue);

    @Select("SELECT * FROM venue WHERE place_id = #{placeId}")
    List<Venue> findVenuesByPlaceId(Long placeId);

    List<Venue> listByPlaceId(Long placeId, String venueName, String type);

    @Select("SELECT * FROM venue WHERE id = #{venueId}")
    Venue findVenueByVenueId(Long venueId);


    @Update("update venue set popularity=popularity+1 where id=#{venueId}")
    void incrementPopularityByVenueId(Long venueId);

    @Select("select venue.* from venue join plan_venue on venue.id = plan_venue.venue_id where plan_venue.plan_id = #{planId}")
    List<Long> listByPlanId(Integer planId);
}
