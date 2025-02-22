package org.twentyEight.controller;

import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.twentyEight.pojo.Result;
import org.twentyEight.service.MapUpdateService;


@RestController
@RequestMapping("/MapUpdate")
@NoArgsConstructor
public class MapUpdateController {
    @Autowired
    private MapUpdateService mapUpdateService;

    @PostMapping("/import")
    public Result importFiles() {
        mapUpdateService.importJsonFilesFromDisk(System.getenv("MAP_DATA") + "/map_exports");
        return Result.success();
    }
}
