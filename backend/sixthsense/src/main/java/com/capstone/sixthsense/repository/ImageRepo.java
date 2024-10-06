package com.capstone.sixthsense.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Image;

@Repository 
public interface ImageRepo extends JpaRepository<Image, String>{
	Image findByName(String name);
}
