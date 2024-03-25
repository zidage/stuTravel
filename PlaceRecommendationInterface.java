import java.util.List;
// 地点推荐接口
public interface PlaceRecommendationInterface {
    List<Place> getRecommendedPlaces(String userId, List<String> preferences); // 根据用户的ID和偏好返回推荐地点列表
}