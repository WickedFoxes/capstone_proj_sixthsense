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
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotEmpty;

@Entity
@Table(name = "item")
public class Item {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Column(name = "itemtype")
	@Enumerated(EnumType.STRING)
	private ItemType itemtype;
	
	@Column(columnDefinition = "TEXT", name = "body")
	@NotEmpty
	private String body;	
	
	@Column(name = "tabindex")
	private long tabindex;

	@Column(columnDefinition = "TEXT", name = "css_selector")
	private String css_selector;
	
	@OneToOne(cascade = CascadeType.ALL, orphanRemoval = true)
	@JoinColumn(name = "colorimg", referencedColumnName="id")
	private Image colorimg;

	@OneToOne(cascade = CascadeType.ALL, orphanRemoval = true)
	@JoinColumn(name = "grayimg", referencedColumnName="id")
	private Image grayimg;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "page_id", referencedColumnName="id")
    private Page page;
	
	public Item() {}	
	public Item(String body) {
		this.body = body;
	}
	public long getId() {
		return id;
	}
	public void setId(long id) {
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
	public long getTabindex() {
		return tabindex;
	}
	public void setTabindex(long tabindex) {
		this.tabindex = tabindex;
	}
	public String getCss_selector() {
		return css_selector;
	}
	public void setCss_selector(String css_selector) {
		this.css_selector = css_selector;
	}
	public Image getColorimg() {
		return colorimg;
	}
	public void setColorimg(Image colorimg) {
		this.colorimg = colorimg;
	}
	public Image getGrayimg() {
		return grayimg;
	}
	public void setGrayimg(Image grayimg) {
		this.grayimg = grayimg;
	}
	public Page getPage() {
		return page;
	}
	public void setPage(Page page) {
		this.page = page;
	}
}
