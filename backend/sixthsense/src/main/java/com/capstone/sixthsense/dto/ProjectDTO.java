package com.capstone.sixthsense.dto;

import java.time.LocalDateTime;

import com.capstone.sixthsense.model.Project;

public class ProjectDTO {
    private long id;
	private String title;
    private String description;
    private String username;
    private String image_name;
    private LocalDateTime createdDate;
    private boolean isComplete;
    
    public ProjectDTO() {}
    public ProjectDTO(Project project) {
    	this.id = project.getId();
    	this.title = project.getTitle();
    	this.description = project.getDescription();
    	this.username = project.getAccount().getUsername();
    	this.createdDate = project.getCreatedDate();
    	this.image_name = project.getImage();
    	this.isComplete = project.isComplete();
    }
	
	public LocalDateTime getCreatedDate() {
		return createdDate;
	}
	public void setCreatedDate(LocalDateTime createdDate) {
		this.createdDate = createdDate;
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
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getImage_name() {
		return image_name;
	}
	public void setImage_name(String image_name) {
		this.image_name = image_name;
	}
	public boolean isComplete() {
		return isComplete;
	}
	public void setComplete(boolean isComplete) {
		this.isComplete = isComplete;
	}
	
}
