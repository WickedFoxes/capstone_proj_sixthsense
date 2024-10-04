package com.capstone.sixthsense.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;

import com.capstone.sixthsense.dto.AccountDTO;
import com.capstone.sixthsense.dto.LoginDTO;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.exception.UserAlreadyExistsException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.service.AccountService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@RestController
public class AccountController {
	private final AuthenticationManager authenticationManager;
	
    public AccountController(AuthenticationManager authenticationManager) {
        this.authenticationManager = authenticationManager;
    }
	
	@Autowired
	private AccountService service;
	
    @GetMapping("/")
    public Map<String, String> home() {
    	HashMap<String, String> map = new HashMap<>();
    	
        map.put("welcom", "This is sixthsense API server for automatic web accessibility scanning.");
        map.put("isAuthenticated", String.valueOf(isAuthenticated()));
        
        if(isAuthenticated()) {
        	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        	AccountDetails account = (AccountDetails)authentication.getPrincipal();
        	map.put("username", account.getUsername());
        	map.put("userID", String.valueOf(account.getId()));
        }
    	return map;
    }
    
    @PostMapping("/auth/login")
    public ResponseEntity<Object> login(
    		@RequestBody LoginDTO loginRequest, 
    		HttpServletRequest request
    ) {    	
    	UsernamePasswordAuthenticationToken authenticationToken = 
            new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword());
        
    	Authentication authentication = null;
    	SecurityContext securityContext = null;
    	try {
            authentication = authenticationManager.authenticate(authenticationToken);
            securityContext = SecurityContextHolder.getContext();
            securityContext.setAuthentication(authentication);
    	} catch(Exception e) {
    		HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
        
        // 세션에 SecurityContext 저장
        HttpSession session = request.getSession(true);
        session.setAttribute(HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY, securityContext);
        
        AccountDetails accountDetails = (AccountDetails)authentication.getPrincipal();
        Account account = service.getAccount(accountDetails.getUsername());
        
        return ResponseEntity.status(HttpStatus.CREATED).body(new AccountDTO(account));
    }
    
    @PostMapping("/auth/signup")
    public ResponseEntity<Object> signup(@RequestBody Account account) {
    	try {
    		service.signup(account);
    		return ResponseEntity.status(HttpStatus.CREATED).body(new AccountDTO(account));
    	}catch(Exception e){
    		HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
    }
    
    // 로그인 여부 확인
    private boolean isAuthenticated() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || authentication instanceof AnonymousAuthenticationToken) {
            return false;
        }
        return authentication.isAuthenticated();
    }
    
    @DeleteMapping("/auth/delete")
    public ResponseEntity<Object> deleteAccount(HttpServletRequest request){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = service.getAccount(accountDetail.getUsername());
		
    	HashMap<String, String> map = new HashMap<>();
    	try {
    		service.deleteAccount(account);
    		map.put("success", "Deletion of account was successful.");
            HttpSession session = request.getSession();
            session.invalidate();
    		return ResponseEntity.status(HttpStatus.ACCEPTED).body(map);
    	} catch(Exception e){
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
    	
    }
}
