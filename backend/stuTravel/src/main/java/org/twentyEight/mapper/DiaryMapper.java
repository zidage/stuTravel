package org.twentyEight.mapper;

import org.apache.ibatis.annotations.*;
import org.twentyEight.pojo.Diary;

import java.util.List;

@Mapper
public interface DiaryMapper {
    // 新增
    @Insert("insert into diary(title, content, cover_img, state, create_user, create_time, update_time, plan_id, place_id, create_nickname)" +
            "values(#{title}, #{content}, #{coverImg}, #{state}, #{createUser}, #{createTime}, #{updateTime}, #{planId}, #{placeId}, #{createNickname})")
    void add(Diary diary);

    List<Diary> list(Integer userId, Long placeId, String state, String title);

    List<Diary> listCommunity(Long placeId);

    Diary getByDiaryId(Integer id);

    @Update("update diary set popularity=popularity+1 where id=#{diaryId}")
    void incrementPopularityByDiaryId(Integer diaryId);

    @Update("update diary set rating=#{rating}, rating_count=#{ratingCount} where id=#{diaryId}")
    void updateRating(Integer diaryId, Double rating, Integer ratingCount);

    @Update("update diary set title=#{title}, content=#{content}, cover_img=#{coverImg}, state=#{state}, update_time=now()," +
            "plan_id=#{planId}, place_id=#{placeId} where id=#{id}")
    void updateDiary(Diary editDiary);

    @Update("update diary set plan_id=null where plan_id=#{planId}")
    void deleteDiaryForeignKey(Integer planId);

    @Delete("delete from diary where id=#{diaryId}")
    void deleteDiaryById(Integer diaryId);
}
