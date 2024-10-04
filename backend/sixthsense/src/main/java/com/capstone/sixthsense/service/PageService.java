package com.capstone.sixthsense.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Request;
import com.capstone.sixthsense.repository.AccountRepo;
import com.capstone.sixthsense.repository.PageRepo;
import com.capstone.sixthsense.repository.ProjectRepo;

@Service
public class PageService {
	@Autowired
	private PageRepo repo;
	public Page getPage(int id, Account account) {
		Page page = repo.findById(id);
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		Project project = page.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return page;
	}
	public List<Page> getPageList(Project project, Account account){
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotExistException("No data found.");
		}
		return repo.findAllByProject(project);
	}
	public Page createPage(Page page, Account account) {
		Project project = page.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(page.getTitle().isBlank() || page.getUrl().isBlank()) {
    		throw new NotNullException("It should not be provided as a blank space.");
    	}
		return repo.save(page);
	}
	
	public void deletePage(PageDTO pageDTO, Account account) {
		Page page = repo.findById(pageDTO.getId());
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		Project project = page.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		repo.deleteById(pageDTO.getId());
	}
	public Page updatePage(PageDTO pageDTO, Account account) {
		Page page = repo.findById(pageDTO.getId());
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		Project project = page.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(pageDTO.getTitle().isBlank() || pageDTO.getUrl().isBlank()) {
			throw new NotNullException("It should not be provided as a blank space.");
		}
		
		page.setTitle(pageDTO.getTitle());
		page.setUrl(pageDTO.getUrl());
		return repo.save(page);
	}
}
