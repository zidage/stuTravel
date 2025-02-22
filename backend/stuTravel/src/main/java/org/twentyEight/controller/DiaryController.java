package org.twentyEight.controller;

import com.github.pagehelper.Page;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.twentyEight.pojo.Diary;
import org.twentyEight.pojo.PageBean;
import org.twentyEight.pojo.Plan;
import org.twentyEight.pojo.Result;
import org.twentyEight.service.DiaryService;
import org.twentyEight.service.PlanService;

@RestController
@RequestMapping("/diary")
public class DiaryController {

    @Autowired
    private DiaryService diaryService;
    @Autowired
    private PlanService planService;

    @PostMapping("/newDiary")
    public Result add(@RequestBody Diary diary) {
        diaryService.add(diary);
        return Result.success();
    }

    @GetMapping("/{diaryId}")
    public Result<DiaryResponse> getByDiaryId(@PathVariable Integer diaryId) {
        DiaryResponse diaryResponse = new DiaryResponse();
        Diary diary = diaryService.getByDiaryId(diaryId);
        incrementPopularityByDiaryId(diaryId);
        if (diary == null) {
            return Result.error("日记不存在或不可见");
        }
        diaryResponse.setDiary(diary);
        String placeName = planService.getPlaceById(diary.getPlaceId()).getName();
        Plan plan = planService.getPlanById(diary.getPlanId());
        diaryResponse.setPlaceName(placeName);
        diaryResponse.setPlan(plan);
        return Result.success(diaryResponse);
    }

    private void incrementPopularityByDiaryId(Integer diaryId) {
        diaryService.incrementPopularityByDiaryId(diaryId);
    }

    @PutMapping("/{diaryId}/rating")
    public Result rateDiaryById(@PathVariable Integer diaryId, @RequestParam String rating) {
        Diary diary = diaryService.getByDiaryId(diaryId);
        if (diary == null) {
            return Result.error("日记不存在或不可见");
        }
        Integer ratingCount = diary.getRatingCount();
        Double numericRating = Double.parseDouble(rating);
        diary.setRating((diary.getRating() * ratingCount + numericRating) / (ratingCount + 1));
        diary.setRatingCount(ratingCount + 1);
        diaryService.updateRating(diary);
        return Result.success();
    }


    @PutMapping("/editDiary")
    public Result editDiary(@RequestBody Diary editDiary) {
        diaryService.updateDiary(editDiary);
        return Result.success();
    }


    @GetMapping("/myDiaries")
    public Result<PageBean<Diary>> list(
            Integer pageNum,
            Integer pageSize,
            @RequestParam(required = false) Long placeId,
            @RequestParam(required = false) String state,
            @RequestParam(required = false) String title
    ) {
        PageBean<Diary> pb = diaryService.list(pageNum, pageSize, placeId, state, title);
        return Result.success(pb);
    }

    @GetMapping("/community")
    public Result<PageBean<Diary>> listCommunity(
            Integer pageNum,
            Integer pageSize,
            @RequestParam(required = false) String title,
            @RequestParam(required = false) Long placeId
    ) {
        PageBean<Diary> pb = diaryService.listCommunity(pageNum, pageSize, placeId);
        return Result.success(pb);
    }

    @DeleteMapping("/deleteDiary")
    public Result deleteDiaryById(@RequestParam Integer id) {
        diaryService.deleteDiaryById(id);
        return Result.success();
    }

    @Data
    static class DiaryResponse {
        Diary diary;
        String placeName;
        Plan plan;

    }
}
