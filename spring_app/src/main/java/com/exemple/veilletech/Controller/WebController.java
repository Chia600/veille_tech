package com.example.veilletech.controller;

import com.example.veilletech.repository.ResourceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {
    @Autowired
    private ResourceRepository repository;

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("resources", repository.findAll());
        return "index";
    }
}