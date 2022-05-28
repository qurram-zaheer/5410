package com.assignment1.partc;

import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbBean;
import software.amazon.awssdk.enhanced.dynamodb.mapper.annotations.DynamoDbPartitionKey;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.StringJoiner;

@DynamoDbBean
public class Park {
    List<String> types_of_Campsites;
    private String name;
    private String place;
    private String properties;
    private String size;

    public Park() {

    }

    public String getPlace() {
        return place;
    }

    public void setPlace(String place) {
        this.place = place;
    }

    public String getProperties() {
        return properties;
    }

    public void setProperties(String properties) {
        this.properties = properties;
    }

    public String getSize() {
        return size;
    }

    public void setSize(String size) {
        this.size = size;
    }

    public List<String> getTypes_of_Campsites() {
        return types_of_Campsites;
    }

    public void setTypes_of_Campsites(List<String> types_of_Campsites) {
        this.types_of_Campsites = types_of_Campsites;
    }

    @DynamoDbPartitionKey
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        StringJoiner sj = new StringJoiner(",\t");

        sj.add(getName()).add(getPlace()).add(getSize());
        String properties = getProperties();
        String cut_props = properties.substring(0, Math.min(properties.length(), 10));
        sj.add(cut_props + "...");
        try {
            sj.add(String.join(",", getTypes_of_Campsites()));
        } catch (NullPointerException ex) {

        }
        return sj.toString();
    }

}
