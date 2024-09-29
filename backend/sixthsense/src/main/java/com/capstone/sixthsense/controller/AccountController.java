package com.capstone.sixthsense.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
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
    public Map<String, String> Home() {
    	HashMap<String, String> map = new HashMap<>();
    	
        map.put("welcom", "This is sixthsense API server for automatic web accessibility scanning.");
        map.put("isAuthenticated", String.valueOf(isAuthenticated()));
        map.put("username", null);
        map.put("userID", null);
        
        if(isAuthenticated()) {
        	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        	AccountDetails account = (AccountDetails)authentication.getPrincipal();
        	map.put("username", account.getUsername());
        	map.put("userID", String.valueOf(account.getId()));
        }
    	return map;
    }
    
    @PostMapping("/auth/login")
    public ResponseEntity<HashMap<String, String>> login(
    		@RequestBody LoginDTO loginRequest, 
    		HttpServletRequest request
    ) {    	
    	HashMap<String, String> map = new HashMap<>();
    	
    	UsernamePasswordAuthenticationToken authenticationToken = 
            new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword());
        
    	Authentication authentication = null;
    	SecurityContext securityContext = null;
    	try {
            authentication = authenticationManager.authenticate(authenticationToken);
            securityContext = SecurityContextHolder.getContext();
            securityContext.setAuthentication(authentication);
    	} catch(Exception e) {
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
        
        // 세션에 SecurityContext 저장
        HttpSession session = request.getSession(true);
        session.setAttribute(HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY, securityContext);
        
        AccountDetails account = (AccountDetails)authentication.getPrincipal();
        map.put("welcom", "This is sixthsense API server for automatic web accessibility scanning.");
        map.put("isAuthenticated", "true");
        map.put("username", account.getUsername());
        
        return ResponseEntity.status(HttpStatus.CREATED).body(map);
    }
    
    @PostMapping("/auth/signup")
    public ResponseEntity<HashMap<String, String>> signup(@RequestBody Account account) {
    	HashMap<String, String> map = new HashMap<>();
    	try {
    		service.signup(account);
    		map.put("username", account.getUsername());
    		map.put("email", account.getEmail());
    		return ResponseEntity.status(HttpStatus.CREATED).body(map);
    	}catch(Exception e){
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
}
