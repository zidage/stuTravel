import java.util.List;
// 游学日记管理接口
public interface DiaryManagementInterface {
    Diary createDiary(String title, String content, List<Place> places, String userId); // 创建新的游学日记
    List<Diary> getUserDiaries(String userId); // 获取指定用户的所有日记
    Diary updateDiary(String diaryId, String title, String content); // 更新指定日记的内容和标题
    void deleteDiary(String diaryId); // 删除指定日记
}
