package com.capstone.sixthsense.model;

import com.capstone.sixthsense.enumeration.ItemType;
import com.capstone.sixthsense.enumeration.ScanStatus;

import jakarta.persistence.CascadeType;
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
import jakarta.validation.constraints.NotEmpty;

@Entity
@Table(name = "item")
public class Item {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;
	
	@Column(name = "itemtype")
	@Enumerated(EnumType.STRING)
	private ItemType itemtype;
	
	@Column(columnDefinition = "TEXT", name = "body")
	@NotEmpty
	private String body;	
	
	@Column(name = "tabindex")
	private int tabindex;

	@Column(name = "colorimg")
	private String colorimg;

	@Column(name = "grayimg")
	private String grayimg;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "page_id", referencedColumnName="id")
    private Page page;
	
	public Item() {}
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public ItemType getItemtype() {
		return itemtype;
	}

	public void setItemtype(ItemType itemtype) {
		this.itemtype = itemtype;
	}

	public String getBody() {
		return body;
	}

	public void setBody(String body) {
		this.body = body;
	}

	public int getTabindex() {
		return tabindex;
	}

	public void setTabindex(int tabindex) {
		this.tabindex = tabindex;
	}

	public String getColorimg() {
		return colorimg;
	}

	public void setColorimg(String colorimg) {
		this.colorimg = colorimg;
	}

	public String getGrayimg() {
		return grayimg;
	}

	public void setGrayimg(String grayimg) {
		this.grayimg = grayimg;
	}
	public Page getPage() {
		return page;
	}
	public void setPage(Page page) {
		this.page = page;
	}
	
}
