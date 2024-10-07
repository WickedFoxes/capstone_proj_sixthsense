package com.capstone.sixthsense.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Item;
import com.capstone.sixthsense.model.Page;

@Repository
public interface ItemRepo extends JpaRepository<Item, Integer>{
	List<Item> findAllByPage(Page page);
	Item findById(int id);
}
