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
import org.springframework.web.bind.annotation.RequestBody;

import com.capstone.sixthsense.dto.ItemDTO;
import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ScanDTO;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Scan;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.ItemService;
import com.capstone.sixthsense.service.PageService;
import com.capstone.sixthsense.service.ScanService;

@Controller
public class ScanController {
	@Autowired
	private ScanService scanService;
	@Autowired
	private ItemService itemService;
	@Autowired
	private PageService pageService;
	@Autowired
	private AccountService accountService;
	
	@GetMapping("/scan/list/by-page/{page_id}")
	public ResponseEntity<Object> getScanList(@PathVariable("page_id") int page_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		Page page = pageService.getPage(page_id, account);
    		List<Scan> list = scanService.getScanList(page, account);
    		List<ScanDTO> listDTO = new ArrayList<>();
    		for(Scan scan : list) {
    			listDTO.add(new ScanDTO(scan));
    		} 
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PostMapping("/scan/create/by-page/by-item/by-key/{page_id}/{item_id}/{enginekey}")
	public ResponseEntity<Object> createItemWithKey(
			@PathVariable("enginekey") String enginekey,
			@PathVariable("page_id") int page_id,
			@PathVariable("item_id") int item_id,
			@RequestBody Scan scan
		){
		try {
			Page page = pageService.getPageWithKey(page_id, enginekey);
			scan.setPage(page);
			Item item = itemService.getItemWithKey(item_id, enginekey);
			scan.setItem(item);
			
			Scan result = scanService.createScanWithKey(scan, enginekey);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ScanDTO(result));

		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@DeleteMapping("/scan/delete/by-page/by-key/{page_id}/{enginekey}")
	public ResponseEntity<Object> deleteScanList(
			@PathVariable("page_id") int page_id,
			@PathVariable("enginekey") String enginekey
		){
    	try{
    		Page page = pageService.getPageWithKey(page_id, enginekey);    		
    		scanService.deleteScanListWithKey(page, enginekey);
    		itemService.deleteItemListWithKey(page, enginekey);
    		return ResponseEntity.status(HttpStatus.OK).body(new PageDTO(page));     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
}
