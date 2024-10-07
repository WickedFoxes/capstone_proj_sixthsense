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
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.multipart.MultipartFile;

import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.dto.ProjectPageDTO;
import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.PageService;
import com.capstone.sixthsense.service.ProjectService;

@Controller
public class ProjectController {
	@Autowired
	private ProjectService projectService;
	@Autowired
	private PageService pageService;
	@Autowired
	private AccountService accountService;	
	
	@GetMapping("/project/list")
	public ResponseEntity<Object> getProjectList(){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		List<Project> list = projectService.getProjectList(account);
    		List<ProjectDTO> listDTO = new ArrayList<>();
    		for(Project project : list) listDTO.add(new ProjectDTO(project));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}

	@PostMapping("/project-page/create")
	public ResponseEntity<Object> createProject(@RequestBody ProjectPageDTO projectPageDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		
		try {
			Project project = projectPageDTO.getProject();
			List<Page> pageList = projectPageDTO.getPageList();
			project.setAccount(account);
			
			projectService.createProject(project);
			for(Page page : pageList) {
				page.setProject(project);
				page.setStatus(ScanStatus.READY);
				pageService.createPage(page, account);
			}
			return ResponseEntity.status(HttpStatus.CREATED).body(new ProjectDTO(project));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@PostMapping("/project/create")
	public ResponseEntity<Object> createProject(@RequestBody Project project){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		project.setAccount(account);
		
		try {
			projectService.createProject(project);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ProjectDTO(project));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@PutMapping("/project/update")
	public ResponseEntity<Object> updateProject(
			@RequestBody ProjectDTO projectDTO
		){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			Project project = projectService.updateProject(projectDTO, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ProjectDTO(project));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@DeleteMapping("/project/delete")
	public ResponseEntity<Object> deleteProject(@RequestBody ProjectDTO projectDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			projectService.deleteProject(projectDTO, account);
			return ResponseEntity.status(HttpStatus.ACCEPTED).body(projectDTO);
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
}
