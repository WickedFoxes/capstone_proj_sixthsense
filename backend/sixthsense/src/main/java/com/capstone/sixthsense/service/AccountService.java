package com.capstone.sixthsense.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.exception.UserAlreadyExistsException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.repository.AccountRepo;

@Service
public class AccountService implements UserDetailsService{
	@Autowired
	private AccountRepo repo;
	
	public Account getAccount(String username) {
		return repo.findByUsername(username);
	}
	public void deleteAccount(Account account) {
		repo.delete(account);
	}
	
	public Account signup(Account account) {
		BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
		account.setPassword(passwordEncoder.encode(account.getPassword()));
		
		if(repo.findByUsername(account.getUsername()) != null) {
			throw new UserAlreadyExistsException("Username already exists");
		}
    	if(account.getUsername().isBlank()||account.getPassword().isBlank()||account.getEmail().isBlank()) {
    		throw new NotNullException("It should not be provided as a blank space.");
    	}	
		return repo.save(account);
	}
	
	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException{
		Account account = repo.findByUsername(username);
		if(account == null) {
			throw new UsernameNotFoundException("User not found");
		}
		return new AccountDetails(account);
	}
}
