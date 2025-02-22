package org.twentyEight.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.twentyEight.pojo.Result;

import java.io.File;
import java.io.IOException;

@RestController
public class FileUploadController {
    @PostMapping("/upload")
    public Result<String> upload(MultipartFile file) throws IOException {
        String originalFilename = file.getOriginalFilename();
        file.transferTo(new File(System.getenv("DS_FILES") + "/"
         + originalFilename));
        return Result.success("http://localhost:8080/upload/" + originalFilename);
    }
}
