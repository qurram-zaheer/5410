package com.assignment1.partb;

import java.io.IOException;

public class Wrapper {
    public static void main(String[] args) {
        Bucket bucket = new Bucket();
        bucket.createBucket("as1-bucket");
        bucket.listBuckets();
        FileProcessor fp = new FileProcessor();
        try {
            String fileText = fp.getFileFromResourceAsStream("Qurram.txt");
            bucket.uploadObject("Qurram", "as1-bucket", fileText);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
