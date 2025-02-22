package org.twentyEight.pojo;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class Diary {
    private Integer id;
    private String title;
    private String content;
    private String coverImg;
    private String state;
    private Integer createUser;
    private Integer planId; // 与该游学日记相关的游学计划
    private Integer popularity;
    private Long placeId; // 与该游学日记有关的地点
    private Double rating;
    private Integer ratingCount;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
    private String createNickname;
}