package com.capstone.sixthsense.model;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import com.capstone.sixthsense.enumeration.PageType;
import com.capstone.sixthsense.enumeration.ScanStatus;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
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
@Table(name = "page")
public class Page {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Column(name = "title")
	private String title;
	
	@Column(name = "url")
	private String url;
	
	@Column(name = "status")
	@Enumerated(EnumType.STRING)
	private ScanStatus status;
	
	@Column(name = "pagetype")
	@Enumerated(EnumType.STRING)
	private PageType pagetype = PageType.URL;
	
	@Column(columnDefinition = "TEXT", name = "htmlbody")
	private String htmlbody; 
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "project_id", referencedColumnName="id")
    private Project project;
	
	@OneToMany(mappedBy = "page", cascade=CascadeType.REMOVE)
	private List<Scan> scans;

	@OneToMany(mappedBy = "page", cascade=CascadeType.REMOVE)
	private List<Item> items;
	
	public Page() {}

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

	public Project getProject() {
		return project;
	}

	public void setProject(Project project) {
		this.project = project;
	}

	public List<Scan> getSacns() {
		return scans;
	}
	
	public void setScans(List<Scan> scans) {
		this.scans = scans;
	}

	public ScanStatus getStatus() {
		return status;
	}

	public void setStatus(ScanStatus status) {
		this.status = status;
	}

	public List<Item> getItems() {
		return items;
	}

	public void setItems(List<Item> items) {
		this.items = items;
	}

	public List<Scan> getScans() {
		return scans;
	}

	public String getHtmlbody() {
		return htmlbody;
	}

	public void setHtmlbody(String htmlbody) {
		this.htmlbody = htmlbody;
	}

	public PageType getPagetype() {
		return pagetype;
	}

	public void setPagetype(PageType pagetype) {
		this.pagetype = pagetype;
	}
	
}
