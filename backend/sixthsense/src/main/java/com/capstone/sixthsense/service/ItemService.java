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
		Project project = item.getPage().getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return item;
	}
	public List<Item> getItemList(Page page, Account account){
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		Project project = page.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return repo.findAllByPage(page);
	}
	public Item updateItem(ItemDTO itemDTO, Account account) {
		Item item = repo.findById(itemDTO.getId());
		if(item == null) {
			throw new NotExistException("No data found.");
		}
		Project project = item.getPage().getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
//		if(itemDTO.get) {
//			throw new NotNullException("It should not be provided as a blank space.");
//		}
		
		item.setItemtype(itemDTO.getItemtype());
		item.setTabindex(itemDTO.getTabindex());
		item.setGrayimg(itemDTO.getGrayimg());
		item.setColorimg(itemDTO.getColorimg());
		item.setBody(itemDTO.getBody());
		return repo.save(item);
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
		Project project = item.getPage().getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		return repo.save(item);
	}
}
