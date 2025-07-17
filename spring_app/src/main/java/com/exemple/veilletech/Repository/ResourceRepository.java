package com.example.veilletech.repository;

import com.example.veilletech.model.Resource;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ResourceRepository extends JpaRepository<Resource, String> {
    List<Resource> findByTitleContainingIgnoreCase(String title);
}