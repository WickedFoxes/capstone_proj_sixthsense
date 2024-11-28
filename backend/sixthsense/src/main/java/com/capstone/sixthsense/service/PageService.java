package com.capstone.sixthsense.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.repository.PageRepo;
import com.capstone.sixthsense.repository.ProjectRepo;

@Service
public class PageService {
	@Value("${engine.key}")
	String enginekey;
	
	@Autowired
	private PageRepo repo;
	@Autowired
	private ProjectRepo project_repo;	
	
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
		if(pageDTO.getUrl().isBlank()) {
			throw new NotNullException("It should not be provided as a blank space.");
		}
		
		page.setTitle(pageDTO.getTitle());
		page.setUrl(pageDTO.getUrl());
		return repo.save(page);
	}
	public Page setPageReady(Page page, Account acccount) {
		Project project = page.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(acccount.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		page.setStatus(ScanStatus.READY);
		return repo.save(page);
	}
	public List<Page> setPagesReadyInProject(Project project, Account account) {
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		List<Page> pages = repo.findAllByProject(project);
		for(Page page : pages) {
			if(page.getStatus().equals(ScanStatus.COMPLETE) || page.getStatus().equals(ScanStatus.ERROR)) {
				page.setStatus(ScanStatus.READY);
				repo.save(page);
			}
		}
		return pages;
	}
	
	public List<Page> getReadyPageListWithKey(String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return repo.findAllByStatus(ScanStatus.READY);
	}
	
	public Page getPageWithKey(long id, String key) {
		Page page = repo.findById(id);
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		if(!enginekey.equals(key)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return page;
	}
	
	public Page updatePageWithKey(PageDTO pageDTO, String key) {
		if(!enginekey.equals(key)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Page page = repo.findById(pageDTO.getId());
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		page.setStatus(pageDTO.getStatus());
		return repo.save(page);
	}
	public List<Page> setPagesReadyInProjectWithKey(long project_id, String key) {
		if(!enginekey.equals(key)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Project project = project_repo.findById(project_id);
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		List<Page> pages = repo.findAllByProject(project);
		for(Page page : pages) {
			if(page.getStatus().equals(ScanStatus.COMPLETE) || page.getStatus().equals(ScanStatus.ERROR)) {
				page.setStatus(ScanStatus.READY);
				repo.save(page);
			}
		}
		return pages;
	}
}
