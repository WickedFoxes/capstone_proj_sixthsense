package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.enumeration.ItemType;
import com.capstone.sixthsense.model.Item;

public class ItemDTO {
	private long id;
	private ItemType itemtype;
	private String body;	
	private long tabindex;
	private String colorimg;
	private String grayimg;
	private long page_id;
	private String css_selector;
    
    public ItemDTO() {}
    public ItemDTO(Item item) {
    	this.id = item.getId();
    	this.itemtype = item.getItemtype();
    	this.body = item.getBody();
    	this.tabindex = item.getTabindex();
    	this.css_selector = item.getCss_selector();
    	if(item.getColorimg() != null) {
    		this.colorimg = item.getColorimg().getName();
    	}
    	if(item.getGrayimg() != null) {
    		this.grayimg = item.getGrayimg().getName();
    	}
    	if(item.getPage() != null) {
    		this.page_id = item.getPage().getId();
    	}
    }
    
	public long getId() {
		return id;
	}
	public void setId(long id) {
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
	public long getTabindex() {
		return tabindex;
	}
	public void setTabindex(long tabindex) {
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
	public long getPage_id() {
		return page_id;
	}
	public void setPage_id(long page_id) {
		this.page_id = page_id;
	}
	public String getCss_selector() {
		return css_selector;
	}
	public void setCss_selector(String css_selector) {
		this.css_selector = css_selector;
	}
}
