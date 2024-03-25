import java.util.Date;
import java.util.List;
// 日记类
public class Diary {
    private String id; // 唯一标识符
    private String title; // 日记标题
    private String content; // 日记内容
    private String author; // 作者
    private Date createdAt; // 创建日期
    private List<Place> placesVisited; // 访问过的地点列表

    // 构造函数
    public Diary(String id, String title, String content, String author, Date createdAt, List<Place> placesVisited) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.author = author;
        this.createdAt = createdAt;
        this.placesVisited = placesVisited;
    }

    // getter和setter方法
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public List<Place> getPlacesVisited() {
        return placesVisited;
    }

    public void setPlacesVisited(List<Place> placesVisited) {
        this.placesVisited = placesVisited;
    }
}

