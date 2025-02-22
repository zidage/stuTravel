package org.twentyEight.pojo;

import com.baomidou.mybatisplus.annotation.TableField;
import lombok.Data;

@Data
public class Place {
    private Long id;
    private String name;
    private Integer popularity;
    private Double rating;
    private String formattedName;
    private String address;
    private String description;

    @TableField(typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String images;
}
