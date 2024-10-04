package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.model.Page;

public class PageDTO {
	private int id;
	private String title;
	private String url;
    private int project_id;
    public PageDTO() {}
    public PageDTO(Page page) {
    	this.id = page.getId();
    	this.title = page.getTitle();
    	this.url = page.getUrl();
    	this.project_id = page.getProject().getId();
    }
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public int getProject_id() {
		return project_id;
	}
	public void setProject_id(int project_id) {
		this.project_id = project_id;
	}
    
}
