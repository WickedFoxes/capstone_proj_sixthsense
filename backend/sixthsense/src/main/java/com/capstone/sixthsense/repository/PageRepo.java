package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;

@Repository
public interface PageRepo extends JpaRepository<Page, Integer>{
	Page findById(int id);
	List<Page> findAllByProject(Project project);
	List<Page> findAllByStatus(ScanStatus status);
}
