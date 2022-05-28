package com.assignment1.partc;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbSortKey;
import software.amazon.awssdk.enhanced.dynamodb.model.BatchWriteItemEnhancedRequest;
import software.amazon.awssdk.enhanced.dynamodb.model.WriteBatch;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;

import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.*;

public class DynamoDB {
    public static List<Map<String, String>> parkList = Arrays.asList(Map.of("name", "Amherst Shore", "place", "6596 Hwy 366", "properties", "On the shore of the Northumberland Strait, offering an attractive mixed woodland setting for camping with some of the warmest saltwater swimming north of the Carolinas.", "size", "Large"),
            Map.of("name", "Battery", "place", "10110 Hwy 4", "properties", "Home to a number of historically significant sites, including the site of a lime kiln used to make plaster and mortar, some of which was used in the construction of Fortress Louisbourg, as well as the remains of two forts that were involved in the French and English struggle over the North American continent.", "size", "Medium"));

    public static Map<String, List<String>> campsites =
            Map.of("Amherst Shore", Arrays.asList("showers"),
                    "Battery", Arrays.asList("firewood", "showers"));

    public static void addRecords(DynamoDbEnhancedClient enhancedClient) {
        DynamoDbTable<Park> parkTable = enhancedClient.table("Parks_NovaScotia", TableSchema.fromBean(Park.class));

        parkList.stream().forEach(park -> {
            Park record = new Park();
            record.setName(park.get("name"));
            record.setPlace(park.get("place"));
            record.setProperties(park.get("properties"));
            record.setSize(park.get("size"));

            parkTable.putItem(record);
        });


    }

    public static void updateRecords(DynamoDbEnhancedClient enhancedClient) {
        DynamoDbTable<Park> parkTable = enhancedClient.table("Parks_NovaScotia", TableSchema.fromBean(Park.class));

        for (Map.Entry<String, List<String>> campMap : campsites.entrySet()) {

        }

        campsites.entrySet().forEach(stringListEntry -> {
            Key key = Key.builder().partitionValue(stringListEntry.getKey()).build();
            Park record = parkTable.getItem(r -> r.key(key));
            record.setTypes_of_Campsites(stringListEntry.getValue());

            parkTable.updateItem(record);
        });

        System.out.println("Updated records successfully");
    }

    public static void scan(DynamoDbEnhancedClient enhancedClient) {

        try {
            DynamoDbTable<Park> custTable = enhancedClient.table("Parks_NovaScotia", TableSchema.fromBean(Park.class));
            Iterator<Park> results = custTable.scan().items().iterator();
            while (results.hasNext()) {

                Park rec = results.next();
                System.out.println(rec.toString());
            }

        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }

    }

}
