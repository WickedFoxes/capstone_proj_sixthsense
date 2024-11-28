package com.capstone.sixthsense.model;

import java.time.LocalDateTime;
import java.time.ZoneId;

import com.capstone.sixthsense.enumeration.ScanStatus;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "schedule")
public class Schedule {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;

	@Column(name = "title")
	private String title;
	
	@Column(columnDefinition = "TEXT", name = "description")
	private String description;
	
	@Column(name = "runningdate")
    private LocalDateTime runningdate;
	
	@Column(name = "status")
	@Enumerated(EnumType.STRING)
	private ScanStatus status = ScanStatus.READY;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "project_id", referencedColumnName="id")
    private Project project;
	
	public Schedule() {}
	
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
	public LocalDateTime getRunningdate() {
		return runningdate;
	}
	public void setRunningdate(LocalDateTime runningdate) {
		this.runningdate = runningdate;
	}
	public Project getProject() {
		return project;
	}
	public void setProject(Project project) {
		this.project = project;
	}
	public ScanStatus getStatus() {
		return status;
	}
	public void setStatus(ScanStatus status) {
		this.status = status;
	}

	public boolean isTimeForNextSchedule() {
		if(this.runningdate == null) return false;
		return LocalDateTime.now(ZoneId.of("Asia/Seoul")).isAfter(this.runningdate);
	}
}
