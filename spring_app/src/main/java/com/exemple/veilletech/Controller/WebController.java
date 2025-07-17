package com.example.veilletech.controller;

import com.example.veilletech.repository.ResourceRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class WebController {
    private final ResourceRepository resourceRepository;

    public WebController(ResourceRepository resourceRepository) {
        this.resourceRepository = resourceRepository;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("resources", resourceRepository.findAll());
        return "index";
    }

    @GetMapping("/health")
    @ResponseBody
    public String health() {
        return "OK";
    }
}