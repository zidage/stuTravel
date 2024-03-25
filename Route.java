import java.util.List;
// 路线类
public class Route {
    private String id; // 唯一标识符
    private String name; // 路线名称
    private String description; // 路线描述
    private List<Place> places; // 组成该路线的地点列表
    private String duration; // 路线所需时间
    private String difficulty; // 路线难度等级

    // 构造函数
    public Route(String id, String name, String description, List<Place> places, String duration, String difficulty) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.places = places;
        this.duration = duration;
        this.difficulty = difficulty;
    }

    // getter和setter方法
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<Place> getPlaces() {
        return places;
    }

    public void setPlaces(List<Place> places) {
        this.places = places;
    }

    public String getDuration() {
        return duration;
    }

    public void setDuration(String duration) {
        this.duration = duration;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(String difficulty) {
        this.difficulty = difficulty;
    }
}
