package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.enumeration.ErrorOption;
import com.capstone.sixthsense.model.Scan;

public class ScanDTO {
	private long id;
	private String error;
	private String errormessage;
	private ErrorOption erroroption;
	private long page_id;
	private ItemDTO item;
	
    public ScanDTO() {}
    public ScanDTO(Scan scan) {
    	this.id = scan.getId();
    	this.error = scan.getErrortype();
    	this.errormessage = scan.getErrormessage();
    	this.erroroption = scan.getErroroption();
    	this.page_id = scan.getPage().getId();
    	this.item = new ItemDTO(scan.getItem());
    }
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getError() {
		return error;
	}
	public void setError(String error) {
		this.error = error;
	}
	public String getErrormessage() {
		return errormessage;
	}
	public void setErrormessage(String errormessage) {
		this.errormessage = errormessage;
	}
	public ErrorOption getErroroption() {
		return erroroption;
	}
	public void setErroroption(ErrorOption erroroption) {
		this.erroroption = erroroption;
	}
	public long getPage_id() {
		return page_id;
	}
	public void setPage_id(long page_id) {
		this.page_id = page_id;
	}
	public ItemDTO getItem() {
		return item;
	}
	public void setItem(ItemDTO item) {
		this.item = item;
	}
}
