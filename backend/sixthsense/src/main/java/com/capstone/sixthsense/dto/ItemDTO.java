package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.enumeration.ItemType;
import com.capstone.sixthsense.model.Item;

public class ItemDTO {
	private int id;
	private ItemType itemtype;
	private String body;	
	private int tabindex;
	private String colorimg;
	private String grayimg;
    private int page_id;
    private int project_id;
    
    public ItemDTO() {}
    public ItemDTO(Item item) {
    	this.id = item.getId();
    	this.itemtype = item.getItemtype();
    	this.body = item.getBody();
    	this.tabindex = item.getTabindex();
    	this.colorimg = item.getColorimg();
    	this.grayimg = item.getGrayimg();
    	this.page_id = item.getPage().getId();
    	this.project_id = item.getPage().getProject().getId();
    }
    
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public ItemType getItemtype() {
		return itemtype;
	}
	public void setItemtype(ItemType itemtype) {
		this.itemtype = itemtype;
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
