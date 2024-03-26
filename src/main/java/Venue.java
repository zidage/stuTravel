// 场所类
public class Venue {
    private String id; // 唯一标识符
    private String name; // 场所名称
    private String type; // 场所类型（例如：博物馆、公园等）
    private String address; // 场所地址
    private String operatingHours; // 营业时间
    private String contactInfo; // 联系方式

    // 构造函数
    public Venue(String id, String name, String type, String address, String operatingHours, String contactInfo) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.address = address;
        this.operatingHours = operatingHours;
        this.contactInfo = contactInfo;
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

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getOperatingHours() {
        return operatingHours;
    }

    public void setOperatingHours(String operatingHours) {
        this.operatingHours = operatingHours;
    }

    public String getContactInfo() {
        return contactInfo;
    }

    public void setContactInfo(String contactInfo) {
        this.contactInfo = contactInfo;
    }
}
