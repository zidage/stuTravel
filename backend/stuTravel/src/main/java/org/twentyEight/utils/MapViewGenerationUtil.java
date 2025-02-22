package org.twentyEight.utils;

import java.io.*;
import java.nio.charset.Charset;

public class MapViewGenerationUtil {
    private String script_path;
    private ProcessBuilder pb;
    private Process process;
    private OutputStreamWriter writer;
    private BufferedReader reader;

    public MapViewGenerationUtil() throws IOException {
        script_path = System.getenv("DS_PY_UTIL");
        pb = new ProcessBuilder("python3", script_path + "/map_view_generator.py");
        process = pb.start();
        writer = new OutputStreamWriter(process.getOutputStream());
        reader = new BufferedReader(new InputStreamReader(process.getInputStream(), Charset.forName("GBK")));
    }

    public void creatQuery(String query) throws IOException {
        writer.write(query + "\n");
        writer.flush(); // 刷新缓冲区以确保数据被发送
        // return reader.readLine();
    }

    public String getStdOut() throws IOException {
        String line;
        return reader.readLine();
    }

    public String endProcess() throws IOException, InterruptedException {
        writer.close();
        String result = reader.readLine();
        process.waitFor();
        return result;
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        MapViewGenerationUtil mapViewGenerationUtil = new MapViewGenerationUtil();
        mapViewGenerationUtil.creatQuery(
                "-r 12345 0 0 Harbin_Institute_of_Technology_Weihai 1226934978 425467438 657768326 657768305 6001784001 17344858");

        // mapViewGenerator.getStdOut();
        mapViewGenerationUtil.endProcess();
    }
}
