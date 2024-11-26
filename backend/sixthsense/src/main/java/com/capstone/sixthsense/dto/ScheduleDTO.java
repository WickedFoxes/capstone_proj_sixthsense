package com.capstone.sixthsense.dto;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Schedule;

public class ScheduleDTO {
	private long id;
	private String title;
	private String description;
    private String date;
	private LocalDateTime runningdate;
	private ScanStatus status;
    private long project_id;
	
    public ScheduleDTO(){}
    public ScheduleDTO(Schedule schedule){
    	this.id = schedule.getId();
    	this.title = schedule.getTitle();
    	this.description = schedule.getDescription();
    	this.runningdate = schedule.getRunningdate();
    	this.project_id = schedule.getProject().getId();
    	this.status = schedule.getStatus();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
        this.date = runningdate.format(formatter);
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
	
	public long getProject_id() {
		return project_id;
	}
	public void setProject_id(long project_id) {
		this.project_id = project_id;
	}
	public LocalDateTime getRunningdate() {
		return runningdate;
	}
	public void setRunningdate(LocalDateTime runningdate) {
		this.runningdate = runningdate;
	}
	public String getDate() {
		return date;
	}
	public void setDate(String date) {
		this.date = date;
	}
	public ScanStatus getStatus() {
		return status;
	}
	public void setStatus(ScanStatus status) {
		this.status = status;
	}
	
	
}
