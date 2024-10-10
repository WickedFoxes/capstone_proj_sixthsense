package com.capstone.sixthsense.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.repository.ProjectRepo;

@Service
public class ProjectService {
	@Autowired
	private ProjectRepo repo;
	public Project getProject(int id, Account account) {
		Project project = repo.findById(id);
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return project;
	}
	public List<Project> getProjectList(Account account){
		return repo.findAllByAccount(account);
	}
	public Project createProject(Project project) {
    	if(project.getAccount() == null || project.getDescription().isBlank()) {
    		throw new NotNullException("It should not be provided as a blank space.");
    	}
		return repo.save(project);
	}
	
	public void deleteProject(ProjectDTO projectDTO, Account account) {
		Project project = repo.findById(projectDTO.getId());
		if(project == null || !project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotExistException("No data found.");
		}
		repo.deleteById(projectDTO.getId());
	}
	public Project updateProject(ProjectDTO projectDTO, Account account) {
		Project project = repo.findById(projectDTO.getId());
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(projectDTO.getTitle().isBlank() || projectDTO.getDescription().isBlank()) {
			throw new NotNullException("It should not be provided as a blank space.");
		}
		
		project.setTitle(projectDTO.getTitle());
		project.setDescription(projectDTO.getDescription());
		return repo.save(project);
	}
}
