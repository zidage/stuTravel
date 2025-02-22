package org.twentyEight.pojo;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class Plan {
    private Integer id;
    private Integer createUser;
    private String title;
    private Long placeId;
    private String transport;
    private String strategy;
    private Integer requiredTime;
    private Integer distance;
    private String mapView;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
