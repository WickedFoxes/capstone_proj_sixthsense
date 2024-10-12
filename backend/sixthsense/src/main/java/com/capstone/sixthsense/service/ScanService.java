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
import com.capstone.sixthsense.model.Scan;
import com.capstone.sixthsense.repository.ItemRepo;
import com.capstone.sixthsense.repository.ScanRepo;

@Service
public class ScanService {
	@Value("${engine.key}")
	String enginekey;	
	
	@Autowired
	private ScanRepo repo;
	public Scan getScan(int id, Account account) {
		Scan scan = repo.findById(id);
		if(scan == null) {
			throw new NotExistException("No data found.");
		}
		Project project = scan.getPage().getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return scan;
	}
	
	public List<Scan> getScanList(Page page, Account account) {
		if(page == null) {
			throw new NotExistException("No data found.");
		}
		Project project = page.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return repo.findAllByPage(page);
	}
	
	public Scan getScanWithKey(int id, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Scan scan = repo.findById(id);
		if(scan == null) {
			throw new NotExistException("No data found.");
		}
		return scan;
	}
	
	public Scan createScanWithKey(Scan scan, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}	
		return repo.save(scan);
	}
	
	public Page deleteScanListWithKey(Page page, String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		repo.deleteAllByPage(page);
		return page;
	}
}
