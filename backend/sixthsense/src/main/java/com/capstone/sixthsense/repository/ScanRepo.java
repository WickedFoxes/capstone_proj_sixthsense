package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Scan;

import jakarta.transaction.Transactional;

@Repository
public interface ScanRepo extends JpaRepository<Scan, Integer>{
	@Transactional
	void deleteAllByPage(Page page);
	List<Scan> findAllByPage(Page page);
	Scan findById(int id);
}
