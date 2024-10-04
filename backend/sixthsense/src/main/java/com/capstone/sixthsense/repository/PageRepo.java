package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;

@Repository
public interface PageRepo extends JpaRepository<Page, Integer>{
	List<Page> findAllByProject(Project project);
	Page findById(int id);
}
