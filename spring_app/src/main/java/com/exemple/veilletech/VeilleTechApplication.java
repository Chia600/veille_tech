package com.example.veilletech;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;

@SpringBootApplication
@EntityScan("com.example.veilletech.model")
public class VeilleTechApplication {
    public static void main(String[] args) {
        SpringApplication.run(VeilleTechApplication.class, args);
    }
}