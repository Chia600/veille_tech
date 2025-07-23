package com.exemple.veilletech.Repository;

import com.exemple.veilletech.model.Resource;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ResourceRepository extends JpaRepository<Resource, Long> {
    List<Resource> findBySource(String source);
    List<Resource> findByTitleContainingIgnoreCase(String title);
    List<Resource> findByDescriptionContainingIgnoreCase(String description);
    List<Resource> findByLinkContainingIgnoreCase(String link);
    List<Resource> findBySourceAndTitleContainingIgnoreCase(String source, String title);
    List<Resource> findBySourceAndDescriptionContainingIgnoreCase(String source, String description);
    List<Resource> findBySourceAndLinkContainingIgnoreCase(String source, String link);
    List<Resource> findBySourceAndTitleContainingIgnoreCaseAndDescriptionContainingIgnoreCaseAndLinkContainingIgnoreCase(String source, String title, String description, String link);
}