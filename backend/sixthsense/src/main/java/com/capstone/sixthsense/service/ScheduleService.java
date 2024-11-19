package com.capstone.sixthsense.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.capstone.sixthsense.dto.ScheduleDTO;
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
	public Schedule createSchedule(Schedule schedule, Account account) {
		Project project = schedule.getProject();
		if(project == null) {
			throw new NotExistException("No data found.");
		}
		if(!project.getAccount().getUsername().equals(account.getUsername())) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		if(schedule.getDayofweek() < 0 
				|| schedule.getTime().isBlank()) {
			throw new NotNullException("It should not be provided as a blank space.");
		}
		schedule.calcNexttDateTime();
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
		
		schedule.setDayofweek(scheduleDTO.getDayofweek());
		schedule.setTime(scheduleDTO.getTime());
		schedule.calcNexttDateTime();
		
		return repo.save(schedule);
	}
	
	public List<Schedule> getNextScheduleListWithKey(String key) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		List<Schedule> schedule_list = repo.findAll();
		ArrayList<Schedule> schedules = new ArrayList<>();
		for(Schedule schedule : schedule_list) {
			if(schedule.isTimeForNextSchedule()) {
				schedules.add(schedule);
			}
		}
		return schedules;
	}
	
	public Schedule refreshNextScheduleWithKey(String key, long schedule_id) {
		if(!key.equals(enginekey)) {
			throw new NotHaveAuthException("you don't have Auth");
		}
		Schedule schedule = repo.findById(schedule_id);
		schedule.updateLastRunningDate();
		schedule.updateNextRunningDate();
		return repo.save(schedule);
	}
	
}
