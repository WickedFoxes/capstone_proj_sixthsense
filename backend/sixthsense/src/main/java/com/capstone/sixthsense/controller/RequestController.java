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
import org.springframework.web.bind.annotation.RequestParam;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.dto.RequestDTO;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Request;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.PageService;
import com.capstone.sixthsense.service.ProjectService;
import com.capstone.sixthsense.service.RequestService;

@Controller
public class RequestController {
	@Autowired
	private RequestService requestService;
	@Autowired
	private PageService pageService;
	@Autowired
	private AccountService accountService;	
	
	@GetMapping("/request/list/by-page/{page}")
	public ResponseEntity<Object> getRequestList(@PathVariable("page") int page_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		Page page = pageService.getPage(page_id, account);
    		List<Request> list = requestService.getRequestList(page, account);
    		List<RequestDTO> listDTO = new ArrayList<>();
    		for(Request request : list) listDTO.add(new RequestDTO(request));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PostMapping("/request/create/by-page/{page}")
	public ResponseEntity<Object> createPage(
			@PathVariable("page") int page_id
		){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
		
		try {
			Page page = pageService.getPage(page_id, account);
			Request request = requestService.createRequest(page, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new RequestDTO(request));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@DeleteMapping("/request/delete")
	public ResponseEntity<Object> deletePage(@RequestBody RequestDTO requestDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			requestService.deleteRequest(requestDTO, account);
			return ResponseEntity.status(HttpStatus.ACCEPTED).body(requestDTO);
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@GetMapping("/request/list/ready/by-key/{enginekey}")
	public ResponseEntity<Object> getReadyRequestListWithKey(
			@PathVariable("enginekey") String enginekey
	){
    	try{
    		List<Request> list = requestService.getReadyRequestListWithKey(enginekey);
    		List<RequestDTO> listDTO = new ArrayList<>();
    		for(Request request : list) listDTO.add(new RequestDTO(request));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PutMapping("/request/update/by-key/{enginekey}")
	public ResponseEntity<Object> updateRequestWithKey(
			@RequestBody RequestDTO requestDTO,
			@PathVariable("enginekey") String enginekey
		){    	
		try {
			Request request = requestService.updateRequestWithKey(requestDTO, enginekey);
			return ResponseEntity.status(HttpStatus.CREATED).body(new RequestDTO(request));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
}
