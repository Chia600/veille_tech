package com.exemple.veilletech.Controller;

import com.exemple.veilletech.Repository.ResourceRepository;
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
        model.addAttribute("resources", resourceRepository.findBySource("NVD"));
        return "index";
    }

   /**
    * 
    * @param model 
    * @return
     @GetMapping("/newfetch")
    public String newFetch(Model model) {
        model.addAttribute("resources", resourceRepository.findBySource("NVD"));
        return "newfetch";
    }
*/
    @GetMapping("/certfr")
    public String certFr(Model model) {
        model.addAttribute("resources", resourceRepository.findBySource("CERT-FR"));
        return "certfr";
    }

    @GetMapping("/cisa")
    public String nvdRss(Model model) {
        model.addAttribute("resources", resourceRepository.findBySource("NVD-RSS"));
        return "cisa";
    }

    @GetMapping("/thehackernews")
    public String theHackerNews(Model model) {
        model.addAttribute("resources", resourceRepository.findBySource("TheHackerNews"));
        return "thehackernews";
    }

    @GetMapping("/health")
    @ResponseBody
    public String health() {
        return "OK";
    }
}