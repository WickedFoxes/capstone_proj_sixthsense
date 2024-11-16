package com.capstone.sixthsense.controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.capstone.sixthsense.dto.PageDTO;
import com.capstone.sixthsense.dto.ProjectDTO;
import com.capstone.sixthsense.dto.ScheduleDTO;
import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.AccountDetails;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Schedule;
import com.capstone.sixthsense.service.AccountService;
import com.capstone.sixthsense.service.PageService;
import com.capstone.sixthsense.service.ProjectService;
import com.capstone.sixthsense.service.ScheduleService;

@Controller
public class ScheduleController {
	@Autowired
	private ScheduleService scheduleService;
	@Autowired
	private ProjectService projectService;
	@Autowired
	private AccountService accountService;	
	
	@GetMapping("/schedule/list")
	public ResponseEntity<Object> getScheduleList(){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
    	try{
    		List<Schedule> schedule_list = scheduleService.getScheduleList(account);
    		List<ScheduleDTO> listDTO = new ArrayList<>();
    		for(Schedule schedule : schedule_list) {
    			listDTO.add(new ScheduleDTO(schedule));
    		} 
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PostMapping("/schedule/create/by-project/{project}")
	public ResponseEntity<Object> createSchedule(
			@PathVariable("project") int project_id,
			@RequestBody Schedule schedule
		){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			Project project = projectService.getProject(project_id, account);
			schedule.setProject(project);
			Schedule result = scheduleService.createSchedule(schedule, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ScheduleDTO(result));
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}	
	}
	
	@PutMapping("/schedule/update")
	public ResponseEntity<Object> updateSchedule(@RequestBody ScheduleDTO scheduleDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			Schedule schedule = scheduleService.updateSchedule(scheduleDTO, account);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ScheduleDTO(schedule));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@DeleteMapping("/schedule/delete")
	public ResponseEntity<Object> deleteSchedule(@RequestBody ScheduleDTO scheduleDTO){
    	Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
    	AccountDetails accountDetail = (AccountDetails)authentication.getPrincipal();
    	Account account = accountService.getAccount(accountDetail.getUsername());
    	
		try {
			scheduleService.deleteSchedule(scheduleDTO, account);
			return ResponseEntity.status(HttpStatus.ACCEPTED).body(scheduleDTO);
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
	
	@GetMapping("/schedule/list/nextschedule/by-key/{enginekey}")
	public ResponseEntity<Object> getScheduleListWithKey(
			@PathVariable("enginekey") String enginekey
	){
    	try{
    		List<Schedule> list = scheduleService.getNextScheduleListWithKey(enginekey);
    		List<ScheduleDTO> listDTO = new ArrayList<>();
    		for(Schedule schedule : list) listDTO.add(new ScheduleDTO(schedule));
    		
    		return ResponseEntity.status(HttpStatus.OK).body(listDTO);     
    		
    	} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);    		
    	}
	}
	
	@PutMapping("/schedule/update/by-schedule/by-key/{schedule_id}/{enginekey}")
	public ResponseEntity<Object> updateScheduleWithKey(
			@PathVariable("schedule_id") long schedule_id,
			@PathVariable("enginekey") String enginekey
		){    	
		try {
			Schedule schedule = scheduleService.refreshNextScheduleWithKey(enginekey, schedule_id);
			return ResponseEntity.status(HttpStatus.CREATED).body(new ScheduleDTO(schedule));
			
		} catch(Exception e){
			HashMap<String, String> map = new HashMap<>();
    		map.put("error", e.getMessage());
    		return ResponseEntity.status(HttpStatus.CONFLICT).body(map);
    	}
	}
}
