package com.capstone.sixthsense.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.PageService;
import com.capstone.sixthsense.service.ProjectService;

@Controller
public class PageController {
	@Autowired
	private PageService pageService;
	@Autowired
	private ProjectService projectService;
	@Autowired
	private AccountService accountService;	
	
	@GetMapping("/page/list/by-project/{project}")
	public ResponseEntity<Object> getPageList(@PathVariable("project") int project_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		Project project = projectService.getProject(project_id, account);
    		List<Page> list = pageService.getPageList(project, account);
    		List<PageDTO> listDTO = new ArrayList<>();
    		for(Page page : list) {
    			listDTO.add(new PageDTO(page));
    		} 
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PostMapping("/page/create/by-project/{project}")
	public ResponseEntity<Object> createPage(
			@PathVariable("project") int project_id,
			@RequestBody Page page
		){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		
		try {
			Project project = projectService.getProject(project_id, account);
			page.setProject(project);
			page.setStatus(ScanStatus.READY);
			pageService.createPage(page, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new PageDTO(page));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@PutMapping("/page/update")
	public ResponseEntity<Object> updatePage(@RequestBody PageDTO pageDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			Page page = pageService.updatePage(pageDTO, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new PageDTO(page));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@DeleteMapping("/page/delete")
	public ResponseEntity<Object> deletePage(@RequestBody PageDTO pageDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			pageService.deletePage(pageDTO, account);
			return ResponseEntity.status(HttpStatus.ACCEPTED).body(pageDTO);
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@PostMapping("/page/run/{page_id}")
	public ResponseEntity<Object> runPage(@PathVariable("page_id") int page_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		try {
			Page page = pageService.getPage(page_id, account);
			page = pageService.setPageReady(page, account);
			return ResponseEntity.status(HttpStatus.OK).body(new PageDTO(page));
			
		} catch(Exception e) {
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
		}
	}
	
	@PostMapping("/page/run/by-project/{project_id}")
	public ResponseEntity<Object> runAllPageInProject(@PathVariable("project_id") int project_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		try {
			Project project = projectService.getProject(project_id, account);
			List<Page> list = pageService.setPagesReadyInProject(project, account);
			List<PageDTO> dtolist = new ArrayList<>();
			for(Page page : list)
				dtolist.add(new PageDTO(page));
			return ResponseEntity.status(HttpStatus.OK).body(dtolist);
			
		} catch(Exception e) {
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
		}
	}
	
	@GetMapping("/page/list/ready/by-key/{enginekey}")
	public ResponseEntity<Object> getReadyPageListWithKey(
			@PathVariable("enginekey") String enginekey
	){
    	try{
    		List<Page> list = pageService.getReadyPageListWithKey(enginekey);
    		List<PageDTO> listDTO = new ArrayList<>();
    		for(Page page : list) listDTO.add(new PageDTO(page));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PutMapping("/page/update/by-key/{enginekey}")
	public ResponseEntity<Object> updatePageWithKey(
			@RequestBody PageDTO pageDTO,
			@PathVariable("enginekey") String enginekey
		){    	
		try {
			Page page = pageService.updatePageWithKey(pageDTO, enginekey);
			return ResponseEntity.status(HttpStatus.CREATED).body(new PageDTO(page));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@PutMapping("/page/run/by-project/by-key/{project_id}/{enginekey}")
	public ResponseEntity<Object> runAllPageInProjectWithKey(
			@PathVariable("project_id") int project_id,
			@PathVariable("enginekey") String enginekey
		){
		try {
			List<Page> list = pageService.setPagesReadyInProjectWithKey(project_id, enginekey);
			List<PageDTO> dtolist = new ArrayList<>();
			for(Page page : list)
				dtolist.add(new PageDTO(page));
			return ResponseEntity.status(HttpStatus.OK).body(dtolist);
			
		} catch(Exception e) {
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
		}
	}
}
