package com.capstone.sixthsense.service;

import java.io.File;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.capstone.sixthsense.exception.ImageSaveException;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.repository.ImageRepo;
import com.capstone.sixthsense.model.Image;

import io.jsonwebtoken.io.IOException;

@Service
public class ImageService {
	@Value("${image.save.path}")
	String imgSavePath;
	@Value("${engine.key}")
	String enginekey;
	
	@Autowired
	ImageRepo imageRepo;
	
	public Image save(MultipartFile image) {
	    if(image.isEmpty()) {
	    	throw new NotNullException("It should not be provided as a blank space.");
	    }
	    
    	String fileName = UUID.randomUUID().toString();
	    String fullPathName = imgSavePath + fileName;  
	    try{
	    	image.transferTo(new File(fullPathName));
	    	Image result = imageRepo.save(new Image(fileName, fullPathName));
	    	return result;
	    } catch(Exception e){
	    	throw new ImageSaveException("Unable to save image.");
	    }
	}
    public Image saveWithKey(MultipartFile image, String key){  
	    if(!key.equals(enginekey)) {
	    	throw new NotHaveAuthException("you don't have Auth");
	    }
	    return save(image);
    }
    public String getImagePath(String name){
        Image img = imageRepo.findByName(name);
		if(img == null) {
			throw new NotExistException("No data found.");
		}
        return img.getPath();
    }
    public Image getImageWithKey(String name, String key){
	    if(!key.equals(enginekey)) {
	    	throw new NotHaveAuthException("you don't have Auth");
	    }
    	Image img = imageRepo.findByName(name);
		if(img == null) {
			throw new NotExistException("No data found.");
		}
        return img;
    }
}
