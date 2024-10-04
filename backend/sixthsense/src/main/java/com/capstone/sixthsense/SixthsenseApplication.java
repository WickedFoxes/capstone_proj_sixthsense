package com.capstone.sixthsense;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing // JPA 감사 기능 활성화
public class SixthsenseApplication {

	public static void main(String[] args) {
		SpringApplication.run(SixthsenseApplication.class, args);
	}
}
