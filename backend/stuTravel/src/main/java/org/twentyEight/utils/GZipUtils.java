package org.twentyEight.utils;

import java.io.*;
import java.util.Base64;
import java.util.zip.*;

public class GZipUtils {
    public static String compressString(String str, String encoding) throws IOException {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        GZIPOutputStream gzipOutputStream = new GZIPOutputStream(byteArrayOutputStream);
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(gzipOutputStream, encoding);
        BufferedWriter bufferedWriter = new BufferedWriter(outputStreamWriter);

        bufferedWriter.write(str);
        bufferedWriter.close();

        // 获取压缩后的字节数组
        byte[] compressedData = byteArrayOutputStream.toByteArray();

        // 使用Base64编码将字节数组转换为字符串
        return Base64.getEncoder().encodeToString(compressedData);
    }

    // 解压缩Base64编码的字符串
    public static String decompressString(String compressedStr, String encoding) throws IOException {
        // 使用Base64解码将字符串转换为字节数组
        byte[] compressedData = Base64.getDecoder().decode(compressedStr);

        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(compressedData);
        GZIPInputStream gzipInputStream = new GZIPInputStream(byteArrayInputStream);
        InputStreamReader inputStreamReader = new InputStreamReader(gzipInputStream, encoding);
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);

        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = bufferedReader.readLine()) != null) {
            stringBuilder.append(line);
        }
        bufferedReader.close();
        return stringBuilder.toString();
    }
}
