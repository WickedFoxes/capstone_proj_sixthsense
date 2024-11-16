package com.capstone.sixthsense.dto;

import java.time.LocalDateTime;

import com.capstone.sixthsense.model.Schedule;

public class ScheduleDTO {
	private long id;
	private String title;
	private String description;
	private int dayofweek;
	private String time;
    private LocalDateTime lastRunningDate;
    private LocalDateTime nextRunningDate;
    private long project_id;
	
    public ScheduleDTO(){}
    public ScheduleDTO(Schedule schedule){
    	this.id = schedule.getId();
    	this.title = schedule.getTitle();
    	this.description = schedule.getDescription();
    	this.dayofweek = schedule.getDayofweek();
    	this.time = schedule.getTime();
    	this.lastRunningDate = schedule.getLastRunningDate();
    	this.nextRunningDate = schedule.getNextRunningDate();
    	this.project_id = schedule.getProject().getId();
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
	public int getDayofweek() {
		return dayofweek;
	}
	public void setDayofweek(int dayofweek) {
		this.dayofweek = dayofweek;
	}
	public String getTime() {
		return time;
	}
	public void setTime(String time) {
		this.time = time;
	}
	public LocalDateTime getLastRunningDate() {
		return lastRunningDate;
	}
	public void setLastRunningDate(LocalDateTime lastRunningDate) {
		this.lastRunningDate = lastRunningDate;
	}
	public LocalDateTime getNextRunningDate() {
		return nextRunningDate;
	}
	public void setNextRunningDate(LocalDateTime nextRunningDate) {
		this.nextRunningDate = nextRunningDate;
	}
	public long getProject_id() {
		return project_id;
	}
	public void setProject_id(long project_id) {
		this.project_id = project_id;
	}
}
