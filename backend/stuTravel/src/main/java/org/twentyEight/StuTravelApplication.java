package org.twentyEight;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.twentyEight.controller.MapUpdateController;

/**
 * Hello world!
 *
 */
@SpringBootApplication
public class StuTravelApplication
{
    public static void main( String[] args ) {
        SpringApplication.run(StuTravelApplication.class, args);
    }

}
