package org.twentyEight.utils;


import java.nio.charset.StandardCharsets;


public class HashUtil {
    public static long fnv1a64(String input) {
        final long FNV_64_PRIME = 0x100000001b3L;
        long hash = 0xcbf29ce484222325L;
        for (byte b : input.getBytes(StandardCharsets.UTF_8)) {
            hash ^= b;
            hash *= FNV_64_PRIME;
        }
        return hash;
    }
}
