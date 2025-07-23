package com.exemple.veilletech.Controller;

import com.exemple.veilletech.model.Resource;
import com.exemple.veilletech.Repository.ResourceRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/resources")
public class ResourceController {
    private final ResourceRepository repository;

    public ResourceController(ResourceRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/{id}")
    public ResponseEntity<Resource> getResourceById(@PathVariable Long id) {
        Resource resource = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Resource not found"));
        return ResponseEntity.ok(resource);
    }

    @GetMapping("/search")
    public List<Resource> searchResources(@RequestParam String title) {
        return repository.findByTitleContainingIgnoreCase(title);
    }

    @PostMapping
    public ResponseEntity<Resource> createResource(@RequestBody Resource resource) {
        Resource savedResource = repository.save(resource);
        return ResponseEntity.ok(savedResource);
    }

    @GetMapping
    public List<Resource> getAllResources() {
        return repository.findAll();
    }

    @GetMapping("/by-source")
    public List<Resource> getResourcesBySource(@RequestParam String source) {
        return repository.findBySource(source);
    }
}