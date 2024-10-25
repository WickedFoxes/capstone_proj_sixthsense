package com.capstone.sixthsense.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.capstone.sixthsense.model.Account;

import java.util.Optional;

@Repository
public interface AccountRepo extends JpaRepository<Account, Long>{
	Account findByUsername(String username);
	Account findById(int id);
}
