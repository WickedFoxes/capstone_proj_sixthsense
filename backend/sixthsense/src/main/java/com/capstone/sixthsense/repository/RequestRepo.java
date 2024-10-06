package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.enumeration.RequestStatus;
import com.capstone.sixthsense.model.Page;
import com.capstone.sixthsense.model.Request;

@Repository
public interface RequestRepo extends JpaRepository<Request, Integer>{
	List<Request> findAll();
	List<Request> findAllByPage(Page page);
	List<Request> findAllByStatus(RequestStatus status);
	Request findById(int id);
}
