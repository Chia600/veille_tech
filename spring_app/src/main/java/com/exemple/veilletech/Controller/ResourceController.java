package com.example.veilletech.controller;

import com.example.veilletech.model.Resource;
import com.example.veilletech.repository.ResourceRepository;
import org.owasp.html.Sanitizers;
import org.owasp.html.PolicyFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/resources")
public class ResourceController {
    @Autowired
    private ResourceRepository repository;

    @PostMapping
    public Resource addResource(@RequestBody Resource resource) {
        PolicyFactory policy = Sanitizers.FORMATTING.and(Sanitizers.LINKS);
        resource.setTitle(policy.sanitize(resource.getTitle()));
        resource.setDescription(policy.sanitize(resource.getDescription()));
        resource.setId(UUID.randomUUID().toString());
        return repository.save(resource);
    }

    @GetMapping
    public List<Resource> getResources() {
        return repository.findAll();
    }

    @GetMapping("/search")
    public List<Resource> searchResources(@RequestParam String category) {
        return repository.findByTitleContainingIgnoreCase(category);
    }
}