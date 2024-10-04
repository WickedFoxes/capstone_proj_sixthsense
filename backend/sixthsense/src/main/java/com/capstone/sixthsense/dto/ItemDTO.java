package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.enumeration.ItemType;
import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Request;

public class ItemDTO {
	private int id;
	private ItemType type;
	private String body;	
	private int tabindex;
	private String colorimg;
	private String grayimg;
    private int request_id;
    private int page_id;
    private int project_id;
    
    public ItemDTO() {}
    public ItemDTO(Item item) {
    	this.id = item.getId();
    	this.type = item.getType();
    	this.body = item.getBody();
    	this.tabindex = item.getTabindex();
    	this.colorimg = item.getColorimg();
    	this.grayimg = item.getGrayimg();
    	this.request_id = item.getRequest().getId();
    	this.page_id = item.getRequest().getPage().getId();
    	this.project_id = item.getRequest().getPage().getProject().getId();
    }
    
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public ItemType getType() {
		return type;
	}
	public void setType(ItemType type) {
		this.type = type;
	}
	public String getBody() {
		return body;
	}
	public void setBody(String body) {
		this.body = body;
	}
	public int getTabindex() {
		return tabindex;
	}
	public void setTabindex(int tabindex) {
		this.tabindex = tabindex;
	}
	public String getColorimg() {
		return colorimg;
	}
	public void setColorimg(String colorimg) {
		this.colorimg = colorimg;
	}
	public String getGrayimg() {
		return grayimg;
	}
	public void setGrayimg(String grayimg) {
		this.grayimg = grayimg;
	}
	public int getRequest_id() {
		return request_id;
	}
	public void setRequest_id(int request_id) {
		this.request_id = request_id;
	}
	public int getPage_id() {
		return page_id;
	}
	public void setPage_id(int page_id) {
		this.page_id = page_id;
	}
	public int getProject_id() {
		return project_id;
	}
	public void setProject_id(int project_id) {
		this.project_id = project_id;
	}
    
}
