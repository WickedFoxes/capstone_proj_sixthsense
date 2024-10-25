package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Page;

public class PageDTO {
	private long id;
	private String title;
	private String url;
    private long project_id;
    private ScanStatus status;
    public PageDTO() {}
    public PageDTO(Page page) {
    	this.id = page.getId();
    	this.title = page.getTitle();
    	this.url = page.getUrl();
    	this.project_id = page.getProject().getId();
    	this.status = page.getStatus();
    }
	public long getId() {
		return id;
	}
	public void setId(long id) {
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
	public long getProject_id() {
		return project_id;
	}
	public void setProject_id(long project_id) {
		this.project_id = project_id;
	}
	public ScanStatus getStatus() {
		return status;
	}
	public void setStatus(ScanStatus status) {
		this.status = status;
	}
	
}
