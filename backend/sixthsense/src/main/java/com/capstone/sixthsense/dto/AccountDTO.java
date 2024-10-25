package com.capstone.sixthsense.dto;

import com.capstone.sixthsense.model.Account;

public class AccountDTO {
	private long id;
	private String username;
	private String email;
	
	public AccountDTO() {}
	public AccountDTO(int id, String username, String email) {
		super();
		this.id = id;
		this.username = username;
		this.email = email;
	}
	public AccountDTO(Account account) {
		this.id = account.getId();
		this.username = account.getUsername();
		this.email = account.getEmail();
	}
	
	
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	
}
