package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Project;
import com.capstone.sixthsense.model.Scan;
import com.capstone.sixthsense.model.Schedule;

import jakarta.transaction.Transactional;

@Repository
public interface ScheduleRepo extends JpaRepository<Schedule, Long>{
	List<Schedule> findAll();
	Schedule findById(long id);
}
