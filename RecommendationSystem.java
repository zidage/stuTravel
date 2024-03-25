import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Location {
    String name;//地点名称
    double popularity;//热度
    double rating;//评价

    public Location(String name, double popularity, double rating) {
        this.name = name;
        this.popularity = popularity;
        this.rating = rating;
    }
}

interface RecommendTop10 {
    List<Location> recommendTop10(List<Location> locations, List<String> userInterests);
}

public class RecommendationSystem implements RecommendTop10 {
    @Override
    public List<Location> recommendTop10(List<Location> locations, List<String> userInterests) {
        // 根据热度和评价对景点和学校进行排序
        locations.sort(Comparator.comparingDouble((Location l) -> l.popularity * l.rating).reversed());

        // 根据用户兴趣筛选前10个推荐的景点和学校
        List<Location> recommendedLocations = new ArrayList<>();
        for (Location location : locations) {
            if (userInterests.contains(location.name)) {
                recommendedLocations.add(location);
                if (recommendedLocations.size() == 10) {
                    break;
                }
            }
        }

        return recommendedLocations;
    }
}

