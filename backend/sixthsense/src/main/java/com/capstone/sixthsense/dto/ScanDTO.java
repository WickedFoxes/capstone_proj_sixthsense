package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.model.Scan;

public class ScanDTO {
	private int id;
	private String error;
	private String errormessage;
	private String guide;
	private int page_id;
	private ItemDTO item;
	
    public ScanDTO() {}
    public ScanDTO(Scan scan) {
    	this.id = scan.getId();
    	this.error = scan.getErrortype();
    	this.errormessage = scan.getErrormessage();
    	this.guide = scan.getGuide();
    	this.page_id = scan.getPage().getId();
    	this.item = new ItemDTO(scan.getItem());
    }
	public int getId() {
		return id;
	}
	public void setId(int id) {
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
	public String getGuide() {
		return guide;
	}
	public void setGuide(String guide) {
		this.guide = guide;
	}
	public int getPage_id() {
		return page_id;
	}
	public void setPage_id(int page_id) {
		this.page_id = page_id;
	}
	public ItemDTO getItem() {
		return item;
	}
	public void setItem(ItemDTO item) {
		this.item = item;
	}
}
