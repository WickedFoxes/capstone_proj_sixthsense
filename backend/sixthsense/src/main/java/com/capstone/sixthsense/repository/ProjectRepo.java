package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Project;

@Repository
public interface ProjectRepo extends JpaRepository<Project, Long>{
	List<Project> findAllByAccount(Account account);
	Project findById(long id);
}
