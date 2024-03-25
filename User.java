import java.util.List;
// 用户类
public class User {
    private String id; // 唯一标识符
    private String username; // 用户名
    private String email; // 邮箱地址
    private String password; // 密码
    private List<String> preferences; // 用户偏好（如兴趣点、旅行风格等）
    private List<Diary> diaries; // 用户发布的日记列表

    // 构造函数
    public User(String id, String username, String email, String password, List<String> preferences, List<Diary> diaries) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
        this.preferences = preferences;
        this.diaries = diaries;
    }

    // getter和setter方法
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public List<String> getPreferences() {
        return preferences;
    }

    public void setPreferences(List<String> preferences) {
        this.preferences = preferences;
    }

    public List<Diary> getDiaries() {
        return diaries;
    }

    public void setDiaries(List<Diary> diaries) {
        this.diaries = diaries;
    }


}
