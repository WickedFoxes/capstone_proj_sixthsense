package com.capstone.sixthsense.dto;

import java.time.LocalDateTime;

import com.capstone.sixthsense.enumeration.RequestStatus;
import com.capstone.sixthsense.model.Request;

public class RequestDTO {
	private int id;
	private RequestStatus status;
    private LocalDateTime createdDate;
    private int page_id;
    private int project_id;
    private String image_name;
    public RequestDTO() {}
    public RequestDTO(Request request) {
    	this.id = request.getId();
    	this.status = request.getStatus();
    	this.createdDate = request.getCreatedDate();
    	this.page_id = request.getPage().getId();
    	this.project_id = request.getPage().getProject().getId();
    	this.image_name = request.getImage();
    }
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public RequestStatus getStatus() {
		return status;
	}
	public void setStatus(RequestStatus status) {
		this.status = status;
	}
	public LocalDateTime getCreatedDate() {
		return createdDate;
	}
	public void setCreatedDate(LocalDateTime createdDate) {
		this.createdDate = createdDate;
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
	public String getImage_name() {
		return image_name;
	}
	public void setImage_name(String image_name) {
		this.image_name = image_name;
	}
	
}
