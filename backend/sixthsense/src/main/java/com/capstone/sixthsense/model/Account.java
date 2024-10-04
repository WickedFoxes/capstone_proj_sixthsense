package com.capstone.sixthsense.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotEmpty;

@Entity
@Table(name = "account")
public class Account {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;
	
	@Column(name = "username", unique=true)
	@NotEmpty
	private String username;
	
	@Column(name = "password")
	@NotEmpty
	private String password;
	
	@Column(name = "email")
	@NotEmpty
	private String email;

	@OneToMany(mappedBy = "account", cascade=CascadeType.REMOVE)
	private List<Project> projects;

	// 기본 생성자 (파라미터가 없는 생성자) 이거 없으면 오류 발생
    public Account() {
    }
	public Account(@JsonProperty("id") int id, 
			@JsonProperty("username") String username, 
			@JsonProperty("password") String password,
			@JsonProperty("email") String email) {
		this.id = id;
		this.username = username;
		this.password = password;
		this.email = email;
	}
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public List<Project> getProjects() {
		return projects;
	}
	public void setProjects(List<Project> projects) {
		this.projects = projects;
	}
}
