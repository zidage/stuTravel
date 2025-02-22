package org.twentyEight.controller;

import jakarta.validation.constraints.Pattern;
import org.hibernate.validator.constraints.URL;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.twentyEight.pojo.Result;
import org.twentyEight.pojo.User;
import org.twentyEight.service.MapUpdateService;
import org.twentyEight.service.UserService;
import org.twentyEight.utils.JwtUtil;
import org.twentyEight.utils.Md5Util;
import org.twentyEight.utils.ThreadLocalUtil;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/user")
@Validated
public class UserController {

    @Autowired
    private UserService userService;
    @Autowired
    private MapUpdateService mapUpdateService;

    @PostMapping("/regist")
    public Result register(@Pattern(regexp = "^\\S{1,16}$")String username,
                           @Pattern(regexp = "^(?=.*[a-z])(?=.*\\d)[a-zA-Z\\d]{8,32}$")String password) {

        User u = userService.findByUserName(username);
        if (u == null) {
            // 注册
            userService.register(username, password);
            return Result.success();
        } else {
            return Result.error("用户名已被占用");
        }
    }

    @PostMapping("/login")
    public Result<String> login(@Pattern(regexp = "^\\S{1,16}$")String username,
                                @Pattern(regexp = "^(?=.*[a-z])(?=.*\\d)[a-zA-Z\\d]{8,32}$")String password) {
        // 根据用户名查询用户
        User loginUser = userService.findByUserName(username);
        // 判断该用户时候存在
        if (loginUser == null) {
            return Result.error("用户名错误");
        }

        // 判断密码是否正确 loginUser对象中的password是密文
        if (Md5Util.getMD5String(password).equals(loginUser.getPassword())) {
            // 登录成功
            Map<String, Object> claims = new HashMap<>();
            claims.put("id", loginUser.getId());
            claims.put("username", loginUser.getUsername());
            String token = JwtUtil.genToken(claims);
            mapUpdateService.importJsonFilesFromDisk(System.getenv("MAP_DATA") + "/map_exports");
            return Result.success(token);
        }

        return Result.error("密码错误");
    }

    @GetMapping("/userInfo")
    public Result<User> userInfo() {
        // 根据用户名查询用户
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User user = userService.findByUserName(username);
        return Result.success(user);
    }

    @GetMapping("/nickname")
    public Result<String> getNickNameById(@RequestParam Integer id) {
        String nickname = userService.getUserByName(id);
        return Result.success(nickname);
    }

    @PutMapping("/update")
    public Result update(@RequestBody @Validated User user) {
        userService.update(user);
        return Result.success();
    }

    @PatchMapping("/updateAvatar")
    public Result updateAvatar(@RequestParam @URL String avatarUrl) {
        userService.updateAvatar(avatarUrl);
        return Result.success();
    }

    @PatchMapping("/updatePwd")
    public Result updatePwd(@RequestBody Map<String, String> params) {
        // 1.校验参数
        String old_pwd = params.get("old_pwd");
        String new_pwd = params.get("new_pwd");
        String re_pwd = params.get("re_pwd");

        if (!StringUtils.hasLength(old_pwd) || !StringUtils.hasLength(new_pwd) || !StringUtils.hasLength(re_pwd)) {
            return Result.error("缺少必要的参数");
        }

        // 原密码是否正确
        // 调用userService根据用户名拿到密码
        Map<String, Object> map = ThreadLocalUtil.get();
        String username = (String) map.get("username");
        User loginUser = userService.findByUserName(username);
        if (!loginUser.getPassword().equals(Md5Util.getMD5String(old_pwd))) {
            return Result.error("原密码填写不正确");
        }

        // 新密码和确认密码是否相同
        if (!re_pwd.equals(new_pwd)) {
            return Result.error("两次填写的新密码不一致");
        }

        // 2. 调用service完成更新
        userService.updatePwd(new_pwd);
        return Result.success();
    }
}
