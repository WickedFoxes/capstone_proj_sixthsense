package com.capstone.sixthsense.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.ScheduleDTO;
import com.capstone.sixthsense.enumeration.ScanStatus;
import com.capstone.sixthsense.exception.NotExistException;
import com.capstone.sixthsense.exception.NotHaveAuthException;
import com.capstone.sixthsense.exception.NotNullException;
import com.capstone.sixthsense.model.Account;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Schedule;
import com.capstone.sixthsense.repository.ScheduleRepo;

@Service
public class ScheduleService {
	@Value("${engine.key}")
	String enginekey;	
	
	@Autowired
	private ScheduleRepo repo;
	
	public Schedule getSchedule(int id, Account account) {
		Schedule schedule = repo.findById(id);
		if(schedule == null) {
			throw new NotExistException("No data found.");
		}
		Project project = schedule.getProject();
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		return schedule;
	}
	public List<Schedule> getScheduleList(Account account) {
		List<Schedule> schedule_list = repo.findAll();
		ArrayList<Schedule> schedules = new ArrayList<>();
		for(Schedule schedule : schedule_list) {
			if(schedule.getProject().getAccount().getUsername().equals(account.getUsername())) {
				schedules.add(schedule);
			}
		}
		return schedules;
	}
	public Schedule createSchedule(ScheduleDTO scheduleDTO, Project project, Account account) {
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(scheduleDTO.getDate().isEmpty()) {
			throw new NotNullException("It should not be provided as a blank space.");
		}
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
		
		Schedule schedule = new Schedule();
		schedule.setTitle(scheduleDTO.getTitle());
		schedule.setDescription(scheduleDTO.getDescription());
		schedule.setProject(project);
		schedule.setRunningdate(LocalDateTime.parse(scheduleDTO.getDate(), formatter));
		schedule.setStatus(ScanStatus.READY);
		return repo.save(schedule);
	}
	public void deleteSchedule(ScheduleDTO scheduleDTO, Account account) {
		Project project = repo.findById(scheduleDTO.getId()).getProject();
		if(project == null || !project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotExistException("No data found.");
		}
		repo.deleteById(scheduleDTO.getId());
	}
	public Schedule updateSchedule(ScheduleDTO scheduleDTO, Account account) {
		Schedule schedule = repo.findById(scheduleDTO.getId());
		Project project = schedule.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(!scheduleDTO.getTitle().isBlank()) {
			schedule.setTitle(scheduleDTO.getTitle());
		}
		if(!scheduleDTO.getDescription().isBlank()) {
			schedule.setDescription(scheduleDTO.getDescription());
		}
		if(!scheduleDTO.getDate().isBlank()) {
			DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm");
			schedule.setRunningdate(LocalDateTime.parse(scheduleDTO.getDate(), formatter));	
		}
		schedule.setStatus(ScanStatus.READY);
		return repo.save(schedule);
	}
	
	public List<Schedule> getNextScheduleListWithKey(String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		List<Schedule> schedule_list = repo.findAll();
		ArrayList<Schedule> schedules = new ArrayList<>();
		for(Schedule schedule : schedule_list) {
			if(schedule.getStatus().equals(ScanStatus.READY) 
					&& schedule.isTimeForNextSchedule()) {
				schedules.add(schedule);
			}
		}
		return schedules;
	}
	public Schedule completeScheduleWithKey(String key, long schedule_id) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Schedule schedule = repo.findById(schedule_id);
		schedule.setStatus(ScanStatus.COMPLETE);
		return repo.save(schedule);
	}
	
}
