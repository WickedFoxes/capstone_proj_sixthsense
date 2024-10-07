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
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.capstone.sixthsense.dto.ItemDTO;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.ItemService;
import com.capstone.sixthsense.service.PageService;

@Controller
public class ItemController {
	@Autowired
	private ItemService itemService;
	@Autowired
	private PageService pageService;
	@Autowired
	private AccountService accountService;	
	
	@GetMapping("/item/list/by-page/{page_id}")
	public ResponseEntity<Object> getItemList(@PathVariable("page_id") int page_id){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		Page page = pageService.getPage(page_id, account);
    		List<Item> list = itemService.getItemList(page, account);
    		List<ItemDTO> listDTO = new ArrayList<>();
    		for(Item item : list) listDTO.add(new ItemDTO(item));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PostMapping("/item/create/by-page/by-key/{page_id}/{enginekey}")
	public ResponseEntity<Object> createItemWithKey(
			@PathVariable("page_id") int page_id,
			@PathVariable("enginekey") String enginekey,
			@RequestBody Item item
		){
		try {
			Page page = pageService.getPageWithKey(page_id, enginekey);
			item.setPage(page);
			
			Item result = itemService.createItemWithKey(item, enginekey);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ItemDTO(result));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
}
