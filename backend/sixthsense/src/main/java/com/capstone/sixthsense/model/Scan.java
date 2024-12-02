package com.capstone.sixthsense.model;

import com.capstone.sixthsense.enumeration.ErrorOption;
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
@Table(name = "scan")
public class Scan {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Column(name = "errortype")
	private String errortype;

	@Column(name = "errormessage")
	private String errormessage;
	
	@Column(name = "erroroption")
	@Enumerated(EnumType.STRING)
	private ErrorOption erroroption = ErrorOption.ERROR;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "page_id", referencedColumnName="id")
    private Page page;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "item_id", referencedColumnName="id")
    private Item item;

	public Scan() {}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public String getErrortype() {
		return errortype;
	}

	public void setErrortype(String errortype) {
		this.errortype = errortype;
	}

	public String getErrormessage() {
		return errormessage;
	}

	public void setErrormessage(String errormessage) {
		this.errormessage = errormessage;
	}

	public ErrorOption getErroroption() {
		return erroroption;
	}

	public void setErroroption(ErrorOption erroroption) {
		this.erroroption = erroroption;
	}

	public Page getPage() {
		return page;
	}

	public void setPage(Page page) {
		this.page = page;
	}

	public Item getItem() {
		return item;
	}

	public void setItem(Item item) {
		this.item = item;
	}
}
