import java.util.List;
// 地点类
public class Place {
    private String id; // 唯一标识符
    private String name; // 地点名称
    private String description; // 描述信息
    private String location; // 地理位置信息（经纬度）
    private List<String> tags; // 标签（例如：历史、文化、自然等）
    private List<String> images; // 地点图片链接列表
    private List<String> recommendations; // 推荐理由或者评论

    // 构造函数
    public Place(String id, String name, String description, String location, List<String> tags, List<String> images, List<String> recommendations) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.location = location;
        this.tags = tags;
        this.images = images;
        this.recommendations = recommendations;
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

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public List<String> getTags() {
        return tags;
    }

    public void setTags(List<String> tags) {
        this.tags = tags;
    }

    public List<String> getImages() {
        return images;
    }

    public void setImages(List<String> images) {
        this.images = images;
    }

    public List<String> getRecommendations() {
        return recommendations;
    }

    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }
}
