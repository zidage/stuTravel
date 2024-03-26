import java.util.List;
// 游学路线规划接口
public interface RoutePlanningInterface {
    Route createRoute(String name, String description, List<Place> places); // 创建新的游学路线
    Route getRouteDetails(String routeId); // 根据路线ID获取路线详情
}
