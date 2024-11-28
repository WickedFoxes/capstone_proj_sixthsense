package com.capstone.sixthsense.model;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import com.capstone.sixthsense.enumeration.ScanStatus;
import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotEmpty;

@Entity
@EntityListeners(AuditingEntityListener.class) // 감사 기능 활성화
@Table(name = "project")
public class Project {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Column(name = "title")
	@NotEmpty
	private String title;
	
	@Column(name = "description")
	@NotEmpty
	private String description;
	
	@Column(name = "createdDate", nullable = false, updatable = false)
    @CreatedDate
    private LocalDateTime createdDate;

	@Column(name = "image")
	private String image;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "account_id", referencedColumnName="id")
    private Account account;
	
	@OneToMany(mappedBy = "project", cascade=CascadeType.REMOVE)
	private List<Page> pages;
	
    @OneToMany(mappedBy = "project", cascade = CascadeType.REMOVE)
    private List<Schedule> schedules;
	
	public Project() {}

	public Account getAccount() {
		return account;
	}

	public void setAccount(Account account) {
		this.account = account;
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

	public LocalDateTime getCreatedDate() {
		return createdDate;
	}

	public void setCreatedDate(LocalDateTime createdDate) {
		this.createdDate = createdDate;
	}

	public List<Page> getPages() {
		return pages;
	}

	public void setPages(List<Page> pages) {
		this.pages = pages;
	}

	public String getImage() {
		return image;
	}

	public void setImage(String image) {
		this.image = image;
	}
	
	public boolean isComplete() {
		if(this.getPages() == null) return true;
		for(Page page : this.getPages()) {
			if(!page.getStatus().equals(ScanStatus.COMPLETE))
				return false;
		}
		return true;
	}
}
