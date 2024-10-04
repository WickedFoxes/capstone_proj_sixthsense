package com.capstone.sixthsense.model;

import com.capstone.sixthsense.enumeration.ItemType;
import com.capstone.sixthsense.enumeration.RequestStatus;

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
	
	@Column(name = "type")
	@Enumerated(EnumType.STRING)
	@NotEmpty
	private ItemType type;
	
	@Column(name = "body")
	@NotEmpty
	private String body;	
	
	@Column(name = "tabindex")
	@NotEmpty
	private int tabindex;

	@Column(name = "colorimg")
	@NotEmpty
	private String colorimg;

	@Column(name = "grayimg")
	@NotEmpty
	private String grayimg;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "request_id", referencedColumnName="id")
    private Request request;

	public Item() {}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public ItemType getType() {
		return type;
	}

	public void setType(ItemType type) {
		this.type = type;
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
	
	public Request getRequest() {
		return request;
	}

	public void setRequest(Request request) {
		this.request = request;
	}
}
