package com.capstone.sixthsense.controller;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import com.capstone.sixthsense.model.Image;
import com.capstone.sixthsense.service.ImageService;

import io.jsonwebtoken.io.IOException;

@Controller
public class ImageController {
	@Autowired
	private ImageService imageService;
	
	@GetMapping("/image/{name}")
    public ResponseEntity<Object> getImage(@PathVariable("name") String name) throws IOException {
        // 예시로 이미지 경로를 지정 (id를 이용하여 파일 이름을 구성할 수도 있음)
        // 실제 구현에서는 DB에서 해당 id의 이미지 경로를 가져올 수 있음
        byte[] imageBytes = null;
		try {
	    	String imagePath = imageService.getImagePath(name);
	    	Path path = Paths.get(imagePath);
			imageBytes = Files.readAllBytes(path);
		} catch (Exception e) {
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
			
		}

        HttpHeaders headers = new HttpHeaders();
        headers.setContentLength(imageBytes.length);
        headers.setContentType(MediaType.IMAGE_PNG);
        return new ResponseEntity<>(imageBytes, headers, HttpStatus.OK);
    }
	
	
	@PostMapping("/image/save/by-key/{enginekey}")  
	public ResponseEntity<Object> saveImageWithKey( 
			@RequestParam("image") MultipartFile image, 
			@PathVariable("enginekey") String enginekey) throws IOException {  
		try {
			Image result = imageService.saveWithKey(image, enginekey);
			return ResponseEntity.status(HttpStatus.CREATED).body(result);
		} catch(Exception e) {
			HashMap<String, String> map = new HashMap<>();
			map.put("error", e.getMessage());
			return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
		}		
	}
	
}
