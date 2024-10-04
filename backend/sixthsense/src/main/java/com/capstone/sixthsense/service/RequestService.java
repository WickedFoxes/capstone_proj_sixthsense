package com.capstone.sixthsense.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.dto.RequestDTO;
import com.capstone.sixthsense.enumeration.RequestStatus;
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
import com.capstone.sixthsense.repository.RequestRepo;

@Service
public class RequestService {
	@Autowired
	private RequestRepo repo;
	public Request getRequest(int id, Account account) {
		Request request = repo.findById(id);
		if(request == null) {
			throw new NotExistException("No data found.");
		}
		Project project = request.getPage().getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return request;
	}
	public List<Request> getRequestList(Page page, Account account){
		Project project = page.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return repo.findAllByPage(page);
	}
	public Request createRequest(Page page, Account account) {
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
		Request request = new Request();
		request.setStatus(RequestStatus.READY);
		request.setPage(page);
		return repo.save(request);
	}
	
	public void deleteRequest(RequestDTO requestDTO, Account account) {
		Request request = repo.findById(requestDTO.getId());
		if(request == null) {
			throw new NotExistException("No data found.");
		}
		Page page = request.getPage();
		Project project = page.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(request.getStatus().equals(RequestStatus.RUNNIG)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		repo.deleteById(requestDTO.getId());
	}
}
