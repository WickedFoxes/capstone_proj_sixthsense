package com.capstone.sixthsense.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.ItemDTO;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.repository.ItemRepo;

@Service
public class ItemService {
	@Value("${engine.key}")
	String enginekey;	
	
	@Autowired
	private ItemRepo repo;
	public Item getItem(int id, Account account) {
		Item item = repo.findById(id);
		if(item == null) {
			throw new NotExistException("No data found.");
		}
		return item;
	}
	
	public Item getItemWithKey(int id, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Item item = repo.findById(id);
		if(item == null) {
			throw new NotExistException("No data found.");
		}
		return item;
	}
	
	public Item createItemWithKey(Item item, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}		
		return repo.save(item);
	}

	public Page deleteItemListWithKey(Page page, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		repo.deleteAllByPage(page);
		return page;
	}
}
