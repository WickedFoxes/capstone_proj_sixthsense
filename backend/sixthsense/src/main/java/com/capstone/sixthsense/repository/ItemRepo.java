package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Page;

import jakarta.transaction.Transactional;

@Repository
public interface ItemRepo extends JpaRepository<Item, Long>{
	@Transactional
	void deleteAllByPage(Page page);
	Item findById(long id);
}
