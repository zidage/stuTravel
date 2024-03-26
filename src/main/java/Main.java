import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // 创建一些示例数据
        List<Location> locations = new ArrayList<>();
        locations.add(new Location("景点A", 8.5, 4.2));
        locations.add(new Location("景点B", 7.9, 4.5));
        locations.add(new Location("景点C", 9.1, 4.8));
        locations.add(new Location("景点D", 6.3, 4.0));
        locations.add(new Location("景点E", 8.2, 4.6));
        locations.add(new Location("景点F", 7.5, 4.3));
        locations.add(new Location("景点G", 9.0, 4.7));
        locations.add(new Location("景点H", 6.8, 4.1));
        locations.add(new Location("景点I", 8.4, 4.4));
        locations.add(new Location("景点J", 7.7, 4.2));
        // ... 添加更多地点

        List<String> userInterests = new ArrayList<>();
        userInterests.add("景点A");
        userInterests.add("景点C");
        userInterests.add("景点E");
        userInterests.add("景点G");
        userInterests.add("景点I");
        userInterests.add("景点B");
        userInterests.add("景点D");
        userInterests.add("景点F");
        userInterests.add("景点H");
        userInterests.add("景点J");
        // ... 添加更多用户兴趣

        // 创建推荐系统实例
        RecommendationSystem recommendationSystem = new RecommendationSystem();

        // 获取前10个推荐的景点和学校
        List<Location> recommendedLocations = recommendationSystem.recommendTop10(locations, userInterests);

        // 输出推荐的景点和学校
        for (Location location : recommendedLocations) {
            System.out.println("推荐的景点或学校：" + location.name);
        }
    }
}