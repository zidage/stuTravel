package org.twentyEight.service.impl;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.twentyEight.mapper.PlaceMapper;
import org.twentyEight.mapper.VenueMapper;
import org.twentyEight.pojo.Place;
import org.twentyEight.pojo.Venue;
import org.twentyEight.service.MapUpdateService;
import org.twentyEight.utils.HashUtil;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.zip.CRC32;

@Service
public class MapUpdateServiceImpl implements MapUpdateService {
    @Autowired
    private PlaceMapper placeMapper;
    @Autowired
    private VenueMapper venueMapper;
    @Override
    public void importJsonFilesFromDisk(String directoryPath) {
        File mainDirectory = new File(directoryPath);
        if (mainDirectory.isDirectory()) {
            File[] directories = mainDirectory.listFiles();
            for (File subDir : directories) {
                File[] mapFile = subDir.listFiles((dir, name) -> name.toLowerCase().endsWith(".json"));
                File jsonFile = mapFile[0];
                try {
                    ObjectMapper objectMapper = new ObjectMapper();
                    String jsonContent = new String(Files.readAllBytes(jsonFile.toPath()));
                    JsonNode rootNode = objectMapper.readTree(jsonContent);

                    // 读取Place信息
                    Place place = new Place();
                    place.setName(rootNode.get("name").asText());
                    place.setRating(rootNode.get("rating").asDouble());
                    place.setPopularity(rootNode.get("popularity").asInt());
                    String[] dataPath = rootNode.get("data_path").asText().split("/");
                    place.setFormattedName(dataPath[dataPath.length - 1]);
                    place.setAddress(rootNode.get("address").asText());
                    place.setId(computeUniqueId(place.getAddress()));
                    place.setDescription(rootNode.get("description").asText());
                    JsonNode arrayNode =  rootNode.get("images");
                    if (arrayNode != null && arrayNode.isArray()) {
                        List<String> imageUrls = new ArrayList<>();
                        Iterator<JsonNode> it=arrayNode.elements();
                        while(it.hasNext()) {
                            JsonNode itemNode = it.next();
                            imageUrls.add(itemNode.asText());
                        }
                        place.setImages(objectMapper.writeValueAsString(imageUrls));
                    }
                    placeMapper.insertPlace(place);

                    // 读取Venue信息
                    JsonNode amenityNode = rootNode.get("amenity");
                    JsonNode amenityListNode = amenityNode.get("amenity_list");
                    if (amenityListNode != null && amenityListNode.isArray()) {
                        Iterator<JsonNode> elements = amenityListNode.elements();
                        while (elements.hasNext()) {
                            JsonNode venueNode = elements.next();
                            Venue venue = new Venue();

                            venue.setOsmid(venueNode.has("id") ? venueNode.get("id").asLong() : null);
                            venue.setName(venueNode.has("name") ? venueNode.get("name").asText() : null);
                            venue.setType(venueNode.has("type") ? venueNode.get("type").asText() : null);
                            venue.setLatitude(venueNode.has("latitude") ? venueNode.get("latitude").asDouble() : null);
                            venue.setLongitude(venueNode.has("longitude") ? venueNode.get("longitude").asDouble() : null);
                            venue.setPlaceId(place.getId());

                            venueMapper.insertVenue(venue);
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private Long computeUniqueId(String name) {
        CRC32 crc = new CRC32();
        crc.update(name.getBytes());
        return crc.getValue();
    }
}
