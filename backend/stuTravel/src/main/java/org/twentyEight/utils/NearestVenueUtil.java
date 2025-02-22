package org.twentyEight.utils;

import org.twentyEight.pojo.Venue;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class NearestVenueUtil {
    public static List<Venue> findNearestVenues(List<Venue> venues, double userLat, double userLong, double searchRadius) {
        // 过滤、排序，并限制搜索范围
        List<Venue> nearestVenues = venues.stream()
                .filter(Venue ->  // 根据类型过滤，如果没有指定则跳过这一步
                        DistanceCalculator.calculateDistance(userLat, userLong, Venue.getLatitude(), Venue.getLongitude()) <= searchRadius) // 检查距离是否在搜索半径内
                .sorted(Comparator.comparingDouble(Venue -> DistanceCalculator.calculateDistance(userLat, userLong, Venue.getLatitude(), Venue.getLongitude()))) // 根据距离排序
                .collect(Collectors.toList());
        return nearestVenues;
    }
}

class DistanceCalculator {
    private static final double EARTH_RADIUS = 6371; // 地球半径，单位为千米

    public static double calculateDistance(double startLat, double startLong, double endLat, double endLong) {
        double latDistance = Math.toRadians(endLat - startLat);
        double lonDistance = Math.toRadians(endLong - startLong);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(startLat)) * Math.cos(Math.toRadians(endLat))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = EARTH_RADIUS * c * 1000;
        return distance;
    }
}