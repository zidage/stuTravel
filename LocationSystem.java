import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

interface SearchLocations {
    List<Location> search(String keyword);
}

interface SortLocations {
    List<Location> sort(List<Location> locations);
}

public class LocationSystem implements SearchLocations, SortLocations {
    @Override
    public List<Location> search(String keyword) {
        // 根据关键字搜索地点，这里简化为直接返回所有地点
        List<Location> allLocations = getAllLocations();
        List<Location> result = new ArrayList<>();
        for (Location location : allLocations) {
            if (location.name.contains(keyword)) {
                result.add(location);
            }
        }
        return result;
    }

    @Override
    public List<Location> sort(List<Location> locations) {
        // 根据热度和评价对地点进行排序
        locations.sort(Comparator.comparingDouble((Location l) -> l.popularity * l.rating).reversed());
        return locations;
    }

    private List<Location> getAllLocations() {
        // 获取所有地点，这里简化为直接返回一个示例列表
        List<Location> locations = new ArrayList<>();
        locations.add(new Location("景点A", 8.5, 4.2));
        locations.add(new Location("景点B", 7.9, 4.5));
        locations.add(new Location("景点C", 9.1, 4.8));
        locations.add(new Location("景点D", 6.3, 4.0));
        locations.add(new Location("景点E", 8.2, 4.6));
        return locations;
    }
}
