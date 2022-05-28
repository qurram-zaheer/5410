package com.assignment1.partc;

import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

import static com.assignment1.partc.DynamoDB.*;

public class Wrapper {
    public static void main(String[] args) {
        Region region = Region.US_EAST_1;
        DynamoDbClient ddb = DynamoDbClient.builder()
                .region(region)
                .build();

        DynamoDbEnhancedClient enhancedClient = DynamoDbEnhancedClient.builder()
                .dynamoDbClient(ddb)
                .build();

        System.out.println("Table before adding records: ");
        System.out.println("[");
        scan(enhancedClient);
        System.out.println("]");
        System.out.println("Table after adding records:");
        System.out.println("[");

        addRecords(enhancedClient);
        scan(enhancedClient);
        System.out.println("]");

        System.out.println("Table after updating records:");
        System.out.println("[");
        updateRecords(enhancedClient);
        scan(enhancedClient);
        System.out.println("]");
    }
}
