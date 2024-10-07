package com.capstone.sixthsense.dto;

import java.time.LocalDateTime;
import java.util.List;

import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;

public class ProjectPageDTO {
	private Project project;
	private List<Page> pageList;
    
    public ProjectPageDTO() {}

	public Project getProject() {
		return project;
	}

	public void setProject(Project project) {
		this.project = project;
	}

	public List<Page> getPageList() {
		return pageList;
	}

	public void setPageList(List<Page> pageList) {
		this.pageList = pageList;
	}
	
}
