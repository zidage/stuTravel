import java.util.List;
// 场所查询接口
public interface VenueQueryInterface {
    List<Venue> searchVenues(String keyword, String location); // 根据关键词和位置搜索场所
    Venue getVenueDetails(String venueId); // 根据场所ID获取场所详情
}
